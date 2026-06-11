"""CLI: generate names from a chapter.

    python -m pyebon <chapter.ebn> [-n COUNT] [-m MIN] [-x MAX] [-s SEED]

Accepts a plaintext .ebn file (strategy A). .qch support is added separately.
"""

import argparse
import sys

from .ebn import load_ebn
from .generate import Generator, GenerationError


def main(argv=None):
    p = argparse.ArgumentParser(prog="pyebon", description="Everchanging Book of Names (reimplementation).")
    p.add_argument("chapter", help="path to a .ebn chapter file")
    p.add_argument("-n", "--count", type=int, default=20, help="how many names (default 20)")
    p.add_argument("-m", "--min", dest="min_len", type=int, default=2)
    p.add_argument("-x", "--max", dest="max_len", type=int, default=30)
    p.add_argument("-s", "--seed", type=int, default=None)
    p.add_argument("--info", action="store_true", help="print chapter info and exit")
    args = p.parse_args(argv)

    # .qch (compiled, incl. locked chapters) or .ebn (plaintext seeds).
    if args.chapter.lower().endswith(".qch"):
        from .qch import qch_to_chapter
        ch, _ = qch_to_chapter(args.chapter, fit=1)
        print("(note: .qch chapters use real elements/structures/prefix+suffix; "
              "EBoN's exact fit matrices are not yet replicated, and special "
              "letters are not yet expanded)", file=sys.stderr)
    else:
        ch = load_ebn(args.chapter)

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
