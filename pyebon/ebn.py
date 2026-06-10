"""Parse plaintext EBoN .ebn chapter files (TITLE/LINE1/GENOPT/NAMES tags).

The format is a series of TAG = "..."; blocks. NAMES holds quoted, comma-
separated seed names. // and <!- -> style comments are ignored.
"""

from __future__ import annotations

import re
from typing import Dict, List, Tuple

from .model import GenOpts
from .preprocess import build_chapter

_TAG_RE = re.compile(r'([A-Z][A-Z0-9]*)\s*=\s*(.*?);', re.DOTALL)
_STR_RE = re.compile(r'"([^"]*)"')


def _strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        # Strip // line comments (not inside quotes — chapters don't use // in data).
        if "//" in line:
            # keep portion before // unless // is within quotes; data has no //
            q = line.count('"')
            if q == 0:
                line = line.split("//", 1)[0]
        out.append(line)
    text = "\n".join(out)
    text = re.sub(r"<!-.*?>", "", text, flags=re.DOTALL)
    return text


def parse_ebn_text(text: str) -> Tuple[Dict[str, str], List[str], GenOpts]:
    text = _strip_comments(text)
    tags: Dict[str, str] = {}
    names: List[str] = []
    for m in _TAG_RE.finditer(text):
        tag, body = m.group(1), m.group(2)
        if tag == "NAMES":
            names = _STR_RE.findall(body)
        else:
            vals = _STR_RE.findall(body)
            tags[tag] = " ".join(vals)
    opts = GenOpts.parse(tags.get("GENOPT", ""))
    return tags, names, opts


def load_ebn(path: str):
    """Load a .ebn file and return a built Chapter."""
    with open(path, "r", encoding="latin-1") as fh:
        text = fh.read()
    tags, names, opts = parse_ebn_text(text)
    return build_chapter(
        names,
        opts,
        title=tags.get("TITLE", ""),
        line1=tags.get("LINE1", ""),
        line2=tags.get("LINE2", ""),
        author=tags.get("AUTHOR", ""),
        date=tags.get("DATE", ""),
    )
