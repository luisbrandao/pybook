"""Variable-order back-off generation -- a 'smarter' alternative to the
fit-level walk in generate.py.

Instead of EBoN's structure templates + fit levels, this models a name as a
sequence of elements and, at each step, predicts the next element from the
*longest* run of preceding elements the chapter has actually seen, backing off
to a shorter context when the long one is unknown (stupid-backoff). Two
consequences fall out for free:

  * element categories alternate by construction, so the walk never has to be
    told "vowel here, consonant there" -- phonotactic alternation is inherent;
  * name length is decided by the model itself (it emits an END token), not by
    a pre-chosen structure -- so lengths follow the source distribution.

A `temperature` knob trades typicality for novelty: <1 sharpens toward common
choices (safe, repetitive), 1 samples in proportion to the data, >1 flattens
toward rarer choices (varied, wilder).

When a chapter carries no stored higher-order data, an order-2 distribution is
synthesized on the fly from the skip adjacency (`adj2`) when present -- the
next element must follow the previous one (`adj`) AND be a seen skip-neighbor
of the one before that, which is exactly what the fit:2/3 walk enforces. The
.qch-derived library books carry mask-derived adj/adj2, so they get real
order-2 behavior; with no adj2 either, the model degrades to order 1.
"""

from __future__ import annotations

import random
from collections import Counter
from typing import List, Optional

from .model import Chapter, START, END, MAX_ORDER
from .generate import GenerationError, valid_name, titlecase


class BackoffGenerator:
    def __init__(self, chapter: Chapter, seed: Optional[int] = None,
                 temperature: float = 1.0, max_order: int = MAX_ORDER):
        self.ch = chapter
        self.rng = random.Random(seed)
        self.temp = max(0.05, float(temperature))
        self.max_order = max_order

    def _dist(self, history: List[str]):
        """Next-element distribution given the elements placed so far.

        Tries the longest context (up to max_order, START-padded) and backs off
        until a seen context is found; order 1 is the adjacency graph, which is
        always present, so this returns None only at a true dead end.
        """
        full = [START] + history
        hi = min(self.max_order, len(full))
        for length in range(hi, 0, -1):
            ctx = tuple(full[-length:])
            table = self.ch.successors(ctx[0]) if length == 1 else self.ch.ngram(ctx)
            if not table and length == 2 and not self.ch.ngrams:
                table = self._synth2(ctx)
            if table:
                return table
        return None

    def _synth2(self, ctx):
        """Order-2 distribution from adj constrained by adj2 (chapters that
        store no ngrams, e.g. the .qch-derived library books): the next element
        must follow ctx[1] and be a seen skip-neighbor of ctx[0]. END passes on
        the adjacency alone (adj2 holds no sentinels)."""
        succ = self.ch.successors(ctx[1])
        skip = self.ch.successors2(ctx[0])
        if not succ or not skip:
            return None
        table = Counter({e: w for e, w in succ.items()
                         if e == END or skip.get(e, 0) > 0})
        return table or None

    def _sample(self, table):
        inv = 1.0 / self.temp
        elems = list(table.keys())
        weights = [float(c) ** inv for c in table.values()]
        return self.rng.choices(elems, weights=weights, k=1)[0]

    def _walk(self, max_elems: int = 24) -> Optional[List[str]]:
        history: List[str] = []
        for _ in range(max_elems):
            table = self._dist(history)
            if not table:
                return None
            nxt = self._sample(table)
            if nxt == END:
                return history or None
            history.append(nxt)
        return None  # ran past the cap without ending -- treat as a failed try

    def generate(self, min_len: int = 2, max_len: int = 30, tries: int = 2000) -> str:
        for _ in range(tries):
            elems = self._walk()
            if not elems:
                continue
            raw = "".join(elems)
            if not (min_len <= len(raw) <= max_len):
                continue
            if not valid_name(raw, self.ch.opts.val):
                continue
            return titlecase(raw)
        raise GenerationError("could not generate a name within the given bounds")
