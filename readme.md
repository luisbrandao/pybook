# pyebon — Everchanging Book of Names

A Python reimplementation of **EBoN** (Sami Pyörre, 1998–2000), an old Windows
name generator. The original is abandonware; this project reverse-engineered its
algorithm and data to rebuild it from scratch — stdlib-only Python 3, no
external dependencies.

The engine analyses seed names by splitting them into vowelic and consonantal
elements, learning which elements follow which at multiple "fit" levels, and
recombining them into new names that feel authentic to each language or culture.

## Quick start

```bash
# GUI — browse all 331 chapters, generate names with one click
python3 pyebon_gui.py

# CLI — generate 20 names from a library chapter
python -m pyebon core_QUENYA -n 20

# CLI — generate from your own seed list
python -m pyebon data/seeds/ST-Klingon.txt -n 20

# CLI — show chapter metadata
python -m pyebon core_SINDARIN --info

# List all available library chapters
python -m pyebon.library list
```

## What's in the library

**331 chapters** extracted from the original EBoN program, covering:
Tolkien (Quenya, Sindarin, Khuzdûl…), Greyhawk, Wheel of Time, Forgotten
Realms, Star Trek species, European gods, Old World cultures, and more — plus
**21 custom seed lists** in `data/seeds/` (Greek, Roman, Viking, ASoIaF, planets…).

The library is pre-built in `library/` as JSON. The engine does not need the
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
  library/             331 pre-extracted chapters in JSON format
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
