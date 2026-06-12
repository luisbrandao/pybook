# PyEBoN — session handoff & the fit-matrix (M1/M2) port

> Written 2026-06-12 as a cold-start briefing for a **clean session** that will
> tackle the last big piece of work: porting EBoN's exact fit matrices so the
> imported library books generate at full fidelity. Read `AGENTS.md` first for
> the project's purpose and conventions; this document is the deep dive.
>
> Latest commit at hand-off: **`6a8c218`** (chapter blending). Working tree clean.

---

## 1. What the project is (30-second version)

A from-scratch Python reimplementation of **EBoN — the Everchanging Book of
Names** (1998–2000 Windows abandonware name generator). Goal is *"inspiration"
fidelity*: reproduce EBoN's process and result quality, store data in our own
format. We reverse-engineered EBoN's compiled `.qch` chapter binaries and
extracted its entire library into our own JSON. Stdlib-only Python 3, no deps.

The original program runs only in a Windows XP VM (odd license check). The user
can still run it there to generate fresh data on request — this is how dumps for
"distillation" (see §3) are produced.

---

## 2. Current state — what works

Everything below is done, committed, and validated. The project is effectively
**feature-complete**; the only substantial open work is §4 (the fit-matrix port).

### Generation engines (two, selectable)
- **Classic (fit-levels)** — `pyebon/generate.py::Generator`. EBoN's method: pick
  a C/V structure, fill its slots by a frequency-weighted random walk over the
  adjacency graph with backtracking. Real `fit` 0–3, prefix/suffix forcing,
  `!REP` validation. **Validated**: reproduces the `debug` chapter's exact 8 name
  shapes from its 2 seeds.
- **Smart (back-off)** — `pyebon/backoff.py::BackoffGenerator` (NEW this arc). A
  variable-order back-off Markov model over the element sequence: predicts each
  next element from the longest run of preceding elements seen, backing off when
  unknown; length decided by an END token; category alternation inherent. Has a
  **temperature/variety** knob (<1 safe, >1 wild).
- Chosen via `pyebon/generate.py::make_generator(chapter, method, seed, temperature)`.

### Chapter blending (NEW this arc)
- `pyebon/blend.py::blend_chapters([(chapter, weight), ...])` — mass-normalizes
  each source so size doesn't dominate, scales by weight, sums **every** field
  both engines read (inventories, `adj`, `adj2`, `ngrams`, structures,
  prefix/suffix). Returns an ordinary `Chapter`; `opts` are deep-copied so blends
  never mutate cached sources. E.g. 70% Klingon + 30% Greek → coherent hybrids.

