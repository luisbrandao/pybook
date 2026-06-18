"""Strategy B: decode EBoN's compiled .qch (Quick Chapter) binary files.

The .qch is the preprocessed form of a chapter. The original seed names are not
stored, but the full generation model is. This decoder is a faithful port of
EBoN's own reader (EBoN.exe:0x41cd90, reverse-engineered via Ghidra; see
Doc/qch-writer-decompiled.md). It reads the entire file and is validated to land
exactly on the trailing '#END' for every known-seed chapter (debug/Luis/klingon).

Numeric encodings recovered from the binary:
  * strings are NUL-terminated latin-1,
  * multi-byte counts/frequencies are BIG-ENDIAN uint16 (high byte first),
  * boolean validity masks are bit-packed LSB-first, 8 per byte.

Extracted fields: metadata, GENOPT, the consonant alphabet, the consonant
ELEMENT list and the vowel ELEMENT list (both multi-letter clusters), the M1/M2
fit-frequency matrices, prefix/suffix two-element keys with frequencies, the
structure / substructure tables, and the four FIT VALIDITY MASKS.

Semantics recovered empirically (bit-exact against the known seeds of
debug/Luis/klingon/ROMANFEM):

  * M1 [vowel x nV] and M2 [cons x nV] are POSITIONAL frequency tables, not
    adjacency: column 0 counts the element name-initially, column nV-1 counts
    it name-finally, and the middle columns count medial use (with the prefix
    GENOPT on, all medials collapse into column 1; with it off they spread
    over columns 1..(nV-1)>>1 start-anchored and (nV-n+p)>>1 end-anchored —
    see the generator decompile, research/ebonW_00420730.c:1066).
  * The transition data is the four bit-packed validity masks, indexed
    [next][prev]. Consonants fit as single LETTERS (Doc/3): the letter axis is
    the character's position in LETTER_TABLE, EBoN's fixed 63-slot internal
    consonant table (extracted verbatim from EBoN.exe @0x92b84; the generator
    indexes the masks via strchr on it — ebonW_00420730.c:2798).
    mask_cv: vowel element following a consonant last-letter (fit L1);
    mask_vc: consonant first-letter following a vowel element (L1);
    mask_cc: consonant first-letter following a consonant last-letter across a
    vowel (L2); mask_vv: vowel element following a vowel element across a
    consonant (L3).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import List, Tuple

# EBoN's internal consonant-letter table (EBoN.exe @0x92b84). The fit masks'
# 64-wide letter axis is a character's index in this string: 0-19 plain
# consonants, 20-39 their soft (-H) forms, 40-50 accented (ç ð ñ þ š Ç Ð Ñ Þ
# Š ß as raw cp1252/latin-1 bytes, matching our latin-1 string decode),
# 51-60 the SPCCON digit codes, 61-62 semivowel y/u.
LETTER_TABLE = ("BCDFGHJKLMNPQRSTVWXZ"
                "bcdfghjklmnpqrstvwxz"
                "\xe7\xf0\xf1\xfe\x9a\xc7\xd0\xd1\xde\x8a\xdf"
                "0123456789"
                "yu")
LETTER_INDEX = {c: i for i, c in enumerate(LETTER_TABLE)}


# ----------------------------------------------------------------------------- #
# Low-level reader matching EBoN's on-disk format.
# ----------------------------------------------------------------------------- #
class _Reader:
    def __init__(self, buf: bytes):
        self.b = buf
        self.p = 0

    def u8(self) -> int:
        v = self.b[self.p]
        self.p += 1
        return v

    def u16(self) -> int:  # BIG-ENDIAN (writer emits high byte then low byte)
        hi = self.b[self.p]
        lo = self.b[self.p + 1]
        self.p += 2
        return hi * 256 + lo

    def cstr(self) -> str:
        e = self.b.index(b"\x00", self.p)
        s = self.b[self.p:e].decode("latin-1")
        self.p = e + 1
        return s

    def raw(self, n: int) -> bytes:
        v = self.b[self.p:self.p + n]
        self.p += n
        return v


@dataclass
class QchChapter:
    """Everything decoded from a .qch, in EBoN's own terms."""
    title: str = ""
    line2: str = ""
    line3: str = ""
    line4: str = ""
    author: str = ""

    flags: int = 0
    fit: int = 0
    val: int = 0
    structgen: bool = False
    statgen: bool = False
    prefix_opt: bool = False
    suffix_opt: bool = False
    shuffle: bool = False

    consonants: str = ""                 # the consonant alphabet (single letters)
    nV: int = 0                          # matrix inner (fit-distance) dimension
    special_clusters: List[str] = field(default_factory=list)  # SPCCON: digit code N -> clusters[N]

    vowel_elements: List[str] = field(default_factory=list)   # list44
    cons_elements: List[str] = field(default_factory=list)    # list48
    M1: List[List[int]] = field(default_factory=list)         # [vowel x nV] fit freqs
    M2: List[List[int]] = field(default_factory=list)         # [cons  x nV] fit freqs

    # Prefix/suffix: each key is (idxA, idxB, tag); tag 0x56 ('V') => idxB is the
    # vowel element (else idxA). Indices: consonants by cons_elements position,
    # vowels by vowel_elements position.
    pre_keys: List[Tuple[int, int, int]] = field(default_factory=list)
    pre_freq: List[int] = field(default_factory=list)
    suf_keys: List[Tuple[int, int, int]] = field(default_factory=list)
    suf_freq: List[int] = field(default_factory=list)

    struct_freq: List[int] = field(default_factory=list)      # index = structure number
    sub_counts: List[int] = field(default_factory=list)
    sub_freq: List[List[int]] = field(default_factory=list)
    sub_labels: List[List[str]] = field(default_factory=list)

    # Fit validity masks as sets of allowed (next, prev) index pairs.
    # Vowels are indexed by vowel_elements position; consonants by single
    # LETTER = position in LETTER_TABLE. See the module docstring.
    mask_cv: set = field(default_factory=set)   # (vowel idx, prev letter idx)   L1
    mask_vc: set = field(default_factory=set)   # (letter idx, prev vowel idx)   L1
    mask_cc: set = field(default_factory=set)   # (letter idx, prev letter idx)  L2
    mask_vv: set = field(default_factory=set)   # (vowel idx, prev vowel idx)    L3

    # Resolve a prefix/suffix entry to its two elements in sequence order.
    # `a` is the first element, `b` the second; the tag gives the C/V pattern:
    #   tag 'C' (0x43) -> consonant then vowel;  tag 'V' (0x56) -> vowel then consonant.
    # (Validated on debug: (0,0,'C')->B,A=BA; (0,2,'C')->B,I=BI; (1,5,'C')->C,Y=CY.)
    def resolve_key(self, key: Tuple[int, int, int]) -> Tuple[Tuple[str, str], Tuple[str, str]]:
        a, b, tag = key

        def vowel(i):
            return ("V", self.vowel_elements[i]) if i < len(self.vowel_elements) else ("?", "")

        def cons(i):
            return ("C", self.cons_elements[i]) if i < len(self.cons_elements) else ("?", "")

        if tag == 0x56:  # 'V' -> vowel, consonant
            return vowel(a), cons(b)
        else:            # 'C' -> consonant, vowel
            return cons(a), vowel(b)


