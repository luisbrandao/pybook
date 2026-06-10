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

- `pyebon/` — our engine (the deliverable). Modules:
  - `model.py` — `Chapter` (our format): element inventories, a frequency-weighted
    **adjacency graph** with `START`/`END` sentinels (the heart of EBoN "fit"),
    structures, prefix/suffix pools, `GenOpts`.
  - `splitting.py` — split a name into alternating vowelic/consonantal elements
    (Doc/3 step 2). `mark_special` is a stub hook for soft consonants (SPCCON).
  - `preprocess.py` — **strategy A**: build a `Chapter` from seed names.
  - `generate.py` — frequency-weighted random walk over the adjacency graph with
    backtracking; structure selection; validation (`!REP` etc.).
  - `ebn.py` — parse plaintext `.ebn` chapter files.
  - `qch.py` — **strategy B**: decode EBoN's compiled `.qch` binary; `qch_to_chapter`
    bridges it into the engine (currently fit:0 only — see "Current task").
  - `__main__.py` — CLI: `python -m pyebon <chapter.ebn|.qch> -n 20 [--info]`.
- `Doc/` — original EBoN help text (`1-GettingStarted`, `2-BasicUse`,
  `3-WritingChapters` = the algorithm spec) + our `qch-format-notes.md`
  (the `.qch` binary format RE) + `debug.txt` (real EBoN output samples).
- `Ebon/` — **gitignored.** The original program (proprietary `.exe`s) + 330
  `.qch` + a few `.ebn` + book data. Local reference only; we decode it into our
  format. Do not commit.
- `chapters/` — the user's own plaintext name lists (one name per line), themed
  per file. These work at full quality via strategy A right now.
- `name_generator_enhanced.py`, `name_generator_gui.py`, `cleaner.py` — the
  user's earlier, simpler generator (pre-EBoN-RE). Superseded by `pyebon/` but
  left in place.
- `qch_explore.py` — scratch hex/format analysis tool for `.qch`.

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

## Current task (#5): decode the `.qch` adjacency/frequency matrices

This is the gate to full-quality generation from the 326 locked chapters.
Without it, `qch_to_chapter` only supports fit:0 (rough — real vowel elements and
structures but random consonant placement).

What we know (details in `Doc/qch-format-notes.md`):
- The matrix region starts right after the vowel list (klingon: ~0x10c) and runs
  to a `#END` terminator. It's sparse little-endian `uint16` tables.
- Per Doc/3, consonants are fit as **single letters** (no consonant-element
  strings are stored); vowels as **whole elements**.
- Index spaces: **consonant letters by position in the alphabet field**; **vowel
  elements by position in the vowel list** (both come straight from the decoder).

Method to crack it (in progress):
- Use Klingon (we have both `.ebn` seeds and `.qch`). Recompute its expected
  adjacency from the seeds using the qch's element orderings, then search the
  byte region for the matching sub-blocks (try both row/col-major) to deduce
  each matrix's offset, dimensions, and meaning (L1 C↔V, L2 C↔C, L3 V↔V,
  start/end, prefix/suffix). NOTE: a few seed names contain letters absent from
  the compiled alphabet (e.g. F, X) — EBoN rejected those names; skip them when
  recomputing.
- Earlier matrix dumps showed values that were multiples of 256 → there is a
  **1-byte alignment subtlety**; check odd/even start offsets.

Once decoded: populate `Chapter.adj` (with weights) from the qch, raise the
bridge to full `fit`, then extract **all 330 chapters into our JSON format** so
the engine no longer needs `Ebon/` at runtime.

## Conventions

- Stdlib only; Python 3. No external deps.
- File tools are proxied (`mcp__opencode_proxy__*`); the question UI is currently
  buggy on the user's machine — **ask questions in plain prose and stop**, do not
  use the interactive question tool, and end with a full stop after a question.
- Validate any RE claim against a known-seed chapter (debug/Luis/klingon) before
  trusting it.

## Quick commands

```
python -m pyebon Ebon/startrek/klingon.ebn -n 20        # full-quality (seeds)
python -m pyebon Ebon/core/QUENYA.qch -n 20             # locked chapter (fit:0 for now)
python -m pyebon Ebon/core/SINDARIN.qch --info          # decoded metadata/inventory
python qch_explore.py Ebon/<path>.qch                   # raw format dump
```
