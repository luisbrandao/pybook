"""pyebon — a from-scratch reimplementation of the Everchanging Book of Names.

Inspired by EBoN 3.0 (Sami Pyörre, 1998-2000). This is not a clone: it borrows
the algorithm (vowelic/consonantal element splitting, fit-level adjacency,
structures, prefix/suffix pools, frequency-weighted generation) described in the
original help files (see Doc/3-WritingChapters.txt) and reproduces the *behavior*,
storing chapter data in our own format rather than EBoN's binary one.

Two front-ends populate the same internal Chapter model:
  * preprocess.py  -- builds a Chapter from a list of seed names (strategy A)
  * qch.py         -- decodes EBoN's compiled .qch quick-chapters (strategy B)
"""

from .model import Chapter, GenOpts
from .preprocess import build_chapter
from .generate import Generator

__all__ = ["Chapter", "GenOpts", "build_chapter", "Generator"]