def expand_special(elem: str, clusters: List[str]) -> str:
    """Expand EBoN's internal special-letter codes back to real letters.

    EBoN marks special letters before splitting (Doc/3 step 1):
      * a *soft consonant* (a consonant followed by H, e.g. TH/DH/SH) is stored
        as that consonant in **lowercase** -> expand X -> XH;
      * a *custom SPCCON cluster* (e.g. SS, PH) is stored as a **digit** 0-9 ->
        expand to clusters[digit].
    Clusters may themselves contain soft (lowercase) letters, so we expand
    digits first, then soft consonants, in a single left-to-right pass.
    Lowercase y/u are NOT soft: they mark the semivowel treated as a consonant
    (the y:/u: GENOPT modes) and expand to the bare letter.
    """
    if not elem:
        return elem
    # Pass 1: digits -> their cluster strings.
    if any(c.isdigit() for c in elem):
        elem = "".join(clusters[int(c)] if (c.isdigit() and int(c) < len(clusters)) else c
                        for c in elem)
    # Pass 2: semivowel consonants y/u -> bare letter; other lowercase (soft
    # consonants) -> uppercase + H.
    if any(c.islower() for c in elem):
        elem = "".join(c.upper() if c in "yu" else (c.upper() + "H" if c.islower() else c)
                       for c in elem)
    return elem


def structure_pattern(num):
    """EBoN structure number -> tuple of 'C'/'V'.

    n even -> starts with C, n odd -> starts with V; element count = n//2 + 2.
    (Validated for 0..12; covers all real chapters.)
    """
    try:
        n = int(num)
    except (ValueError, TypeError):
        return None
    if n < 0 or n > 40:
        return None
    count = n // 2 + 2
    start = "C" if n % 2 == 0 else "V"
    return tuple(start if k % 2 == 0 else ("V" if start == "C" else "C") for k in range(count))


