"""Blend two or more chapters into one, weighted -- a feature EBoN never had.

Each source chapter is first normalized to a common mass, so a 50-name chapter
and a 50,000-name dump contribute according to their *chosen weight*, not their
raw size. The normalized counts are scaled by the weight and summed across every
field the generators read: element inventories, adjacency (order 1 and skip-2),
the back-off n-grams, structures, and the prefix/suffix pools. The result is an
ordinary Chapter, so both engines (classic fit-walk and back-off) generate from
a blend with no special handling.

Counts become floats after weighting; that is fine -- every consumer treats them
as weights (random.choices / frequency comparisons), and "edge exists" is still
"value > 0".
"""

from __future__ import annotations

import copy
from collections import Counter
from typing import List, Tuple

from .model import Chapter

# Common mass each chapter is scaled to before its weight is applied. The value
# is arbitrary (only ratios matter); 10000 keeps the blended counts comfortably
# above zero for readability when inspecting a blended chapter.
TARGET = 10000.0


def _mass(ch: Chapter) -> float:
    """A chapter's size proxy: total element occurrences (>0)."""
    return float(sum(ch.vowel_elements.values()) + sum(ch.cons_elements.values())) or 1.0


def _add(dst: Counter, src: Counter, factor: float) -> None:
    for key, val in src.items():
        dst[key] += val * factor


def blend_chapters(parts: List[Tuple[Chapter, float]], **meta) -> Chapter:
    """Blend (chapter, weight) pairs into a new Chapter. Weights need not sum to
    1 (they are normalized); non-positive weights are dropped. Extra keyword args
    set metadata on the result (title, author, ...)."""
    parts = [(ch, float(w)) for ch, w in parts if w > 0]
    if not parts:
        raise ValueError("blend needs at least one chapter with positive weight")
    total_w = sum(w for _, w in parts)
    parts = [(ch, w / total_w) for ch, w in parts]

    out = Chapter()
    # Inherit options (val level etc.) from the heaviest ingredient -- copied, so
    # later opts tweaks on the blend never mutate the cached source chapter.
    heaviest = max(parts, key=lambda p: p[1])[0]
    out.opts = copy.copy(heaviest.opts)

    for ch, weight in parts:
        factor = (TARGET / _mass(ch)) * weight
        _add(out.vowel_elements, ch.vowel_elements, factor)
        _add(out.cons_elements, ch.cons_elements, factor)
        for node, succ in ch.adj.items():
            _add(out.adj.setdefault(node, Counter()), succ, factor)
        for node, succ in ch.adj2.items():
            _add(out.adj2.setdefault(node, Counter()), succ, factor)
        for length, table in ch.ngrams.items():
            dst_table = out.ngrams.setdefault(length, {})
            for ctx, nxt in table.items():
                _add(dst_table.setdefault(ctx, Counter()), nxt, factor)
        _add(out.structures, ch.structures, factor)
        _add(out.prefixes, ch.prefixes, factor)
        _add(out.suffixes, ch.suffixes, factor)

    for key, val in meta.items():
        if hasattr(out, key):
            setattr(out, key, val)
    return out
