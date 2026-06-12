#!/usr/bin/env bash
# Install the PyEBoN desktop launcher for the current checkout.
# Resolves this repo's location and your python3, fills them into the
# .desktop template, and drops it in your user applications folder.
# Re-run any time the repo moves. Uninstall: ./install.sh --uninstall
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APPS="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
TARGET="$APPS/pyebon.desktop"

if [ "${1:-}" = "--uninstall" ]; then
    rm -f "$TARGET"
    echo "Removed $TARGET"
    command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true
    exit 0
fi

PYTHON="$(command -v python3 || true)"
if [ -z "$PYTHON" ]; then
    echo "error: python3 not found on PATH" >&2
    exit 1
fi

mkdir -p "$APPS"
sed -e "s|__PYTHON__|$PYTHON|g" -e "s|__DIR__|$DIR|g" \
    "$DIR/assets/pyebon.desktop" > "$TARGET"
chmod +x "$TARGET"

command -v update-desktop-database >/dev/null && update-desktop-database "$APPS" 2>/dev/null || true

echo "Installed PyEBoN launcher -> $TARGET"
echo "  python: $PYTHON"
echo "  repo:   $DIR"
echo "Look for 'PyEBoN' in your application menu."
