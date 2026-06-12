# pyebon — Everchanging Book of Names

A Python reimplementation of **EBoN** (Sami Pyörre, 1998–2000), an old Windows
name generator. The original is abandonware; this project reverse-engineered its
algorithm and data to rebuild it from scratch — stdlib-only Python 3, no
external dependencies.

The engine analyses seed names by splitting them into vowelic and consonantal
elements, learning which elements follow which at multiple "fit" levels, and
recombining them into new names that feel authentic to each language or culture.

## Requirements

Python 3 and its **tkinter** module (for the GUI). tkinter is part of the
standard library but most Linux distros ship it as a separate system package
that isn't installed by default — there are no pip dependencies. If you hit
`ModuleNotFoundError: No module named 'tkinter'`, install it:

| distro | command |
| --- | --- |
| Debian / Ubuntu | `sudo apt install python3-tk` |
| Fedora / RHEL / Rocky | `sudo dnf install python3-tkinter` |
| Arch / Manjaro | `sudo pacman -S tk` |
| openSUSE | `sudo zypper install python3-tk` |

The CLI works without tkinter; only the GUI needs it.

## Install the desktop launcher (optional)

```bash
./install.sh             # adds a "PyEBoN" entry to your application menu
./install.sh --uninstall # remove it
```

It fills in the current checkout path and your `python3` automatically, and
checks tkinter is present.

## Quick start

```bash
# GUI — browse books & chapters, generate names, build your own chapters
python3 pyebon_gui.py

# CLI — generate 20 names from a library chapter
python -m pyebon core_QUENYA -n 20

# CLI — generate from your own seed list
python -m pyebon data/seeds/ST-Klingon.txt -n 20

# CLI — show chapter metadata
python -m pyebon core_SINDARIN --info

# List all available library chapters
python -m pyebon.library books      # list books
python -m pyebon.library list       # list every chapter, grouped by book
```

## What's in the library

**332 chapters across 34 books** extracted from the original EBoN program, covering:
Tolkien (Quenya, Sindarin, Khuzdûl…), Greyhawk, Wheel of Time, Forgotten
Realms, Star Trek species, European gods, Old World cultures, and more — plus
**21 custom seed lists** in `data/seeds/` (Greek, Roman, Viking, ASoIaF, planets…).

The library is pre-built in `data/library/<book>/` as JSON (with a per-book
`book.json`). The engine does not need the
original EBoN files at runtime.

## Generation options

| Option | What it does |
|--------|-------------|
| **Fit level** (0–3) | How strictly a new name must echo the original patterns. 0 = loose/random, 1 = adjacent elements must match, 2–3 = progressively stricter. |
| **Prefix** | Force the name to start with an authentic opening pair from the seed data. |
| **Suffix** | Force the name to end with an authentic closing pair. |
| **Count** (`-n`) | How many names to generate. |
| **Min/Max length** (`-m`/`-x`) | Length bounds for generated names. |
| **Seed** (`-s`) | Random seed for reproducible output. |

## Repository layout

```
pyebon_gui.py          GUI (Tkinter) — the main user-facing entry point
pyebon/                the engine
  model.py               Chapter data model (adjacency graph, pools, options)
  splitting.py           vowelic/consonantal element splitting
  preprocess.py          build a Chapter from seed names
  generate.py            frequency-weighted random walk + validation
  qch.py                 decode EBoN's compiled .qch binary format
  ebn.py                 parse plaintext .ebn chapter files
  library.py             extract/load/save chapters as JSON
  __main__.py            CLI entry point
data/
  data/library/<book>/  332 pre-extracted chapters across 34 books (JSON)
  data/seeds/           your own seed lists (+ optional .meta.json sidecars)
  seeds/               custom seed lists (one name per line)
  Doc/                   original EBoN documentation (algorithm spec)
research/              reverse-engineering artifacts + old superseded code
```

## Requirements

Python 3.6+, stdlib only — no `pip install` needed.

## How it works

1. **Split** each seed name into alternating vowel/consonant elements
   (e.g. THRANDUIL → TH·R·A·ND·UI·L).
2. **Learn** element adjacency at up to 3 fit levels, plus prefix/suffix pools,
   structural patterns (CVCVC…), and frequencies.
3. **Generate** by picking a structure, then walking the adjacency graph with
   weighted random selection and backtracking.
4. **Validate** against repetition, letter-frequency, and cycle rules.
5. **Post-process** (titlecase, punctuation).

Full algorithm spec: `Doc/3-WritingChapters.txt`.
