# AGENTS.md — pyebon project orientation

Read this first. It exists so any session (or a restart) can resume without
re-discovering everything.

## What this project is

A from-scratch reimplementation of **EBoN — the Everchanging Book of Names**
(Sami Pyörre, 1998-2000), an old Windows name generator. The original is
abandonware that needs a Windows XP VM and an odd license check to run. We are
**reverse-engineering its algorithm and data** and rebuilding it in Python as
`pyebon/`.

Fidelity goal: **"inspiration", not bit-exact clone.** We want EBoN's *process*
and *result quality*, and we store chapter data in **our own format** — we do
NOT need to mimic EBoN's binary format for writing new chapters. We DO want to
reuse the old content where we can decode it, so the user doesn't restart from
zero.

## Repository layout

- `pyebon_gui.py` — Tkinter GUI: the main user-facing entry point.
- `pyebon/` — the engine (the deliverable). Modules:
  - `model.py` — `Chapter` (our format): element inventories, a frequency-weighted
    **adjacency graph** with `START`/`END` sentinels (the heart of EBoN "fit"),
    structures, prefix/suffix pools, `GenOpts`.
  - `splitting.py` — split a name into alternating vowelic/consonantal elements
    (Doc/3 step 2).
  - `preprocess.py` — **strategy A**: build a `Chapter` from seed names.
  - `generate.py` — frequency-weighted random walk over the adjacency graph with
    backtracking; structure selection; validation (`!REP` etc.); real fit:2/3
    (skip-adjacency) and prefix/suffix forcing.
  - `ebn.py` — parse plaintext `.ebn` chapter files.
  - `qch.py` — **strategy B**: decode EBoN's compiled `.qch` binary;
    `qch_to_chapter` bridges it into the engine; `expand_special()` handles
    soft consonants and SPCCON custom clusters.
  - `library.py` — extract/load/save chapters as JSON; CLI for bulk extraction.
  - `__main__.py` — CLI: `python -m pyebon <chapter|file> -n 20 [--info]`.
- `data/library/` — **331 pre-extracted chapters** in JSON format (our own
  format; serialized `Chapter` objects). The engine no longer needs `Ebon/` at
  runtime.
- `data/seeds/` — the user's own plaintext name lists (one name per line),
  themed per file. These work at full quality via strategy A.
- `research/doc/` — original EBoN help text (`1-GettingStarted`, `2-BasicUse`,
  `3-WritingChapters` = the algorithm spec) + `debug.txt` (real EBoN output).
- `research/` — reverse-engineering artifacts (decompiled C from Ghidra, Ghidra
  scripts, format notes, standalone parser) + old superseded code
  (`name_generator_enhanced.py`, `name_generator_gui.py`, `cleaner.py`,
  `qch_explore.py`). See `research/README.md` for details.
- `Ebon/` — **gitignored.** The original program (proprietary `.exe`s) + 330
  `.qch` + a few `.ebn` + book data. Local reference only; no longer needed at
  runtime.

## The EBoN algorithm (summary; full spec in Doc/3-WritingChapters.txt)

1. Uppercase names; mark special letters (soft consonants TH→lowercase t, etc.).
2. Split into **elements**: maximal runs of vowels (fit as whole units) or
   consonants (fit as single letters). E.g. THRANDUIL → tR-A-ND-UI-L.
3. Gather: element adjacency at 3 **fit levels** (L1 = adjacent element/letter
   pairs; L2 = consonant-skip-vowel; L3 = vowel-skip-consonant), prefix/suffix
   pools (first/last two elements), **structures** (C/V pattern, numbered) and
   substructures (element lengths), and frequencies.
4. Validation: max letter frequency, min repetition distance, anti-cycle (`!REP`).
5. Generate: pick a structure, fill slots by frequency-weighted walk honoring the
   fit constraints; postprocess (titlecase + punctuation).

GENOPT flags: `structgen, statgen, fit:N, val:N, prefix, suffix, shuffle`,
plus `y:`/`u:` semivowel and `punct:` modes and `TEMPLATES`.

## State of the work

DONE and validated:
- The engine (strategy A) **reproduces EBoN's `debug` chapter output exactly**
  (seeds BABEBI/COCUCY → exactly the 8 expected shapes, correct boundary rules).
