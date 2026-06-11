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

## Current task (#5 DONE — format cracked via decompilation)

The `.qch` format is **fully decoded and validated** (lands exactly on `#END`
for debug/Luis/klingon). We decompiled EBoN.exe with Ghidra headless — writer
`0x41b6e1`, reader `0x41cd90`, generator `0x420730` — see
`Doc/qch-writer-decompiled.md` and the faithful parser `re/parse_qch.py`. RE
artifacts/scripts live in `re/`. Key corrections to earlier guesses:

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

Two known fidelity gaps remain (both optional, "inspiration" goal is met):
1. **EBoN's exact fit matrices (M1/M2)** aren't replicated — the middle of a
   name uses generic frequency-weighted vowel↔consonant adjacency, so e.g. debug
   no longer keeps its B/C vowel sets disjoint (strategy A still does, exactly).
   M1/M2 columns are a fit-distance index the generator derives from
   (position, struct length) via `>>1`; porting it means transliterating the
   144KB generator.
2. **Special/soft letters (SPCCON)** aren't expanded: elements carry internal
   codes (digits 0-3, lowercase like the `d` in `EdE`) that should map back to
   real letter sequences on output. `splitting.mark_special` is the stub hook.

Next: optionally (a) expand special letters, (b) port the M1/M2 fit engine, then
extract **all 330 chapters into our JSON format** so the engine no longer needs
`Ebon/` at runtime.

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
