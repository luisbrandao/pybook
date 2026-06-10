"""Generate names from a Chapter model.

Core idea (matches EBoN behavior, validated against the debug chapter): choose a
structure, then fill its element slots by a frequency-weighted random walk over
the adjacency graph, with backtracking. The START/END sentinels ensure names
begin and end the way seed names did; the `fit` level controls how strictly
adjacency is enforced.
"""

from __future__ import annotations

import random
from typing import List, Optional, Tuple

from .model import Chapter, START, END


class GenerationError(RuntimeError):
    pass


class Generator:
    def __init__(self, chapter: Chapter, seed: Optional[int] = None):
        self.ch = chapter
        self.rng = random.Random(seed)

    # --- helpers ---------------------------------------------------------- #
    def _pool(self, cat: str):
        return self.ch.vowel_elements if cat == "V" else self.ch.cons_elements

    def _weighted_pick(self, items: List[str], weights: List[float]) -> str:
        return self.rng.choices(items, weights=weights, k=1)[0]

    def _candidates(self, prev: str, cat: str, is_last: bool) -> List[Tuple[str, float]]:
        """Elements of `cat` that may follow `prev`, with weights."""
        opts = self.ch.opts
        pool = self._pool(cat)
        out: List[Tuple[str, float]] = []
        succ = self.ch.successors(prev)
        for elem, freq in pool.items():
            if opts.fit >= 1:
                edge = succ.get(elem, 0)
                if edge == 0:
                    continue
                # Last slot must be able to end a name.
                if is_last and self.ch.successors(elem).get(END, 0) == 0:
                    continue
                weight = edge if opts.statgen else 1.0
            else:
                if is_last and opts.fit >= 1:
                    pass
                weight = freq if opts.statgen else 1.0
            out.append((elem, float(weight)))
        return out

    # --- structure selection --------------------------------------------- #
    def _pick_structure(self) -> Tuple[str, ...]:
        opts = self.ch.opts
        structs = list(self.ch.structures.keys())
        if not structs:
            raise GenerationError("chapter has no structures")
        if opts.structgen:
            weights = [self.ch.structures[s] if opts.statgen else 1 for s in structs]
            return self._weighted_pick(structs, [float(w) for w in weights])
        return self.rng.choice(structs)

    # --- the walk --------------------------------------------------------- #
    def _walk(self, structure: Tuple[str, ...]) -> Optional[List[str]]:
        """Randomized DFS filling each slot; returns element list or None."""
        n = len(structure)
        result: List[str] = []

        def dfs(i: int, prev: str) -> bool:
            if i == n:
                # At fit 0 we still want a sensible ending; otherwise the
                # adjacency check already guaranteed an END-capable last elem.
                return True
            cat = structure[i]
            is_last = i == n - 1
            cands = self._candidates(prev, cat, is_last)
            if not cands:
                return False
            items = [c for c, _ in cands]
            weights = [w for _, w in cands]
            # Try candidates in weighted-random order, backtracking on dead ends.
            order: List[str] = []
            pool_items, pool_w = items[:], weights[:]
            while pool_items:
                pick = self._weighted_pick(pool_items, pool_w)
                idx = pool_items.index(pick)
                pool_items.pop(idx); pool_w.pop(idx)
                order.append(pick)
            for elem in order:
                result.append(elem)
                if dfs(i + 1, elem):
                    return True
                result.pop()
            return False

        return result if dfs(0, START) else None

    # --- validation ------------------------------------------------------- #
    def _valid(self, name: str) -> bool:
        opts = self.ch.opts
        if opts.val <= 0:
            return True
        # !REP (Doc/3): reject a name that is *entirely* a repeated cycle, e.g.
        # RONDROND (ROND x2) or ABABAB (AB x3). Note this must NOT fire on
        # BABABI -- EBoN accepts that at val:1 -- so we only reject when the
        # whole string is an exact tiling of one shorter unit.
        n = len(name)
        for clen in range(1, n // 2 + 1):
            if n % clen == 0 and name == name[:clen] * (n // clen):
                return False
        return True

    # --- public API ------------------------------------------------------- #
    def generate(self, min_len: int = 2, max_len: int = 30, tries: int = 2000) -> str:
        for _ in range(tries):
            structure = self._pick_structure()
            elems = self._walk(structure)
            if not elems:
                continue
            raw = "".join(elems)
            if not (min_len <= len(raw) <= max_len):
                continue
            if not self._valid(raw):
                continue
            return self._postprocess(raw)
        raise GenerationError("could not generate a name within the given bounds")

    def _postprocess(self, raw: str) -> str:
        """Titlecase: only the first letter uppercase (Doc/3, postprocess)."""
        return raw[:1].upper() + raw[1:].lower()