- Generates good, on-theme names for all seed-based chapters (Klingon, Romulan,
  the user's `chapters/*.txt`).
- `.qch` decoder reads metadata, GENOPT, alphabet, structures, and the vowel-
  element inventory from **all 330 chapters incl. locked ones** (validated vs
  debug/Luis/klingon).

Chapter inventory: **5 unlocked** (plaintext `.ebn`: klingon, romulan, debug,
Luis, Planetas) vs **326 locked** (`.qch`-only: all official Tolkien / Greyhawk /
Wheel of Time / Forgotten Realms / Star Trek / euro-gods / old-world libraries,
incl. the 12 encrypted `core/*.EBN`). Cracking the matrices unlocks 326 chapters.

## Current task (#5 DONE — format cracked via decompilation)

The `.qch` format is **fully decoded and validated** (lands exactly on `#END`
for debug/Luis/klingon). We decompiled EBoN.exe with Ghidra headless — writer
`0x41b6e1`, reader `0x41cd90`, generator `0x420730` — see
`research/qch-writer-decompiled.md` and the faithful parser
`research/parse_qch.py`. RE artifacts/scripts live in `research/`. Key corrections to earlier guesses:

- **Numeric cells are BIG-ENDIAN uint16** (high byte first). This was the whole
  blocker; little-endian searches could never match.
- **Consonant elements ARE stored** (multi-letter clusters, e.g. Klingon
  `KT/TB/NN`). The old "consonants are single letters only" note was wrong.
- `nV = f[0xe58]` is the matrix inner (fit-distance) dimension, not vowel count.
- **Prefix/suffix** entries are 3-byte keys `(idxA, idxB, tag)` (tag `'C'`=0x43
  → consonant-then-vowel, `'V'`=0x56 → vowel-then-consonant), then BE16 freqs.
  Validated on debug: prefixes BA/CO, suffixes BI/CY (its seeds' open/close).
- Structures = BE16 freq table indexed by EBoN structure number, plus
  substructure counts/freqs/labels; then bit-packed validity masks; then 2×127
  validation bytes; then `#END` (no trailing NUL).

`pyebon/qch.py` now uses this parser and feeds the engine **real** vowel +
consonant element pools, the structure distribution, and prefix/suffix START/END
edges (authentic openings/closings). Locked chapters generate clearly on-theme
(Quenya: Nahima, Tintaner, Eranoon; Sindarin: Urnir, Gindered, Hirnosir).

DONE since: **special-letter expansion** and **library extraction**.
- `qch.expand_special()` reverses soft consonants (lowercase X -> XH) and SPCCON
  custom clusters (digit codes index `list_e04`, e.g. greek 0=SS/1=PH). 329/330
  chapters now generate with no leftover marker codes.
- `pyebon/library.py` extracts every chapter to `library/<name>.json` (our own
  format; a serialized `Chapter`). `python -m pyebon.library extract` rebuilt all
  **331** chapters (~13 MB); `load_chapter()` reads them and the CLI accepts a
  bare library name (`python -m pyebon core_QUENYA`). The engine **no longer
  needs `Ebon/` at runtime** — the library is committed. The 12 encrypted
  `core/*.EBN` correctly fall back to their `.qch`.

One known fidelity gap remains (optional; the "inspiration" goal is met):
- **EBoN's exact fit matrices (M1/M2)** aren't replicated — the middle of a name
  uses generic frequency-weighted vowel↔consonant adjacency, so e.g. debug no
  longer keeps its B/C vowel sets disjoint via the `.qch` path (strategy A from
  seeds still does, exactly). M1/M2 columns are a fit-distance index the
  generator derives from (position, struct length) via `>>1`; porting it means
  transliterating the 144KB generator (`research/ebonW_00420730.c`).

## Conventions

- Stdlib only; Python 3. No external deps.
- File tools are proxied (`mcp__opencode_proxy__*`); the question UI is currently
  buggy on the user's machine — **ask questions in plain prose and stop**, do not
  use the interactive question tool, and end with a full stop after a question.
- Validate any RE claim against a known-seed chapter (debug/Luis/klingon) before
  trusting it.

## Quick commands

```
python3 pyebon_gui.py                                   # GUI
python -m pyebon core_QUENYA -n 20                      # generate by library name
python -m pyebon data/seeds/ST-Klingon.txt -n 20         # generate from seed list
python -m pyebon core_SINDARIN --info                   # show chapter metadata
python -m pyebon.library list                           # list all 331 library chapters
python -m pyebon.library extract                        # rebuild library/ from Ebon/
```
