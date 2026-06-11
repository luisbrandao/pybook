# Research & old code

Reverse-engineering artifacts from decompiling EBoN.exe, plus the old
(pre-pyebon) name generator that has been superseded.

## Reverse engineering (EBoN.exe — Borland C++ Builder, 1998)

Ghidra headless was used to decompile the key functions. The results here
are what let us crack the `.qch` binary format and build the faithful parser
now living in `pyebon/qch.py`.

| File | What |
|------|------|
| `qch_writer_decompiled.c` | Decompiled `.qch` writer (`0x41b6e1`). Defines the on-disk format. |
| `qch_reader_decompiled.c` | Decompiled `.qch` reader (`0x41cd90`). Confirms field order. |
| `qch-writer-decompiled.md` | Human-readable spec derived from the writer. |
| `qch-format-notes.md` | Earlier format notes (pre-decompilation). |
| `ebonW_00420730.c` | Decompiled generator (144 KB). Contains the fit-matrix logic. |
| `ebonW_0040da38.c` | Decompiled helper / dispatch function. |
| `parse_qch.py` | Standalone faithful `.qch` parser (reference; production version is in `pyebon/qch.py`). |

## Ghidra scripts

| File | What |
|------|------|
| `DecompAt.java` | Force-create a function at an address and decompile it. |
| `DecompFuncs.java` | Decompile the function containing given addresses. |
| `FindRefs.java` | List functions referencing given data addresses. |
| `FindImm.java` | Find immediate-value references. |
| `DecompFuncs.py` | Python version of DecompFuncs (needs PyGhidra). |
| `run_ghidra.sh` | Launcher script for headless analysis. |

Run (project already analyzed under `/tmp/ghproj2`):
```bash
GH=~/Downloads/ghidra_*/ghidra_*
"$GH/support/analyzeHeadless" /tmp/ghproj2 ebon -process EBoN.exe -noanalysis \
  -scriptPath ~/git/luis/pybook/research -postScript DecompAt.java 0x<addr>
```

## Old code (superseded by pyebon/)

| File | What |
|------|------|
| `name_generator_enhanced.py` | Original CLI name generator (simple syllable splitting). |
| `name_generator_gui.py` | Original Tkinter GUI for the old generator. |
| `cleaner.py` | Utility to strip, dedupe, and sort `.txt` chapter files. |
| `qch_explore.py` | Scratch hex/format analysis tool for `.qch` files. |
