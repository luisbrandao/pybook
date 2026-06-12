"""CLI: generate names from a chapter.

    python -m pyebon <chapter> [-n COUNT] [-m MIN] [-x MAX] [-s SEED]

`<chapter>` may be:
  * a library chapter name (e.g. `core_QUENYA`) — reads data/library/<name>.json,
  * a path to one of our `.json` library files,
  * a plaintext `.ebn` seed file (strategy A), or
  * an EBoN compiled `.qch` file (strategy B).
Run `python -m pyebon.library extract` once to build the data/library/ folder.
"""

import argparse
import os
import sys

from .ebn import load_ebn
from .generate import Generator, GenerationError
from .library import LIBRARY_DIR, load_chapter, find_chapter


def main(argv=None):
    p = argparse.ArgumentParser(prog="pyebon", description="Everchanging Book of Names (reimplementation).")
    p.add_argument("chapter", help="library chapter name, or path to a .json/.ebn/.qch file")
    p.add_argument("-n", "--count", type=int, default=35, help="how many names (default 35)")
    p.add_argument("-m", "--min", dest="min_len", type=int, default=2)
    p.add_argument("-x", "--max", dest="max_len", type=int, default=30)
    p.add_argument("-s", "--seed", type=int, default=None)
    p.add_argument("--info", action="store_true", help="print chapter info and exit")
    args = p.parse_args(argv)

    chapter = args.chapter
    lib_candidate = find_chapter(chapter)
    if chapter.lower().endswith(".json"):
        ch = load_chapter(chapter)
    elif lib_candidate:
        ch = load_chapter(lib_candidate)             # library name (book/chapter or bare)
    elif chapter.lower().endswith(".qch"):
        from .qch import qch_to_chapter
        ch, _ = qch_to_chapter(chapter, fit=1)
    elif chapter.lower().endswith(".txt"):
        from .library import compile_seed
        ch = compile_seed(chapter)   # cached build; rebuilds when the .txt changes
    else:
        ch = load_ebn(chapter)

    if args.info:
        print(f"{ch.title} — {ch.line1} {ch.line2} (by {ch.author})")
        print(f"opts: {ch.opts}")
        print(f"{len(ch.vowel_elements)} vowel elements, {len(ch.cons_elements)} consonant elements, "
              f"{len(ch.structures)} structures")
        return 0

    g = Generator(ch, seed=args.seed)
    for _ in range(args.count):
        try:
            print(g.generate(args.min_len, args.max_len))
        except GenerationError as e:
            print(f"(error: {e})", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
