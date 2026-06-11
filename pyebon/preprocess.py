"""Strategy A: build a Chapter model from a list of seed names.

This mirrors EBoN's preprocessing (Doc/3, step 3): split each seed into
elements, then gather element inventories, the frequency-weighted adjacency
graph (with START/END boundaries), structures, and prefix/suffix pools.
"""

from __future__ import annotations

from typing import List

from .model import Chapter, GenOpts, START, END
from .splitting import split_elements, structure_of


def build_chapter(names: List[str], opts: GenOpts | None = None, **meta) -> Chapter:
    ch = Chapter(opts=opts or GenOpts())
    for k, v in meta.items():
        if hasattr(ch, k):
            setattr(ch, k, v)

    for raw in names:
        raw = raw.strip()
        if not raw:
            continue
        elements = split_elements(raw)
        if len(elements) < 2:
            # EBoN rejects names that are all-vowel or all-consonant.
            continue

        keys = [e for e, _ in elements]

        # Element inventories by category.
        for elem, cat in elements:
            if cat == "V":
                ch.vowel_elements[elem] += 1
            else:
                ch.cons_elements[elem] += 1

        # Adjacency with boundary sentinels.
        ch.add_edge(START, keys[0])
        for a, b in zip(keys, keys[1:]):
            ch.add_edge(a, b)
        ch.add_edge(keys[-1], END)

        # Distance-2 (skip) adjacency for fit levels 2/3: element -> element two
        # positions later (same category, since categories alternate).
        for a, b in zip(keys, keys[2:]):
            ch.add_edge2(a, b)

        # Structure frequency.
        ch.structures[structure_of(elements)] += 1

        # Prefix / suffix pools (two-element openers / closers).
        if len(keys) >= 2:
            ch.prefixes[(keys[0], keys[1])] += 1
            ch.suffixes[(keys[-2], keys[-1])] += 1

    return ch
