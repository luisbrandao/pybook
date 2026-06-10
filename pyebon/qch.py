"""Strategy B: decode EBoN's compiled .qch (Quick Chapter) binary files.

The .qch is the preprocessed form of a chapter. The original seed names are not
stored, but the generation model is. This decoder extracts the fields we can
read with confidence (validated against known-seed chapters debug/Luis/klingon):
metadata, GENOPT, the consonant alphabet, the structure list, and the vowelic
element inventory. The frequency / adjacency matrices are not fully decoded yet
(see Doc/qch-format-notes.md) and are returned as a raw tail for further work.

Format: little-endian, NUL-terminated latin-1 strings.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass, field
from typing import List, Optional

VOWEL_LETTERS = set("AEIOUYÄËÏÖÜŸÁÉÍÓÚÝÂÊÎÔÛÀÈÌÒÙÃÕÅÆØŒ'")


@dataclass
class QchInfo:
    title: str = ""
    line1: str = ""
    line2: str = ""
    author: str = ""
    date: str = ""
    flags: int = 0
    fit: int = 0
    val: int = 0
    structgen: bool = False
    statgen: bool = False
    shuffle: bool = False
    prefix: bool = False
    suffix: bool = False
    consonants: str = ""
    structures: List[str] = field(default_factory=list)   # structure numbers as strings
    vowel_elements: List[str] = field(default_factory=list)
    tail_offset: int = 0  # where the undecoded matrix region begins


def _cstr(buf, pos):
    end = buf.index(b"\x00", pos)
    return buf[pos:end].decode("latin-1"), end + 1


def structure_pattern(num: str):
    """EBoN structure number -> tuple of 'C'/'V'.

    n even -> starts with C, n odd -> starts with V; element count = n//2 + 2.
    (Validated for 0..12; covers all real chapters.)
    """
    try:
        n = int(num)
    except ValueError:
        return None
    if n < 0 or n > 40:
        return None
    count = n // 2 + 2
    start = "C" if n % 2 == 0 else "V"
    return tuple(start if k % 2 == 0 else ("V" if start == "C" else "C") for k in range(count))


def decode_qch(path: str) -> QchInfo:
    buf = open(path, "rb").read()
    info = QchInfo()

    pos = 3  # skip byte0 + hdr_u16
    magic, pos = _cstr(buf, pos)
    if magic != "EBoN 3.0":
        raise ValueError(f"not an EBoN 3.0 qch (magic={magic!r})")
    info.title, pos = _cstr(buf, pos)
    info.line1, pos = _cstr(buf, pos)
    info.line2, pos = _cstr(buf, pos)
    info.author, pos = _cstr(buf, pos)
    info.date, pos = _cstr(buf, pos)

    # GENOPT block: flags, fit, val, then 3 bytes.
    info.flags = buf[pos]
    info.fit = buf[pos + 1]
    info.val = buf[pos + 2]
    info.structgen = bool(info.flags & 1)
    info.statgen = bool(info.flags & 2)
    info.shuffle = bool(info.flags & 4)
    info.prefix = bool(info.flags & 8)
    info.suffix = bool(info.flags & 16)
    pos += 6

    # Consonant alphabet (NUL-terminated).
    info.consonants, pos = _cstr(buf, pos)

    # Structure list + vowelic element list. The records use short NUL-terminated
    # strings: all-digit strings are structure numbers; all-vowel strings are
    # vowel elements. We scan tokens, classifying by content, until the vowel
    # list ends in an empty string (double NUL).
    structures: List[str] = []
    vowels: List[str] = []
    seen_vowel = False
    i = pos
    while i < len(buf):
        # A token is the byte(s) up to the next NUL; but records are interleaved
        # with small count/freq bytes. We look for printable ASCII tokens.
        b = buf[i]
        if b == 0:
            if seen_vowel:
                break  # empty string terminates the vowel list
            i += 1
            continue
        if 0x21 <= b <= 0x7e:
            tok, ni = _cstr(buf, i)
            if tok.isdigit():
                structures.append(tok)
                i = ni
                continue
            if tok and all(c in VOWEL_LETTERS for c in tok):
                vowels.append(tok)
                seen_vowel = True
                i = ni
                continue
            # printable but neither -> likely a count byte coinciding with ASCII
            i += 1
        else:
            i += 1

    info.structures = structures
    info.vowel_elements = vowels
    info.tail_offset = i
    return info


# Vowel letters for separating consonant letters out of the alphabet field.
_VOWEL_LETTERS = set("AEIOUYÄËÏÖÜŸÁÉÍÓÚÝÂÊÎÔÛÀÈÌÒÙÃÕÅÆØŒ'")


def qch_to_chapter(path: str, fit: int = 0):
    """Bridge a decoded .qch into our Chapter model so it can generate.

    NOTE: the fit/adjacency matrices are not decoded yet, so this builds a
    model with the real vowel-element inventory, consonant letters, and
    structures, but NO adjacency. It therefore only supports fit:0 generation
    (rougher than EBoN's fit:3). Full-quality locked-chapter generation needs
    the matrix region cracked (see Doc/qch-format-notes.md).
    """
    from .model import Chapter, GenOpts

    d = decode_qch(path)
    ch = Chapter(
        title=d.title, line1=d.line1, line2=d.line2, author=d.author, date=d.date,
        opts=GenOpts(structgen=True, statgen=False, fit=min(fit, 0), val=1),
    )
    for v in d.vowel_elements:
        ch.vowel_elements[v] += 1
    for c in d.consonants:
        if c not in _VOWEL_LETTERS:
            ch.cons_elements[c] += 1
    for s in d.structures:
        pat = structure_pattern(s)
        if pat:
            ch.structures[pat] += 1
    return ch, d
