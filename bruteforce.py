#!/usr/bin/env python3
"""Bulk-generate names from every library chapter, one file per chapter.

Writes bruteforce/<chapter>-<book>.txt, each with up to COUNT names from the
classic (EBoN-faithful) engine. Meant for grepping a half-remembered name
across the whole library. A pool of worker processes (one per CPU) fans the
332 chapters out; spawning one OS process per chapter would oversubscribe the
cores and pay Python's startup cost 332 times for no gain.

    python3 bruteforce.py [COUNT]      # default 9999
"""
import os
import sys
from multiprocessing import Pool

from pyebon.library import list_books, list_chapters, load_chapter
from pyebon.generate import make_generator, GenerationError

OUT_DIR = "bruteforce"
COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 9999


def gen_chapter(job):
    book_id, stem, path = job
    try:
        ch = load_chapter(path)
        g = make_generator(ch, method="classic")
    except Exception as e:
        return (stem, book_id, 0, f"load error: {e}")

    names, fails = [], 0
    for _ in range(COUNT):
        try:
            names.append(g.generate(2, 30))
        except GenerationError:
            fails += 1
            if fails > 200:        # chapter is too constrained to keep going
                break

    safe_book = book_id.replace(os.sep, "_")
    fname = os.path.join(OUT_DIR, f"{stem}-{safe_book}.txt")
    with open(fname, "w", encoding="utf-8") as fh:
        fh.write("\n".join(names) + "\n")
    return (stem, book_id, len(names), None)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    jobs = []
    for book_id, _ in list_books():
        for stem, _title, path in list_chapters(book_id):
            jobs.append((book_id, stem, path))

    print(f"{len(jobs)} chapters x up to {COUNT} names -> {OUT_DIR}/ "
          f"on {os.cpu_count()} workers", file=sys.stderr)

    done = 0
    with Pool(os.cpu_count()) as pool:
        for stem, book_id, n, err in pool.imap_unordered(gen_chapter, jobs):
            done += 1
            note = f"  [{err}]" if err else ""
            print(f"[{done}/{len(jobs)}] {book_id}/{stem}: {n}{note}",
                  file=sys.stderr)

    print(f"done: {done} files in {OUT_DIR}/", file=sys.stderr)


if __name__ == "__main__":
    main()
