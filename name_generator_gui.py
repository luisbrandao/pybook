
#!/usr/bin/env python3
# GUI for the Enhanced Custom Random Name Generator.
#
# * Lists all *.txt “chapter” files found in the current directory.
# * Generates 20 new names (using name_generator_enhanced.py) on demand.
# * Displays names in a listbox; press the button again to refresh.

import tkinter as tk
from tkinter import ttk, messagebox
import pathlib
import importlib
import sys

# --- import the enhanced generator ---------------------------------------- #
try:
    nge = importlib.import_module("name_generator_enhanced")
except ModuleNotFoundError:
    messagebox.showerror(
        "Module not found",
        "Could not import 'name_generator_enhanced.py'. "
        "Make sure it is in the same folder.",
    )
    sys.exit(1)

COUNT = 20  # number of names per click


def available_chapters():
    """Return a sorted list of *.txt filenames in the chapters directory."""
    chapters_dir = pathlib.Path('./chapters')
    if not chapters_dir.exists():
        return []
    return sorted(p.name for p in chapters_dir.glob('*.txt'))


class NameGenApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Custom Name Generator")
        self.geometry("600x410")
        self.resizable(False, False)

        # Left pane: chapter files
        left = ttk.Frame(self, padding=10)
        left.pack(side=tk.LEFT, fill=tk.Y)

        ttk.Label(left, text="Chapters (.txt)", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W)
        self.chapter_box = tk.Listbox(left, height=15, exportselection=False)
        self.chapter_box.pack(fill=tk.Y, expand=True, pady=5)

        self.refresh_chapters()

        gen_btn = ttk.Button(left, text=f"Generate {COUNT} names", command=self.generate)
        gen_btn.pack(pady=(10, 0))

        # Right pane: generated names
        right = ttk.Frame(self, padding=10)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        ttk.Label(right, text="Generated names", font=("TkDefaultFont", 10, "bold")).pack(anchor=tk.W)
        self.names_box = tk.Listbox(right, height=20)
        self.names_box.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Double‑click a chapter to generate
        self.chapter_box.bind("<Double-Button-1>", lambda e: self.generate())

    def refresh_chapters(self):
        self.chapter_box.delete(0, tk.END)
        for chap in available_chapters():
            self.chapter_box.insert(tk.END, chap)
        if self.chapter_box.size():
            self.chapter_box.selection_set(0)

    def selected_chapter(self):
        sel = self.chapter_box.curselection()
        return None if not sel else self.chapter_box.get(sel[0])

    def generate(self):
        chapter = self.selected_chapter()
        if not chapter:
            messagebox.showwarning("No chapter selected", "Please select a chapter file first.")
            return
        path = pathlib.Path('./chapters') / chapter
        try:
            with path.open(encoding="utf-8") as fh:
                names = [ln.strip() for ln in fh if ln.strip()]
            pools = nge.build_weighted_pools(names)
            new_names = [nge.generate_name(pools, 2, 20) for _ in range(COUNT)]
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            return

        self.names_box.delete(0, tk.END)
        for nm in new_names:
            self.names_box.insert(tk.END, nm)


if __name__ == "__main__":
    NameGenApp().mainloop()
