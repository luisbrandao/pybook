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


def valid_name(name: str, val: int) -> bool:
    """Shared validation (used by both generators).

    !REP (Doc/3): reject a name that is *entirely* a repeated cycle, e.g.
    RONDROND (ROND x2) or ABABAB (AB x3) -- but NOT BABABI, which EBoN accepts
    at val:1, so we only reject when the whole string tiles one shorter unit.
    """
    if val <= 0:
        return True
    n = len(name)
    for clen in range(1, n // 2 + 1):
        if n % clen == 0 and name == name[:clen] * (n // clen):
            return False
    return True


def titlecase(raw: str) -> str:
    """Only the first letter uppercase (Doc/3, postprocess)."""
    return raw[:1].upper() + raw[1:].lower()


def make_generator(chapter: "Chapter", method: str = "classic",
                   seed: Optional[int] = None, temperature: float = 1.0):
    """Return the generator for `method`: 'classic' (the EBoN-style fit walk) or
    'backoff'/'smart' (the variable-order back-off model in backoff.py)."""
    if method in ("backoff", "smart"):
        from .backoff import BackoffGenerator
        return BackoffGenerator(chapter, seed=seed, temperature=temperature)
    return Generator(chapter, seed=seed)


class Generator:
    def __init__(self, chapter: Chapter, seed: Optional[int] = None):
        self.ch = chapter
        self.rng = random.Random(seed)
        # Skip-level (fit 2/3) checks only apply when the chapter actually has
        # distance-2 data; .qch-derived chapters don't, so they stay at fit:1.
        self.has_adj2 = bool(getattr(chapter, "adj2", None))

    # --- helpers ---------------------------------------------------------- #
    def _pool(self, cat: str):
        return self.ch.vowel_elements if cat == "V" else self.ch.cons_elements

    def _cat(self, elem: str) -> str:
        return "V" if elem in self.ch.vowel_elements else "C"

    def _weighted_pick(self, items: List[str], weights: List[float]) -> str:
        return self.rng.choices(items, weights=weights, k=1)[0]

    def _skip_required(self, cat: str) -> bool:
        """Does the current fit level enforce distance-2 adjacency for `cat`?

        fit:2 = consonant-skip-vowel (check when placing a consonant);
        fit:3 = also vowel-skip-consonant (check when placing a vowel).
        """
        if not self.has_adj2:
            return False
        opts = self.ch.opts
        return (opts.fit >= 2 and cat == "C") or (opts.fit >= 3 and cat == "V")

    def _candidates(self, prev: str, prev2: Optional[str], cat: str,
                    is_last: bool) -> List[Tuple[str, float]]:
        """Elements of `cat` that may follow `prev` (two back: `prev2`)."""
        opts = self.ch.opts
        pool = self._pool(cat)
        out: List[Tuple[str, float]] = []
        succ = self.ch.successors(prev)
        succ2 = self.ch.successors2(prev2) if prev2 is not None else None
        skip = self._skip_required(cat) and prev2 is not None
        for elem, freq in pool.items():
            if opts.fit >= 1:
                edge = succ.get(elem, 0)
                if edge == 0:
                    continue
                # Last slot must be able to end a name.
                if is_last and self.ch.successors(elem).get(END, 0) == 0:
                    continue
                # fit 2/3: the element two back must also have been a skip-neighbor.
                if skip and succ2.get(elem, 0) == 0:
                    continue
                weight = edge if opts.statgen else 1.0
            else:
                weight = freq if opts.statgen else 1.0
            out.append((elem, float(weight)))
        return out

    def _pick_pair(self, pool, cats: Tuple[str, str]):
        """Pick a (e1, e2) pair from a prefix/suffix pool matching `cats`."""
        opts = self.ch.opts
        items = [(p, c) for p, c in pool.items()
                 if (self._cat(p[0]), self._cat(p[1])) == cats]
        if not items:
            return None
        pairs = [p for p, _ in items]
        weights = [float(c) if opts.statgen else 1.0 for _, c in items]
        return self.rng.choices(pairs, weights=weights, k=1)[0]

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
    def _pins(self, structure: Tuple[str, ...]):
        """Forced slots from the prefix/suffix pools (or None if unsatisfiable).

        Returns (pins, pair_internal): `pins` maps slot index -> element; slots
        in `pair_internal` get their incoming adjacency for free (they are the
        second element of a real pool pair, or the START opener).
        """
        opts = self.ch.opts
        n = len(structure)
        pins, pair_internal = {}, set()
        if opts.prefix and n >= 2 and self.ch.prefixes:
            pair = self._pick_pair(self.ch.prefixes, (structure[0], structure[1]))
            if pair is None:
                return None
            pins[0], pins[1] = pair
            pair_internal.update({0, 1})
        if opts.suffix and n >= 2 and self.ch.suffixes:
            pair = self._pick_pair(self.ch.suffixes, (structure[-2], structure[-1]))
            if pair is None:
                return None
            # Reconcile with any prefix pins that overlap (short structures).
            if (n - 2 in pins and pins[n - 2] != pair[0]) or \
               (n - 1 in pins and pins[n - 1] != pair[1]):
                return None
            pins[n - 2], pins[n - 1] = pair
            pair_internal.add(n - 1)  # the seam INTO n-2 is still checked
        return pins, pair_internal

    def _walk(self, structure: Tuple[str, ...]) -> Optional[List[str]]:
        """Randomized DFS filling each slot; returns element list or None."""
        n = len(structure)
        pinned = self._pins(structure)
        if pinned is None:
            return None  # prefix/suffix required but no matching pair this structure
        pins, pair_internal = pinned
        result: List[str] = []

        def dfs(i: int) -> bool:
            if i == n:
                return True
            prev = result[i - 1] if i >= 1 else START
            prev2 = result[i - 2] if i >= 2 else None  # None until a real 2-back elem
            cat = structure[i]
            is_last = i == n - 1
            if i in pins:
                elem = pins[i]
                # Check the incoming seam unless this slot is guaranteed valid
                # (slot 0 opener, or the second element of its own pool pair).
                if self.ch.opts.fit >= 1 and i != 0 and i not in pair_internal:
                    if self.ch.successors(prev).get(elem, 0) == 0:
                        return False
                    if self._skip_required(cat) and prev2 is not None \
                            and self.ch.successors2(prev2).get(elem, 0) == 0:
                        return False
                result.append(elem)
                if dfs(i + 1):
                    return True
                result.pop()
                return False

            cands = self._candidates(prev, prev2, cat, is_last)
            if not cands:
                return False
            pool_items = [c for c, _ in cands]
            pool_w = [w for _, w in cands]
            order: List[str] = []
            while pool_items:
                pick = self._weighted_pick(pool_items, pool_w)
                idx = pool_items.index(pick)
                pool_items.pop(idx); pool_w.pop(idx)
                order.append(pick)
            for elem in order:
                result.append(elem)
                if dfs(i + 1):
                    return True
                result.pop()
            return False

        return result if dfs(0) else None

    # --- validation ------------------------------------------------------- #
    def _valid(self, name: str) -> bool:
        return valid_name(name, self.ch.opts.val)

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
        return titlecase(raw)
