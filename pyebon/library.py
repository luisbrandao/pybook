"""Our own chapter library: JSON files the engine reads directly.

Once chapters are extracted here, the engine no longer needs EBoN's original
`Ebon/` files at runtime. The library mirrors EBoN's own hierarchy:

    data/library/<book>/book.json        # decoded book.dat: title, description, author
    data/library/<book>/<chapter>.json   # a serialized Chapter (see model.Chapter)

Build / inspect the library with:

    python -m pyebon.library extract            # Ebon/ -> data/library/<book>/...
    python -m pyebon.library books              # list books
    python -m pyebon.library list [book]        # list chapters (optionally in a book)
    python -m pyebon.library compile            # precompile data/seeds/*.txt

and load a chapter for generation with `load_chapter(path)`.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Dict, List, Optional, Tuple

from .model import Chapter

_DATA = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LIBRARY_DIR = os.path.join(_DATA, "library")
SEEDS_DIR = os.path.join(_DATA, "seeds")
# Precompiled seed chapters: building a Chapter from a big seed .txt costs real
# time (~0.3s for 30k names), and the GUI used to re-run it every session. We
# cache the built Chapter as JSON next to the seeds and reuse it until the .txt
# is edited (mtime check), so opening a seed list is as instant as a library book.
COMPILED_DIR = os.path.join(SEEDS_DIR, ".compiled")

BOOK_META = "book.json"   # per-book metadata file, sits beside the chapters


# --------------------------------------------------------------------------- #
# Chapter (de)serialization
# --------------------------------------------------------------------------- #
def save_chapter(ch: Chapter, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(ch.to_dict(), fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def load_chapter(path: str) -> Chapter:
    with open(path, encoding="utf-8") as fh:
        return Chapter.from_dict(json.load(fh))


def chapter_title(path: str) -> str:
    """Read just the title field of a chapter JSON (cheap listing helper)."""
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh).get("title") or os.path.splitext(os.path.basename(path))[0]
    except Exception:
        return os.path.splitext(os.path.basename(path))[0]


# --------------------------------------------------------------------------- #
# Seed precompile cache + per-seed metadata sidecar
# --------------------------------------------------------------------------- #
def compiled_path(txt_path: str) -> str:
    """Cache path for a seed .txt: data/seeds/.compiled/<stem>.json."""
    stem = os.path.splitext(os.path.basename(txt_path))[0]
    return os.path.join(COMPILED_DIR, stem + ".json")


def seed_meta_path(txt_path: str) -> str:
    """Sidecar metadata for a seed .txt: data/seeds/<stem>.meta.json.

    Seed lists carry no metadata of their own; this optional sidecar lets the
    user attach a title / description / author / date that survive recompiling.
    """
    root = os.path.splitext(txt_path)[0]
    return root + ".meta.json"


def load_seed_meta(txt_path: str) -> Dict[str, str]:
    p = seed_meta_path(txt_path)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {}


def save_seed_meta(txt_path: str, meta: Dict[str, str]) -> None:
    p = seed_meta_path(txt_path)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def _apply_meta(ch: Chapter, meta: Dict[str, str], default_title: str) -> None:
    ch.title = meta.get("title") or default_title
    ch.line1 = meta.get("line1", ch.line1)
    ch.line2 = meta.get("line2", ch.line2)
    ch.author = meta.get("author", ch.author)
    ch.date = meta.get("date", ch.date)


def compile_seed(txt_path: str, force: bool = False) -> Chapter:
    """Build (or load from cache) the Chapter for a seed .txt list.

    Uses a precompiled JSON next to the seeds; rebuilds it only when the .txt or
    its metadata sidecar is newer than the cache (or `force`). This is what lets
    the GUI/CLI open a seed list instantly instead of re-running build_chapter.
    """
    from .preprocess import build_chapter, parse_seed_text

    cache = compiled_path(txt_path)
    meta_p = seed_meta_path(txt_path)
    newest_src = os.path.getmtime(txt_path)
    if os.path.exists(meta_p):
        newest_src = max(newest_src, os.path.getmtime(meta_p))
    if not force and os.path.exists(cache) and os.path.getmtime(cache) >= newest_src:
        return load_chapter(cache)

    with open(txt_path, encoding="utf-8") as fh:
        header, names = parse_seed_text(fh.read())
    ch = build_chapter(names)
    meta = load_seed_meta(txt_path)
    if header and "line1" not in meta:
        # No sidecar description: fall back to the dump's embedded header line.
        meta = {**meta, "line1": header}
    _apply_meta(ch, meta, os.path.splitext(os.path.basename(txt_path))[0])
    save_chapter(ch, cache)
    return ch


def compile_all_seeds(seeds_dir: str = SEEDS_DIR, force: bool = False):
    """Precompile every seed .txt in `seeds_dir`. Returns [(name, seconds)]."""
    import glob
    import time

    results = []
    for txt in sorted(glob.glob(os.path.join(seeds_dir, "*.txt"))):
        t = time.perf_counter()
        compile_seed(txt, force=force)
        results.append((os.path.basename(txt), time.perf_counter() - t))
    return results


# --------------------------------------------------------------------------- #
# Book metadata (decoded from EBoN's book.dat)
# --------------------------------------------------------------------------- #
def decode_book_dat(path: str) -> Dict:
    """Decode a book.dat (plaintext, CRLF lines): title + description + author.

    Layout observed across all books: line 0 = title, the remaining lines are
    description / author / edition+date (varies per book). We keep them all.
    """
    with open(path, "rb") as fh:
        raw = fh.read().decode("latin-1")
    lines = [ln.strip() for ln in raw.replace("\r\n", "\n").split("\n")]
    lines = [ln for ln in lines if ln]
    title = lines[0] if lines else ""
    return {
        "title": title,
        "line1": lines[1] if len(lines) > 1 else "",
        "line2": lines[2] if len(lines) > 2 else "",
        "author": lines[3] if len(lines) > 3 else "",
        "lines": lines,
    }


def _find_book_dat(book_dir: str) -> Optional[str]:
    for f in os.listdir(book_dir):
        if f.lower() == "book.dat":
            return os.path.join(book_dir, f)
    return None


def book_meta_path(book_id: str, out_dir: str = LIBRARY_DIR) -> str:
    return os.path.join(out_dir, book_id, BOOK_META)


def load_book_meta(book_id: str, out_dir: str = LIBRARY_DIR) -> Dict:
    p = book_meta_path(book_id, out_dir)
    if os.path.exists(p):
        try:
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        except Exception:
            pass
    return {"title": book_id, "line1": "", "line2": "", "author": ""}


# --------------------------------------------------------------------------- #
# Discovery — books and chapters
# --------------------------------------------------------------------------- #
def list_books(out_dir: str = LIBRARY_DIR) -> List[Tuple[str, str]]:
    """Return [(book_id, display_title)] for every book dir holding chapters."""
    if not os.path.isdir(out_dir):
        return []
    books = []
    for book_id in sorted(os.listdir(out_dir)):
        bdir = os.path.join(out_dir, book_id)
        if not os.path.isdir(bdir):
            continue
        has_chapter = any(f.endswith(".json") and f != BOOK_META
                          for f in os.listdir(bdir))
        if has_chapter:
            books.append((book_id, load_book_meta(book_id, out_dir).get("title", book_id)))
    return sorted(books, key=lambda b: b[1].lower())


def list_chapters(book_id: str, out_dir: str = LIBRARY_DIR) -> List[Tuple[str, str, str]]:
    """Return [(stem, display_title, path)] for chapters in a book."""
    bdir = os.path.join(out_dir, book_id)
    if not os.path.isdir(bdir):
        return []
    out = []
    for f in sorted(os.listdir(bdir)):
        if f.endswith(".json") and f != BOOK_META:
            path = os.path.join(bdir, f)
            out.append((f[:-5], chapter_title(path), path))
    return sorted(out, key=lambda c: c[1].lower())


def find_chapter(name: str, out_dir: str = LIBRARY_DIR) -> Optional[str]:
    """Resolve a chapter reference to a path. Accepts 'book/chapter', a bare
    chapter stem (first match across books), or a legacy flat 'book_chapter'."""
    if "/" in name or os.sep in name:
        cand = os.path.join(out_dir, name + ".json")
        return cand if os.path.exists(cand) else None
    for book_id, _ in list_books(out_dir):
        cand = os.path.join(out_dir, book_id, name + ".json")
        if os.path.exists(cand):
            return cand
    # legacy flat fallback: book_chapter.json directly under out_dir
    flat = os.path.join(out_dir, name + ".json")
    return flat if os.path.exists(flat) else None


# --------------------------------------------------------------------------- #
# Extraction — Ebon/ -> nested library
# --------------------------------------------------------------------------- #
def _is_distilled(path: str) -> bool:
    """True if a library chapter JSON was produced by distill_into_library."""
    if not os.path.exists(path):
        return False
    try:
        with open(path, encoding="utf-8") as fh:
            return bool(json.load(fh).get("distilled_from"))
    except Exception:
        return False


def _book_id(ebon_root: str, src: str) -> str:
    """Book id = the directory the chapter lives in, relative to Ebon/."""
    rel = os.path.relpath(os.path.dirname(src), ebon_root)
    return rel.replace(os.sep, "_") if rel != "." else "_root"


def extract_all(ebon_root: str = "Ebon", out_dir: str = LIBRARY_DIR) -> List[str]:
    """Decode every chapter under `ebon_root` into `out_dir/<book>/<chapter>.json`.

    `.qch` (compiled, incl. locked chapters) go through the qch bridge; plaintext
    `.ebn` seed chapters go through the preprocessor (full-quality adjacency).
    Also writes a `book.json` per book from its `book.dat`. Returns written paths.
    """
    from .qch import qch_to_chapter
    from .ebn import load_ebn

    written: List[str] = []
    qch_paths, ebn_paths, book_dirs = [], [], set()
    for root, _dirs, files in os.walk(ebon_root):
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext == ".qch":
                qch_paths.append(os.path.join(root, f))
                book_dirs.add(root)
            elif ext == ".ebn":
                ebn_paths.append(os.path.join(root, f))
                book_dirs.add(root)

    # Book metadata: decode each book.dat into <book>/book.json.
    for bdir in sorted(book_dirs):
        bid = _book_id(ebon_root, os.path.join(bdir, "x"))
        dat = _find_book_dat(bdir)
        meta = decode_book_dat(dat) if dat else {"title": bid, "line1": "",
                                                 "line2": "", "author": ""}
        out = book_meta_path(bid, out_dir)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2)
            fh.write("\n")

    def out_path(src):
        bid = _book_id(ebon_root, src)
        stem = os.path.splitext(os.path.basename(src))[0]
        return bid, os.path.join(out_dir, bid, stem + ".json")

    # Prefer .ebn (full adjacency) when a chapter exists in both forms.
    done = set()
    for src in sorted(ebn_paths):
        try:
            ch = load_ebn(src)
        except Exception as e:
            print(f"  skip {src}: {e}", file=sys.stderr)
            continue
        # The 12 core/*.EBN are encrypted: load_ebn yields an empty/garbage
        # chapter. Only prefer an .ebn that actually parsed; else defer to .qch.
        if not ch.structures or not (ch.vowel_elements and ch.cons_elements):
            print(f"  unusable .ebn (encrypted?), deferring to .qch: {src}", file=sys.stderr)
            continue
        bid, out = out_path(src)
        if _is_distilled(out):
            print(f"  keep distilled: {os.path.relpath(out, out_dir)}", file=sys.stderr)
            written.append(out); done.add(out)
            continue
        save_chapter(ch, out)
        written.append(out)
        done.add(out)

    for src in sorted(qch_paths):
        bid, out = out_path(src)
        if out in done:
            continue
        if _is_distilled(out):
            print(f"  keep distilled: {os.path.relpath(out, out_dir)}", file=sys.stderr)
            written.append(out)
            done.add(out)
            continue
        try:
            ch, _ = qch_to_chapter(src, fit=1)
        except Exception as e:
            print(f"  skip {src}: {e}", file=sys.stderr)
            continue
        save_chapter(ch, out)
        written.append(out)
        done.add(out)
    return written


def distill_into_library(seed_txt: str, ref: str, out_dir: str = LIBRARY_DIR) -> str:
    """Replace a library chapter's model with one distilled from a dump of names.

    A big sample of EBoN's own output (`seed_txt`) is run through the seed
    preprocessor to recover the full model — including the skip-fit (adj2) data
    the .qch bridge lacks — then written over the target library chapter while
    preserving its real metadata (title / description / author / date). The
    target is tagged `distilled_from` so `extract` won't clobber it.
    """
    from .preprocess import build_chapter, parse_seed_text

    target = find_chapter(ref, out_dir)
    if not target:
        raise FileNotFoundError(f"no library chapter matches {ref!r}")

    with open(target, encoding="utf-8") as fh:
        meta = json.load(fh)

    with open(seed_txt, encoding="utf-8") as fh:
        _header, names = parse_seed_text(fh.read())
    ch = build_chapter(names)
    # keep the original chapter's metadata, not the seed filename
    ch.title = meta.get("title") or ch.title
    ch.line1 = meta.get("line1", ch.line1)
    ch.line2 = meta.get("line2", ch.line2)
    ch.author = meta.get("author", ch.author)
    ch.date = meta.get("date", ch.date)

    d = ch.to_dict()
    d["distilled_from"] = os.path.basename(seed_txt)
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return target


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    cmd = argv[0] if argv else "books"
    if cmd == "extract":
        root = argv[1] if len(argv) > 1 else "Ebon"
        written = extract_all(root)
        total = sum(os.path.getsize(p) for p in written)
        print(f"extracted {len(written)} chapters across "
              f"{len(list_books())} books to {LIBRARY_DIR} ({total/1024/1024:.1f} MB)")
    elif cmd == "books":
        books = list_books()
        print(f"{len(books)} books in {LIBRARY_DIR}:")
        for bid, title in books:
            n = len(list_chapters(bid))
            print(f"   {title:40s} [{bid}]  ({n} chapters)")
    elif cmd == "list":
        if len(argv) > 1:
            book = argv[1]
            chs = list_chapters(book)
            print(f"{len(chs)} chapters in {book}:")
            for stem, title, _ in chs:
                print(f"   {title:30s} [{stem}]")
        else:
            total = 0
            for bid, title in list_books():
                chs = list_chapters(bid)
                total += len(chs)
                print(f"== {title} ({bid})")
                for stem, ctitle, _ in chs:
                    print(f"     {ctitle}")
            print(f"{total} chapters total")
    elif cmd == "compile":
        force = "--force" in argv
        results = compile_all_seeds(force=force)
        total = sum(dt for _, dt in results)
        print(f"compiled {len(results)} seed chapters to {COMPILED_DIR} "
              f"({total:.2f}s total)")
        for name, dt in results:
            print(f"   {name}  ({dt:.2f}s)")
    elif cmd == "distill":
        if len(argv) < 3:
            print("usage: distill <seed.txt> <book/chapter>", file=sys.stderr)
            return
        target = distill_into_library(argv[1], argv[2])
        print(f"distilled {argv[1]} -> {os.path.relpath(target, LIBRARY_DIR)}")
    else:
        print(f"unknown command {cmd!r}; use 'extract', 'books', 'list', "
              f"'compile', or 'distill'", file=sys.stderr)


if __name__ == "__main__":
    _main()