### The data
- **`data/library/<book>/<chapter>.json`** — 332 chapters across 34 books, our
  serialized `Chapter`. Mirrors EBoN's Library/Book hierarchy; each book has a
  `book.json` (decoded from EBoN's `book.dat`: title/description/author/date).
- **28 of those chapters are "distilled"** (carry `distilled_from`): rebuilt from
  large EBoN output dumps so they have full `adj`/`adj2`/`ngrams` — they generate
  at full fidelity in BOTH engines. The other ~304 are **`.qch`-bridged** and are
  the ones §4 is about.
- **`data/seeds/*.txt`** — 18 user seed lists (one name/line, optional
  `<name>.meta.json` sidecar). Compiled to `Chapter` on demand and cached in
  `data/seeds/.compiled/` (gitignored, mtime-invalidated). Seed chapters have
  full `adj`/`adj2`/`ngrams`.
- **`data/dumps/ebn-*.txt`** — gitignored raw EBoN output dumps (the distillation
  sources). NEVER committed (they're huge; the user's editor dies on big diffs).

### The GUI — `pyebon_gui.py` (Tkinter, ivory theme)
- **Generate tab**: two-column Books|Chapters picker + searchable; metadata panel;
  controls for count, Shortest/Longest length, seed; **Engine** (Classic/Smart),
  **Variety**, Fit, Prefix/Suffix, **Blend with** + primary-% mix; Copy/Save/Dedup;
  scrollable `?` help.
- **Build a chapter tab**: paste/load seed names, edit metadata (saved to sidecar),
  preview, save into `data/seeds/`.
- Installed as a GNOME launcher via `assets/pyebon.desktop` (+ `pyebon.svg`).

### CLI — `python -m pyebon <chapter> [-n] [-m] [-x] [-s] [--method] [-t] [--info]`
- `<chapter>` = library name (`QUENYA` or `core/QUENYA`), or path to `.json` /
  `.ebn` / `.qch` / `.txt`. `--method classic|backoff`, `-t/--temp` for back-off.
- `python -m pyebon.library {extract|compile|books|list|distill|distill-all}`.
  `distill-all` auto-maps every `data/dumps/ebn-*.txt` to its library chapter and
  distills in bulk (dry-run by default; `--apply` to write).

### Reverse-engineering artifacts — `research/`
- `qch-writer-decompiled.md` — **the definitive `.qch` format spec** (from the
  decompiled writer). Read this for §4.
- `parse_qch.py` — faithful standalone parser; lands exactly on `#END`.
- `qch_writer_decompiled.c` / `qch_reader_decompiled.c` — Ghidra C of the
  writer (`0x41b6e1`) and reader (`0x41cd90`).
- `ebonW_00420730.c` (144 KB) — Ghidra C of the **generator** `FUN_00420730`.
  This is the function to transliterate for the full port (§4, Option B).
- `DecompFuncs.java` / `DecompAt.java` / `FindRefs.java` / `FindImm.java` —
  Ghidra headless scripts used to produce the above. `run_ghidra.sh` launches.
- Ghidra itself: `~/Downloads/ghidra_12.1.2_PUBLIC_.../`, headless mode, JDK 21
  present. rizin/radare2 installed (disassembly only, no decompiler). The
  analyzed project was at `/tmp/ghproj2` (may be gone after reboot — re-import
  `Ebon/EBoN.exe` if needed; ~140 s analysis).

---

## 3. What happened (the arc that got us here)

1. **Cracked the `.qch` format** by decompiling EBoN.exe with Ghidra headless
   (rizin found the writer via the `"EBoN 3.0"` string xref; Ghidra decompiled
   it). Key discovery: numeric cells are **big-endian uint16** — every prior
   little-endian search had failed. The parser now lands exactly on `#END` for
   debug/Luis/Klingon (chapters whose seeds we fully know = Rosetta stones).
2. **Extracted the whole library** to `data/library/` (no longer needs `Ebon/`).
3. **Special-letter expansion** (`qch.py::expand_special`): soft consonants
   (lowercase→+H) and SPCCON digit clusters. 329/330 chapters clean.
4. **Metadata fix**: the 5 `.qch` strings are title / 2 subtitle lines / author /
   numeric-serial. Author was being read from the serial slot — fixed; all books
   show real credit lines now. **EBoN does not store a per-chapter DATE** in
   `.qch` (only book-level `book.dat` has dates).
5. **Nested hierarchy** restored (`<book>/<chapter>.json` + `book.json`).
6. **Distillation**: dump 10k+ names from EBoN with all options on (fit:3,
   prefix, suffix, shuffle), feed through the seed preprocessor → recovers ~96%
   of true adjacency AND the skip/`adj2` data the `.qch` can't give. `distill`
   and `distill-all` commands wire this in. Validated against ROMANFEM (a chapter
   we authored, so we know its exact seeds).
7. **Back-off engine + temperature** (§2).
8. **Chapter blending** (§2).
9. Plus: seed precompile cache, GUI two-column picker + metadata panel + Build
   tab, ivory theme, `.desktop` launcher, header-stripping for dumps
   (`description\n\n names` pattern), Dedup button, clearer length labels,
   scrollable help.

---

## 4. THE NEXT TASK — port EBoN's fit matrices (M1/M2)

### The gap, precisely
The ~304 `.qch`-bridged library books generate via `pyebon/qch.py::qch_to_chapter`,
which today does TWO lossy things (see `qch.py:244–274`):
- uses only the **row-sums** of M1/M2 as flat element frequencies, and
- builds a **generic all-pairs alternating adjacency** (every vowel↔consonant
  transition allowed, weighted by target frequency).

Consequences: these books have **no `adj2` and no `ngrams`**, so **fit 2/3
collapse to fit 1** and **Smart falls back to order-1** for them. Names are
on-theme (openings/closings are real, via prefix/suffix→START/END edges) but the
*middles* are generic. This is the one remaining fidelity gap (AGENTS.md notes it).

### The crucial fact (saves a lot of work)
**M1 and M2 are already fully decoded** — `qch.py::decode_qch` parses them into
`d.M1` (`[n44 vowel-elements × nV]`) and `d.M2` (`[n48 cons-elements × nV]`),
big-endian uint16 (`qch.py:190,194`). We are **not** missing data; we are
**discarding its structure**. The columns are thrown away.

### What the columns mean (from `qch-writer-decompiled.md` §"VALIDATED")
- `nV = f[0xe58]` is the **matrix inner dimension** (debug=6, Luis=8, Klingon=7),
  NOT the vowel count. It tracks the max structure length / fit window.
- The generator (`FUN_00420730`) computes a **column index from (position,
  structure-length) via `>>1` halving** — this *is* EBoN's L1/L2/L3 "fitting"
  mechanism. So `M1[i][col]` = how strongly vowel-element `i` fits at the
  fit-distance encoded by `col`; `M2` likewise for consonant elements.

In other words: M1/M2 are **position/fit-distance-conditioned element frequency
tables**. They are richer than a flat frequency and richer than plain bigram
adjacency — they encode "what fits here given where we are in the name."

### Two ways to spend the effort (decision pending — user will choose in-session)

**Option A — derive structure from M1/M2 into the EXISTING engine (cheaper).**
Reconstruct per-fit-distance adjacency (`adj`, and especially `adj2`) — or even
synthesize `ngrams` — from the M1/M2 columns, and write them into the bridged
library `Chapter`. The existing fit 2/3 machinery and Smart engine then "just
work" on library books. Much less code; reuses validated machinery; lifts books
well above today's order-1. Risk: the mapping from "fit-distance column" to our
"distance-2 skip adjacency" is an approximation, not EBoN's exact walk.

**Option B — full port of `FUN_00420730` (faithful, large).**
Transliterate the generator's exact column-derivation (`>>1` from position &
struct length) and matrix-weighted slot filling into a new generator mode. Most
faithful; reproduces EBoN's middles exactly. Cost: it's a 144 KB decompiled
function (`research/ebonW_00420730.c`); bounded but large and somewhat uncertain.

