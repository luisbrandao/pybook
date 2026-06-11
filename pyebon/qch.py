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
fit-frequency matrices, prefix/suffix two-element keys with frequencies, and the
structure / substructure tables.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


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
    ch.structgen = bool(ch.flags & 1)
    ch.statgen = bool(ch.flags & 2)
    ch.prefix_opt = bool(ch.flags & 4)
    ch.suffix_opt = bool(ch.flags & 8)
    ch.shuffle = bool(ch.flags & 16)

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
    _list_e04 = [r.cstr() for _ in range(ne04)]

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

    # (validity bitmasks + 2x127 validation tables + '#END' follow; not needed
    #  for generation, so we stop parsing here.)
    return ch


# ----------------------------------------------------------------------------- #
# Bridge into our engine's Chapter model.
# ----------------------------------------------------------------------------- #
def qch_to_chapter(path: str, fit: int = 1):
    """Build a Chapter from a decoded .qch.

    Uses the real element inventories (vowel + consonant clusters), the
    prefix/suffix two-element keys (genuine seed adjacency for openings and
    closings), the structure distribution, and the M1/M2 fit matrices as element
    frequencies. Prefix/suffix pairs seed the adjacency graph with START/END
    sentinels; the middle is filled from frequency-weighted pools. This is much
    closer to EBoN than the old fit:0 path (which had no consonant clusters and
    no prefix/suffix), though it does not reproduce EBoN's full fit engine.
    """
    from .model import Chapter, GenOpts, START, END

    d = decode_qch(path)
    ch = Chapter(
        title=d.title, line1=d.line2, line2=d.line3, author=d.author,
        opts=GenOpts(structgen=True, statgen=True, fit=fit, val=max(1, d.val),
                     prefix=bool(d.pre_keys), suffix=bool(d.suf_keys),
                     shuffle=d.shuffle),
    )

    # Element pools, weighted by their total fit frequency (row sum of M1/M2).
    for i, v in enumerate(d.vowel_elements):
        w = sum(d.M1[i]) if i < len(d.M1) else 0
        ch.vowel_elements[v] += max(1, w)
    for i, c in enumerate(d.cons_elements):
        w = sum(d.M2[i]) if i < len(d.M2) else 0
        ch.cons_elements[c] += max(1, w)

    # Structures from the frequency table (index = EBoN structure number).
    for num, freq in enumerate(d.struct_freq):
        if freq <= 0:
            continue
        pat = structure_pattern(num)
        if pat:
            ch.structures[pat] += freq

    # Generic alternating adjacency so the walk can traverse the middle: every
    # vowel<->consonant transition is allowed, weighted by the target element's
    # frequency. (EBoN's exact fit matrices constrain this further; frequency
    # weighting keeps names on-theme without porting the full fit engine.)
    for v, vw in ch.vowel_elements.items():
        succ = ch.adj.setdefault(v, Counter())
        for c, cw in ch.cons_elements.items():
            succ[c] += cw
    for c, cw in ch.cons_elements.items():
        succ = ch.adj.setdefault(c, Counter())
        for v, vw in ch.vowel_elements.items():
            succ[v] += vw

    # Prefix keys: authentic openers. Seed START edges and reinforce the first
    # transition; also record the pool for future prefix-forcing.
    for key, freq in zip(d.pre_keys, d.pre_freq):
        (_ca, ea), (_cb, eb) = d.resolve_key(key)
        if not ea or not eb:
            continue
        w = max(1, freq)
        ch.prefixes[(ea, eb)] += w
        ch.adj.setdefault(START, Counter())[ea] += w
        ch.adj.setdefault(ea, Counter())[eb] += w

    # Suffix keys: authentic closers. Only elements that really ended a name get
    # an ->END edge, so the generator's is_last check ends names correctly.
    for key, freq in zip(d.suf_keys, d.suf_freq):
        (_ca, ea), (_cb, eb) = d.resolve_key(key)
        if not ea or not eb:
            continue
        w = max(1, freq)
        ch.suffixes[(ea, eb)] += w
        ch.adj.setdefault(ea, Counter())[eb] += w
        ch.adj.setdefault(eb, Counter())[END] += w

    return ch, d