def decode_qch(path: str) -> QchChapter:
    r = _Reader(open(path, "rb").read())
    r.p = 3  # 3-byte preamble before the magic
    ch = QchChapter()

    magic = r.cstr()
    if magic != "EBoN 3.0":
        raise ValueError(f"not an EBoN 3.0 qch (magic={magic!r})")
    ch.title = r.cstr()
    ch.line2 = r.cstr()
    ch.line3 = r.cstr()
    ch.line4 = r.cstr()
    ch.author = r.cstr()

    ch.flags = r.u8()
    ch.fit = r.u8()
    ch.val = r.u8()
    r.u8(); r.u8(); r.u8()  # opt3, opt4, opt5 (y/u/punct modes — not needed here)
    # Flag bits validated against the five known .ebn GENOPT strings:
    # bit2 is SHUFFLE (not prefix as the writer notes first guessed) — which is
    # also why shuffled chapters collapse all medial M1/M2 use into column 1.
    ch.structgen = bool(ch.flags & 1)
    ch.statgen = bool(ch.flags & 2)
    ch.shuffle = bool(ch.flags & 4)
    ch.prefix_opt = bool(ch.flags & 8)
    ch.suffix_opt = bool(ch.flags & 16)

    ch.consonants = r.cstr()
    r.u16()                       # f[0x3c]: prefix/suffix capacity hint (unused)
    ch.nV = r.u8()                # matrix inner dimension

    n68 = r.u8()                  # structure-label list (struct number + tag byte)
    _list68 = [(r.cstr(), r.u8()) for _ in range(n68)]

    n44 = r.u8()
    ch.vowel_elements = [r.cstr() for _ in range(n44)]
    ch.M1 = [[r.u16() for _ in range(ch.nV)] for _ in range(n44)]

    n48 = r.u16()
    ch.cons_elements = [r.cstr() for _ in range(n48)]
    ch.M2 = [[r.u16() for _ in range(ch.nV)] for _ in range(n48)]

    ne04 = r.u8()
    ch.special_clusters = [r.cstr() for _ in range(ne04)]  # SPCCON custom clusters

    nPre = r.u16()
    ch.pre_keys = [(r.u8(), r.u8(), r.u8()) for _ in range(nPre)]
    ch.pre_freq = [r.u16() for _ in range(nPre)]

    nSuf = r.u16()
    ch.suf_keys = [(r.u8(), r.u8(), r.u8()) for _ in range(nSuf)]
    ch.suf_freq = [r.u16() for _ in range(nSuf)]

    nStruct = r.u8()
    ch.struct_freq = [r.u16() for _ in range(nStruct)]
    ch.sub_counts = [r.u16() for _ in range(nStruct)]
    ch.sub_freq = [[r.u16() for _ in range(ch.sub_counts[i])] for i in range(nStruct)]
    ch.sub_labels = [[r.cstr() for _ in range(ch.sub_counts[i])] for i in range(nStruct)]

    # Fit validity masks, bit-packed LSB-first, one row per "next" index.
    # Row/column geometry from the writer (research/qch-writer-decompiled.md
    # step 36); semantics validated bit-exact against known-seed chapters.
    def mask(nrows: int, nflags: int) -> set:
        per = (nflags + 7) // 8
        pairs = set()
        for i in range(nrows):
            for k, byte in enumerate(r.raw(per)):
                while byte:
                    b = byte & -byte
                    j = k * 8 + b.bit_length() - 1
                    if j < nflags:
                        pairs.add((i, j))
                    byte ^= b
        return pairs

    n44 = len(ch.vowel_elements)
    ch.mask_cv = mask(n44, 64)    # vowel may follow consonant last-letter
    ch.mask_vc = mask(64, n44)    # consonant first-letter may follow vowel
    ch.mask_cc = mask(64, 64)     # cons first-letter after cons last-letter (skip V)
    ch.mask_vv = mask(n44, n44)   # vowel after vowel (skip C)

    # (per-suffix-entry masks + 2x127 validation tables + '#END' follow; not
    #  needed for generation, so we stop parsing here.)
    return ch