**Recommendation:** start with **Option A** — it captures most of the quality for
a fraction of the work and is independently useful. Escalate to **B** only if A's
output is visibly off vs. real EBoN. (The user's distillation workflow already
gives full fidelity for any book they care to dump, so B is "complete the whole
332-book library without VM dumping" — a nice-to-have, not a blocker.)

### Concrete first steps for the clean session
1. **Re-read** `research/qch-writer-decompiled.md` (esp. steps 19/22 and the
   VALIDATED section) and skim `research/parse_qch.py`.
2. **Dump M1/M2 for the Rosetta stones** where seeds are fully known:
   `Ebon/Newkie/debug.qch` (seeds BABEBI, COCUCY), `Ebon/Newkie/Luis.qch`,
   `data/seeds/ST-Klingon.txt`↔`klingon.qch`, and `Ebon/Newkie/ROMANFEM.qch`
   (we authored ROMANFEM, so its 583 seeds are known — the best stone).
   Use `pyebon.qch.decode_qch(path)` → inspect `.M1`, `.M2`, `.nV`.
3. **Confirm the column semantics empirically**: from the known seeds, compute
   the expected per-fit-distance element frequencies under the hypothesized
   `>>1` column formula and compare to the decoded M1/M2. debug is tiny (nV=6,
   values 1–2) and ideal for this.
4. Once the column→fit-distance mapping is confirmed, implement Option A: in
   `qch_to_chapter`, replace the generic all-pairs adjacency (`qch.py:263–274`)
   with M1/M2-derived `adj`/`adj2` (and optionally `ngrams`). Keep the
   prefix/suffix START/END seeding (it's correct and validated).
5. **Validate**: distilled chapters are ground truth — compare a bridged book's
   newly-derived adjacency against the SAME book's distilled version (e.g.
   `icefire/*`, `fae/io_faera`) which we already have. Aim to approach the
   distilled quality without the dump.
6. Re-extract the library (`python -m pyebon.library extract`) to bake the new
   data in — **WARNING**: this rewrites all ~304 bridged JSONs = a large git
   diff. The user's editor has died on large diffs before. Commit via CLI
   (`git add -A data/library && git commit`) WITHOUT opening the diff in-editor,
   and keep `data/dumps/` gitignored. Consider committing in chunks if needed.

### Risks / unknowns
- The exact `>>1` column formula and how start/end positions map to columns
  needs the empirical confirmation in step 3 before trusting any derivation.
- M1/M2 give position-conditioned *element* frequencies, not directly a
  *transition* graph — Option A must choose how to turn "element fits at distance
  d" into "b may follow a". Validating against distilled twins (step 5) is how we
  keep that honest.
- `structure_pattern()` (`qch.py:140`) maps EBoN structure numbers to C/V tuples;
  validated for 0..12. Higher numbers exist in some books — sanity-check.

---

## 5. Housekeeping noticed (not blocking; clean up when convenient)
- **`pyebon/-n`** — a tracked 0-byte junk file (from a botched `... -n` shell
  redirection). Safe to `git rm`.
- **`ROMANFEM.txt`** at repo root — a tracked test artifact from the distillation
  experiment; probably belongs in `research/` or removed.
- **CLI `--help` example** in `pyebon/__main__.py` docstring still says the old
  flat name `core_QUENYA`; nested lookup wants `QUENYA` or `core/QUENYA`.
- The `English-Male.meta.json` stale-metadata episode was fixed upstream
  (commit `e3abbf3`); the Build tab's "New" button now resets fields.

## 6. Sanity commands (verify nothing's broken)
```
python3 -m pyebon QUENYA -n 10                       # bridged library book (classic)
python3 -m pyebon ST-Klingon --method backoff -t 1.4 # seed chapter, smart engine
python3 -m pyebon QUENYA --info                      # shows "deep model: no" (the §4 gap)
python3 -m pyebon ST-Klingon --info                  # shows "deep model: yes"
python3 pyebon_gui.py                                 # GUI (DISPLAY available)
# debug regression (must give exactly 8 shapes): generate ~400 from Ebon/Newkie/debug.ebn classic
```
