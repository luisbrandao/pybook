# Reverse-engineering scratch

Ghidra headless RE of `EBoN.exe` (Borland C++ Builder, 1998).

- `qch_writer_decompiled.c` — decompiled `.qch` writer @ `0x41b6e1`. Defines the
  exact on-disk format. See `Doc/qch-writer-decompiled.md` for the spec.
- `DecompAt.java` — Ghidra headless script: force-create a function at an address
  (clearing any merged-function overlap) and decompile it to `/tmp/ebonW_<addr>.c`.
- `DecompFuncs.java` — decompile the function *containing* given addresses.
- `FindRefs.java` — list functions referencing given data addresses.

Run (project already analyzed under /tmp/ghproj2):
    GH=~/Downloads/ghidra_*/ghidra_*; \
    "$GH/support/analyzeHeadless" /tmp/ghproj2 ebon -process EBoN.exe -noanalysis \
      -scriptPath re -postScript DecompAt.java 0x<addr>
