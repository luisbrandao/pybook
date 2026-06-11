"""Our own chapter library: JSON files the engine reads directly.

Once chapters are extracted here, the engine no longer needs EBoN's original
`Ebon/` files at runtime. Each `.json` is a serialized Chapter (see
`model.Chapter.to_dict`). Build the library with:

    python -m pyebon.library extract            # Ebon/ -> library/
    python -m pyebon.library list               # show what's been extracted

and load a chapter for generation with `load_chapter(path)`.
"""

from __future__ import annotations

import json
import os
import sys
from typing import List

from .model import Chapter

LIBRARY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "library")


def save_chapter(ch: Chapter, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(ch.to_dict(), fh, ensure_ascii=False, separators=(",", ":"))


def load_chapter(path: str) -> Chapter:
    with open(path, encoding="utf-8") as fh:
        return Chapter.from_dict(json.load(fh))


def _flat_name(ebon_root: str, src: str) -> str:
    """A flat, collision-free library filename from a source path under Ebon/."""
    rel = os.path.relpath(src, ebon_root)
    rel = os.path.splitext(rel)[0]
    return rel.replace(os.sep, "_").replace(" ", "_") + ".json"


def extract_all(ebon_root: str = "Ebon", out_dir: str = LIBRARY_DIR) -> List[str]:
    """Decode every chapter under `ebon_root` into `out_dir` as JSON.

    `.qch` (compiled, incl. locked chapters) go through the qch bridge; plaintext
    `.ebn` seed chapters go through the preprocessor (full-quality adjacency).
    Returns the list of written paths.
    """
    from .qch import qch_to_chapter
    from .ebn import load_ebn

    written: List[str] = []
    qch_paths, ebn_paths = [], []
    for root, _dirs, files in os.walk(ebon_root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext == ".qch":
                qch_paths.append(os.path.join(root, f))
            elif ext == ".ebn":
                ebn_paths.append(os.path.join(root, f))

    # Prefer .ebn (full adjacency) when a chapter exists in both forms; key by
    # the flat name so the .ebn version wins.
    done = set()
    for src in sorted(ebn_paths):
        try:
            ch = load_ebn(src)
        except Exception as e:
            print(f"  skip {src}: {e}", file=sys.stderr)
            continue
        # The 12 core/*.EBN are encrypted: load_ebn won't throw but yields an
        # empty/garbage chapter. Only prefer an .ebn that actually parsed; else
        # leave it for the .qch path below.
        if not ch.structures or not (ch.vowel_elements and ch.cons_elements):
            print(f"  unusable .ebn (encrypted?), deferring to .qch: {src}", file=sys.stderr)
            continue
        name = _flat_name(ebon_root, src)
        out = os.path.join(out_dir, name)
        save_chapter(ch, out)
        written.append(out)
        done.add(name)

    for src in sorted(qch_paths):
        name = _flat_name(ebon_root, src)
        if name in done:
            continue
        try:
            ch, _ = qch_to_chapter(src, fit=1)
        except Exception as e:
            print(f"  skip {src}: {e}", file=sys.stderr)
            continue
        out = os.path.join(out_dir, name)
        save_chapter(ch, out)
        written.append(out)
        done.add(name)
    return written


def _main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "list"
    if cmd == "extract":
        root = argv[1] if len(argv) > 1 else "Ebon"
        written = extract_all(root)
        total = sum(os.path.getsize(p) for p in written)
        print(f"extracted {len(written)} chapters to {LIBRARY_DIR} "
              f"({total/1024/1024:.1f} MB)")
    elif cmd == "list":
        if not os.path.isdir(LIBRARY_DIR):
            print("library/ not built yet — run: python -m pyebon.library extract")
            return
        files = sorted(f for f in os.listdir(LIBRARY_DIR) if f.endswith(".json"))
        print(f"{len(files)} chapters in {LIBRARY_DIR}:")
        for f in files:
            print("  ", f[:-5])
    else:
        print(f"unknown command {cmd!r}; use 'extract' or 'list'", file=sys.stderr)


if __name__ == "__main__":
    _main()