# ----------------------------------------------------------------------------- #
# Bridge into our engine's Chapter model.
# ----------------------------------------------------------------------------- #
def qch_to_chapter(path: str, fit: int | None = None):
    """Build a Chapter from a decoded .qch — at full fit fidelity.

    Everything the engine reads is reconstructed from the chapter's own data:

      * adjacency (`adj`) from the L1 validity masks — a transition exists only
        if the seeds contained it (consonants fit as single letters, Doc/3);
      * skip adjacency (`adj2`) from the L2/L3 masks, so fit 2/3 work;
      * START/END edges from M1/M2's initial/final columns, edge weights from
        their medial+final columns (EBoN's own positional frequencies);
      * prefix/suffix pools from the stored two-element keys;
      * structures from the frequency table.

    `fit` overrides the chapter's own fit level (clamped to 0..3) when given.
    """
    from .model import Chapter, GenOpts, START, END

    d = decode_qch(path)
    if fit is None:
        fit = min(max(d.fit, 0), 3)
    ch = Chapter(
        # qch metadata strings: [0]=title [1],[2]=subtitle lines [3]=author/credit.
        # ([4] is a numeric serial, not a date; EBoN does not store DATE in .qch.)
        title=d.title, line1=d.line2, line2=d.line3, author=d.line4,
        opts=GenOpts(structgen=True, statgen=True, fit=fit, val=max(1, d.val),
                     prefix=d.prefix_opt and bool(d.pre_keys),
                     suffix=d.suffix_opt and bool(d.suf_keys),
                     shuffle=d.shuffle),
    )

    # Element pools, weighted by their total positional frequency (row sum).
    # Element strings are expanded from EBoN's special-letter codes to real
    # letters (soft consonants, SPCCON clusters) so generated names read right.
    cl = d.special_clusters
    xv = [expand_special(v, cl) for v in d.vowel_elements]
    xc = [expand_special(c, cl) for c in d.cons_elements]
    for i, v in enumerate(xv):
        ch.vowel_elements[v] += max(1, sum(d.M1[i]))
    for i, c in enumerate(xc):
        ch.cons_elements[c] += max(1, sum(d.M2[i]))

    # Structures from the frequency table (index = EBoN structure number).
    for num, freq in enumerate(d.struct_freq):
        if freq <= 0:
            continue
        pat = structure_pattern(num)
        if pat:
            ch.structures[pat] += freq

    # Positional weights: column 0 = name-initial, column nV-1 = name-final,
    # the rest medial. An element's edge weight is its non-initial use, so
    # initial-only elements are reachable only through START/prefix.
    li = LETTER_INDEX
    v_mid = [sum(row[1:]) for row in d.M1]
    c_mid = [sum(row[1:]) for row in d.M2]

    # START/END sentinels straight from the positional columns: every element
    # that ever began a seed name may begin one (weight = how often), and only
    # elements that ended one satisfy the generator's is_last check.
    for elems, M in ((xv, d.M1), (xc, d.M2)):
        for i, e in enumerate(elems):
            if M[i][0]:
                ch.adj.setdefault(START, Counter())[e] += M[i][0]
            if M[i][d.nV - 1]:
                ch.adj.setdefault(e, Counter())[END] += M[i][d.nV - 1]

    # L1 adjacency from the validity masks (indexed [next][prev]; consonant
    # clusters key by their boundary letter facing the transition).
    for j, v in enumerate(xv):
        for i, c in enumerate(xc):
            raw = d.cons_elements[i]
            if c_mid[i] and (li.get(raw[0]), j) in d.mask_vc:
                ch.adj.setdefault(v, Counter())[c] += c_mid[i]
            if v_mid[j] and (j, li.get(raw[-1])) in d.mask_cv:
                ch.adj.setdefault(c, Counter())[v] += v_mid[j]

    # L2/L3 skip adjacency -> adj2, which fit 2/3 and the back-off engine read.
    for i, c1 in enumerate(xc):
        last = li.get(d.cons_elements[i][-1])
        for k, c2 in enumerate(xc):
            if c_mid[k] and (li.get(d.cons_elements[k][0]), last) in d.mask_cc:
                ch.adj2.setdefault(c1, Counter())[c2] += c_mid[k]
    for j, v1 in enumerate(xv):
        for k, v2 in enumerate(xv):
            if v_mid[k] and (k, j) in d.mask_vv:
                ch.adj2.setdefault(v1, Counter())[v2] += v_mid[k]

    # Prefix/suffix pools: authentic two-element openers/closers.
    for key, freq in zip(d.pre_keys, d.pre_freq):
        (_ca, ea), (_cb, eb) = d.resolve_key(key)
        if ea and eb:
            ch.prefixes[(expand_special(ea, cl), expand_special(eb, cl))] += max(1, freq)
    for key, freq in zip(d.suf_keys, d.suf_freq):
        (_ca, ea), (_cb, eb) = d.resolve_key(key)
        if ea and eb:
            ch.suffixes[(expand_special(ea, cl), expand_special(eb, cl))] += max(1, freq)

    return ch, d
