#!/bin/bash
# Headless Ghidra driver for EBoN.exe reverse engineering.
# Usage:
#   re/run_ghidra.sh import           # one-time: import + analyze into project
#   re/run_ghidra.sh decomp ADDR...   # decompile funcs at hex addrs (reuses project)
set -u
GH=/home/techmago/Downloads/ghidra_12.1.2_PUBLIC_20260605/ghidra_12.1.2_PUBLIC
HEADLESS="$GH/support/analyzeHeadless"
PROJDIR=/tmp/ghproj
PROJ=ebon
REPO=/dados/techmago/git/luis/pybook
SCRIPTS="$REPO/re"
LOG=/tmp/ghidra_run.log

cmd="${1:-}"; shift || true

case "$cmd" in
  import)
    rm -rf "$PROJDIR"; mkdir -p "$PROJDIR"
    "$HEADLESS" "$PROJDIR" "$PROJ" \
      -import "$REPO/Ebon/EBoN.exe" \
      -scriptPath "$SCRIPTS" \
      > "$LOG" 2>&1
    echo "IMPORT DONE rc=$?" >> "$LOG"
    ;;
  decomp)
    "$HEADLESS" "$PROJDIR" "$PROJ" \
      -process EBoN.exe -noanalysis \
      -scriptPath "$SCRIPTS" \
      -postScript DecompFuncs.py "$@" \
      > "$LOG" 2>&1
    echo "DECOMP DONE rc=$?" >> "$LOG"
    ;;
  *)
    echo "usage: $0 import | decomp ADDR..." ;;
esac
