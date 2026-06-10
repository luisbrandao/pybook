"""Split names into alternating vowelic / consonantal elements (Doc/3, step 2).

An element is a maximal run of letters of one category. Example (no special
letters): THRANDUIL -> ['TH','R'?...]; the original EBoN marks soft consonants
(TH) as a single lowercase letter first, giving TH->t, so THRANDUIL -> tR A ND UI L
== elements ['tR','A','ND','UI','L'], structure C V C V C.

We currently implement the plain split (no soft-consonant marking yet); soft
consonants are a documented extension point (see mark_special).
"""

from __future__ import annotations

from typing import List, Tuple

# Vowels per Doc/3 (consonant/vowel character classes). Y defaults to vowel.
VOWELS = set("AEIOUYÄËÏÖÜŸÁÉÍÓÚÝÂÊÎÔÛÀÈÌÒÙÃÕÅÆØŒ'")
# Note: apostrophe is grouped with vowels by EBoN (used in Klingon etc.).


def is_vowel(ch: str) -> bool:
    return ch in VOWELS


def mark_special(name: str) -> str:
    """Hook for SPCCON 'soft' handling (TH->t, etc.). Not yet implemented;
    returns the name unchanged so the rest of the pipeline is wired up."""
    return name


def split_elements(name: str) -> List[Tuple[str, str]]:
    """Return a list of (element, category) where category is 'V' or 'C'.

    Categories alternate. Each element is a maximal same-category run.
    """
    name = mark_special(name.upper())
    out: List[Tuple[str, str]] = []
    i = 0
    n = len(name)
    while i < n:
        cat = "V" if is_vowel(name[i]) else "C"
        j = i
        while j < n and (("V" if is_vowel(name[j]) else "C") == cat):
            j += 1
        out.append((name[i:j], cat))
        i = j
    return out


def structure_of(elements: List[Tuple[str, str]]) -> Tuple[str, ...]:
    """The C/V structure pattern, one entry per element."""
    return tuple(cat for _, cat in elements)
