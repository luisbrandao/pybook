"""Internal chapter model — our own format, shared by both front-ends.

A Chapter holds everything the generator needs, derived either from seed names
(preprocess.py) or decoded from a .qch (qch.py):

  * the element inventory, split into vowelic and consonantal,
  * a frequency-weighted adjacency graph over elements, with START/END sentinels
    that mark which elements may begin or end a name,
  * the set of name structures (C/V patterns) with frequencies,
  * optional prefix/suffix pools (two-element openers/closers),
  * the generation options (fit level, statgen, structgen, shuffle, ...).

The adjacency graph is the heart of "fit": an edge a->b means element b was seen
immediately after element a in some seed name. START->x means x began a name;
x->END means x ended one.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# Sentinel nodes for the adjacency graph.
START = "\x02"  # marks "beginning of name"
END = "\x03"    # marks "end of name"


@dataclass
class GenOpts:
    """Generation options, mirroring EBoN's GENOPT tag."""
    structgen: bool = True   # generate using structures collected from seeds
    statgen: bool = True     # weight choices by frequency of appearance
    fit: int = 3             # fitting level 0..3 (adjacency strictness)
    val: int = 2             # validation level 0..2
    prefix: bool = False     # draw first two elements from the prefix pool
    suffix: bool = False     # draw last two elements from the suffix pool
    shuffle: bool = False    # pool elements globally instead of by position

    @classmethod
    def parse(cls, genopt: str) -> "GenOpts":
        """Parse a GENOPT string like 'structgen, statgen, fit:3, val:2, suffix'."""
        o = cls(structgen=False, statgen=False, fit=3, val=2)
        seen_struct = seen_stat = False
        for tok in genopt.replace("\n", " ").split(","):
            tok = tok.strip().lower()
            if not tok:
                continue
            if tok == "structgen":
                o.structgen = True; seen_struct = True
            elif tok == "statgen":
                o.statgen = True; seen_stat = True
            elif tok == "shuffle":
                o.shuffle = True
            elif tok == "prefix":
                o.prefix = True
            elif tok == "suffix":
                o.suffix = True
            elif tok.startswith("fit:"):
                o.fit = int(tok[4:])
            elif tok.startswith("val:"):
                o.val = int(tok[4:])
            # y:/u:/punct: handled by preprocessing, ignored here
        # EBoN defaults to on when the token is simply present/absent in practice;
        # but an explicit GENOPT lists what it wants, so keep what we parsed.
        return o


@dataclass
class Chapter:
    title: str = ""
    line1: str = ""
    line2: str = ""
    author: str = ""
    date: str = ""
    opts: GenOpts = field(default_factory=GenOpts)

    # Element inventories (uppercase strings; soft consonants kept lowercase).
    vowel_elements: Counter = field(default_factory=Counter)
    cons_elements: Counter = field(default_factory=Counter)

    # Frequency-weighted adjacency: adj[a] is a Counter of elements that
    # followed a. Keys/values include START and END sentinels.
    adj: Dict[str, Counter] = field(default_factory=dict)

    # Distance-2 ("skip") adjacency: adj2[a] counts elements seen two positions
    # after a (same category, since categories alternate). This is what EBoN's
    # fit levels 2/3 check: consonant-skip-vowel (C..C) and vowel-skip-consonant
    # (V..V). Populated by the seed preprocessor; empty for .qch-derived chapters.
    adj2: Dict[str, Counter] = field(default_factory=dict)

    # Structures as tuples of 'C'/'V' (one entry per element), with frequency.
    structures: Counter = field(default_factory=Counter)

    # Prefix/suffix pools: (elem1, elem2) openers / closers, with frequency.
    prefixes: Counter = field(default_factory=Counter)
    suffixes: Counter = field(default_factory=Counter)

    def add_edge(self, a: str, b: str) -> None:
        self.adj.setdefault(a, Counter())[b] += 1

    def add_edge2(self, a: str, b: str) -> None:
        self.adj2.setdefault(a, Counter())[b] += 1

    # --- serialization (our own JSON library format) --------------------- #
    def to_dict(self) -> dict:
        """A JSON-ready dict capturing everything the generator needs."""
        return {
            "title": self.title, "line1": self.line1, "line2": self.line2,
            "author": self.author, "date": self.date,
            "opts": {
                "structgen": self.opts.structgen, "statgen": self.opts.statgen,
                "fit": self.opts.fit, "val": self.opts.val,
                "prefix": self.opts.prefix, "suffix": self.opts.suffix,
                "shuffle": self.opts.shuffle,
            },
            "vowel_elements": dict(self.vowel_elements),
            "cons_elements": dict(self.cons_elements),
            # adjacency as {a: {b: count}}
            "adj": {a: dict(succ) for a, succ in self.adj.items()},
            "adj2": {a: dict(succ) for a, succ in self.adj2.items()},
            # tuple-keyed counters as [[items...], count] pairs
            "structures": [[list(k), v] for k, v in self.structures.items()],
            "prefixes": [[list(k), v] for k, v in self.prefixes.items()],
            "suffixes": [[list(k), v] for k, v in self.suffixes.items()],
        }

    @classmethod
    def from_dict(cls, d: dict) -> "Chapter":
        o = d.get("opts", {})
        ch = cls(
            title=d.get("title", ""), line1=d.get("line1", ""),
            line2=d.get("line2", ""), author=d.get("author", ""),
            date=d.get("date", ""),
            opts=GenOpts(
                structgen=o.get("structgen", True), statgen=o.get("statgen", True),
                fit=o.get("fit", 3), val=o.get("val", 2),
                prefix=o.get("prefix", False), suffix=o.get("suffix", False),
                shuffle=o.get("shuffle", False),
            ),
        )
        ch.vowel_elements = Counter(d.get("vowel_elements", {}))
        ch.cons_elements = Counter(d.get("cons_elements", {}))
        ch.adj = {a: Counter(succ) for a, succ in d.get("adj", {}).items()}
        ch.adj2 = {a: Counter(succ) for a, succ in d.get("adj2", {}).items()}
        ch.structures = Counter({tuple(k): v for k, v in d.get("structures", [])})
        ch.prefixes = Counter({tuple(k): v for k, v in d.get("prefixes", [])})
        ch.suffixes = Counter({tuple(k): v for k, v in d.get("suffixes", [])})
        return ch

    def successors(self, a: str) -> Counter:
        return self.adj.get(a, Counter())

    def successors2(self, a: str) -> Counter:
        return self.adj2.get(a, Counter())

    @staticmethod
    def is_vowel_element(elem: str) -> bool:
        """An element's category is fixed at split time; we tag by sentinel-free
        lookup elsewhere, but for convenience callers may pass category in."""
        raise NotImplementedError  # category is tracked by the caller, see generate.py
