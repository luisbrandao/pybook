#!/usr/bin/env python3
"""pyebon GUI — generate names from the Everchanging Book of Names library.

A clean two-pane Tkinter front-end over the new `pyebon` engine:
  * left  — a searchable list of every chapter (the 331 extracted library books
            plus your own chapters/*.txt seed lists),
  * right — generation controls (count, length, seed) and the results, with
            copy / save / reroll.

Run:  python3 pyebon_gui.py
Stdlib only (Tkinter); no external dependencies.
"""

from __future__ import annotations

import os
import pathlib
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont

from pyebon.library import LIBRARY_DIR, load_chapter
from pyebon.preprocess import build_chapter
from pyebon.generate import Generator, GenerationError

ROOT = pathlib.Path(__file__).resolve().parent
CHAPTERS_DIR = ROOT / "chapters"


# --------------------------------------------------------------------------- #
# Chapter discovery — library .json books + the user's chapters/*.txt lists.
# --------------------------------------------------------------------------- #
def _pretty(stem: str) -> str:
    return stem.replace("_", " ")


def discover_chapters():
    """Return a sorted list of (label, kind, path) for every available chapter."""
    items = []
    libdir = pathlib.Path(LIBRARY_DIR)
    if libdir.is_dir():
        for p in sorted(libdir.glob("*.json")):
            items.append((_pretty(p.stem), "lib", str(p)))
    if CHAPTERS_DIR.is_dir():
        for p in sorted(CHAPTERS_DIR.glob("*.txt")):
            items.append((f"{p.stem}  (txt)", "txt", str(p)))
    return items


def load_any(kind: str, path: str):
    """Load a Chapter from either a library .json or a chapters/*.txt seed list."""
    if kind == "lib":
        return load_chapter(path)
    names = [ln.strip() for ln in open(path, encoding="utf-8") if ln.strip()]
    ch = build_chapter(names)
    ch.title = pathlib.Path(path).stem
    return ch


# --------------------------------------------------------------------------- #
# The app.
# --------------------------------------------------------------------------- #
class App(tk.Tk):
    # Ivory palette.
    BG = "#F3EEDF"        # ivory base
    PANEL = "#FBF8EF"     # lighter ivory for inputs / results
    INK = "#3D372C"       # warm near-black text
    MUTED = "#9A8F77"     # hints
    ACCENT = "#A6794B"    # warm tan / sepia
    ACCENT_HOVER = "#946841"
    ACCENT_FG = "#FFFBF2"
    BORDER = "#DED4BD"
    SELECT = "#E8D9B5"    # soft gold selection

    def __init__(self):
        super().__init__()
        self.title("pyebon — Everchanging Book of Names")
        self.geometry("920x580")
        self.minsize(720, 460)
        self.configure(background=self.BG)

        try:
            ttk.Style().theme_use("clam")
        except tk.TclError:
            pass
        self._style()

        self.all_items = discover_chapters()      # (label, kind, path)
        self.view_items = list(self.all_items)     # filtered view
        self._chapter_cache = {}                   # path -> Chapter

        self._build_layout()
        self._refresh_list()
        if self.view_items:
            self.listbox.selection_set(0)
            self._on_select()

    # ---- styling -------------------------------------------------------- #
    def _style(self):
        s = ttk.Style()
        base = tkfont.nametofont("TkDefaultFont").actual()["family"]
        self.font_h = (base, 11, "bold")
        self.font_mono = self._pick_mono()

        BG, PANEL, INK, MUTED = self.BG, self.PANEL, self.INK, self.MUTED
        ACC, ACCH, ACCFG, BORDER = self.ACCENT, self.ACCENT_HOVER, self.ACCENT_FG, self.BORDER

        s.configure(".", background=BG, foreground=INK, fieldbackground=PANEL,
                    bordercolor=BORDER, lightcolor=BORDER, darkcolor=BORDER,
                    focuscolor=ACC)
        s.configure("TFrame", background=BG)
        s.configure("TLabel", background=BG, foreground=INK)
        s.configure("Hint.TLabel", background=BG, foreground=MUTED)
        s.configure("TPanedwindow", background=BG)
        s.configure("Sash", sashthickness=8, gripcount=0)

        s.configure("TEntry", fieldbackground=PANEL, bordercolor=BORDER, padding=4)
        s.configure("TSpinbox", fieldbackground=PANEL, bordercolor=BORDER, arrowsize=12, padding=2)

        # Buttons: flat tan accent with ivory text.
        s.configure("TButton", background=PANEL, foreground=INK, bordercolor=BORDER,
                    relief="flat", padding=6)
        s.map("TButton",
              background=[("active", self.SELECT)],
              bordercolor=[("active", ACC)])
        s.configure("Big.TButton", font=(base, 11, "bold"), padding=9,
                    background=ACC, foreground=ACCFG, bordercolor=ACC, relief="flat")
        s.map("Big.TButton",
              background=[("active", ACCH), ("pressed", ACCH)],
              foreground=[("active", ACCFG)])

        s.configure("Vertical.TScrollbar", background=self.SELECT, troughcolor=BG,
                    bordercolor=BG, arrowcolor=INK)

    def _pick_mono(self):
        for fam in ("DejaVu Sans Mono", "Liberation Mono", "Consolas", "Menlo", "Courier New"):
            if fam in tkfont.families():
                return (fam, 13)
        return ("TkFixedFont", 13)

    # ---- layout --------------------------------------------------------- #
    def _build_layout(self):
        outer = ttk.Frame(self, padding=10)
        outer.pack(fill=tk.BOTH, expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)

        paned = ttk.PanedWindow(outer, orient=tk.HORIZONTAL)
        paned.grid(row=0, column=0, sticky="nsew")

        # ---- left: chapter picker ----
        left = ttk.Frame(paned, padding=(0, 0, 10, 0))
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)
        paned.add(left, weight=1)
        # Restore a comfortably wide chapter column once the window is laid out.
        self.after(0, lambda: self._init_sash(paned, 360))

        ttk.Label(left, text="Chapter", font=self.font_h).grid(row=0, column=0, sticky="w")
        self.search_var = tk.StringVar()
        search = ttk.Entry(left, textvariable=self.search_var)
        search.grid(row=1, column=0, sticky="ew", pady=(4, 6))
        self._placeholder(search, "search…")

        box = ttk.Frame(left)
        box.grid(row=2, column=0, sticky="nsew")
        box.rowconfigure(0, weight=1); box.columnconfigure(0, weight=1)
        self.listbox = tk.Listbox(
            box, activestyle="none", exportselection=False,
            background=self.PANEL, foreground=self.INK,
            selectbackground=self.SELECT, selectforeground=self.INK,
            highlightthickness=1, highlightbackground=self.BORDER,
            highlightcolor=self.BORDER, borderwidth=0, relief="flat")
        self.listbox.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(box, orient="vertical", command=self.listbox.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=sb.set)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self._on_select())
        self.listbox.bind("<Double-Button-1>", lambda e: self.generate())

        self.count_label = ttk.Label(left, text="", style="Hint.TLabel")
        self.count_label.grid(row=3, column=0, sticky="w", pady=(6, 0))

        # ---- right: controls + results ----
        right = ttk.Frame(paned, padding=(10, 0, 0, 0))
        right.rowconfigure(2, weight=1)
        right.columnconfigure(0, weight=1)
        paned.add(right, weight=2)

        # info line
        self.info_var = tk.StringVar(value="")
        ttk.Label(right, textvariable=self.info_var, font=self.font_h).grid(
            row=0, column=0, sticky="w")

        # controls
        ctl = ttk.Frame(right)
        ctl.grid(row=1, column=0, sticky="ew", pady=8)
        self.count = tk.IntVar(value=20)
        self.min_len = tk.IntVar(value=3)
        self.max_len = tk.IntVar(value=14)
        self.seed = tk.StringVar(value="")
        self._spin(ctl, "Names", self.count, 1, 500, 0)
        self._spin(ctl, "Min", self.min_len, 1, 40, 2)
        self._spin(ctl, "Max", self.max_len, 2, 60, 4)
        ttk.Label(ctl, text="Seed").grid(row=0, column=6, padx=(12, 4))
        ttk.Entry(ctl, textvariable=self.seed, width=8).grid(row=0, column=7)
        ttk.Label(ctl, text="(blank = random)", style="Hint.TLabel").grid(
            row=0, column=8, padx=(4, 0))

        gen = ttk.Button(right, text="Generate  ▸", style="Big.TButton", command=self.generate)
        gen.grid(row=1, column=0, sticky="e")

        # results
        res = ttk.Frame(right)
        res.grid(row=2, column=0, sticky="nsew")
        res.rowconfigure(0, weight=1); res.columnconfigure(0, weight=1)
        self.results = tk.Text(res, font=self.font_mono, wrap="word", state="disabled",
                               background=self.PANEL, foreground=self.INK,
                               insertbackground=self.INK, relief="flat",
                               highlightthickness=1, highlightbackground=self.BORDER,
                               padx=12, pady=10, spacing1=2, spacing3=2)
        self.results.grid(row=0, column=0, sticky="nsew")
        rsb = ttk.Scrollbar(res, orient="vertical", command=self.results.yview)
        rsb.grid(row=0, column=1, sticky="ns")
        self.results.config(yscrollcommand=rsb.set)

        # bottom bar
        bar = ttk.Frame(right)
        bar.grid(row=3, column=0, sticky="ew", pady=(8, 0))
        ttk.Button(bar, text="Copy", command=self.copy).pack(side=tk.LEFT)
        ttk.Button(bar, text="Save…", command=self.save).pack(side=tk.LEFT, padx=6)
        self.status = ttk.Label(bar, text="", style="Hint.TLabel")
        self.status.pack(side=tk.RIGHT)

        # wire live search now that the listbox exists
        self.search_var.trace_add("write", lambda *_: self._refresh_list())

        # shortcuts
        self.bind("<Control-g>", lambda e: self.generate())
        self.bind("<Return>", lambda e: self.generate())

    def _init_sash(self, paned, x):
        try:
            paned.sashpos(0, x)
        except tk.TclError:
            pass

    def _spin(self, parent, label, var, lo, hi, col):
        ttk.Label(parent, text=label).grid(row=0, column=col, padx=(0 if col == 0 else 12, 4))
        ttk.Spinbox(parent, from_=lo, to=hi, textvariable=var, width=5).grid(row=0, column=col + 1)

    def _placeholder(self, entry, text):
        def on_focus_in(_):
            if entry.get() == text:
                entry.delete(0, tk.END); entry.config(foreground=self.INK)
        def on_focus_out(_):
            if not entry.get():
                entry.insert(0, text); entry.config(foreground=self.MUTED)
        entry.insert(0, text); entry.config(foreground=self.MUTED)
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        self._ph_text = text

    # ---- chapter list --------------------------------------------------- #
    def _query(self):
        q = self.search_var.get().strip().lower()
        return "" if q in ("", "search…") else q

    def _refresh_list(self):
        q = self._query()
        self.view_items = [it for it in self.all_items if q in it[0].lower()] if q else list(self.all_items)
        self.listbox.delete(0, tk.END)
        for label, kind, _ in self.view_items:
            self.listbox.insert(tk.END, ("📖 " if kind == "lib" else "✎ ") + label)
        self.count_label.config(text=f"{len(self.view_items)} of {len(self.all_items)} chapters")
        if self.view_items:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)

    def _selected(self):
        sel = self.listbox.curselection()
        return self.view_items[sel[0]] if sel else None

    def _get_chapter(self, kind, path):
        if path not in self._chapter_cache:
            self._chapter_cache[path] = load_any(kind, path)
        return self._chapter_cache[path]

    def _on_select(self):
        it = self._selected()
        if not it:
            return
        label, kind, path = it
        try:
            ch = self._get_chapter(kind, path)
        except Exception as exc:
            self.info_var.set(label)
            self.status.config(text=f"load error: {exc}")
            return
        title = ch.title or label
        author = (ch.author or "").strip()
        meta = f"  ·  {author}" if author and author not in ("0", "-") else ""
        self.info_var.set(title + meta)
        self.status.config(
            text=f"{len(ch.vowel_elements)} vowel · {len(ch.cons_elements)} cons · "
                 f"{len(ch.structures)} structures · fit {ch.opts.fit}")

    # ---- generation ----------------------------------------------------- #
    def generate(self):
        it = self._selected()
        if not it:
            messagebox.showinfo("Pick a chapter", "Select a chapter on the left first.")
            return
        label, kind, path = it
        try:
            ch = self._get_chapter(kind, path)
        except Exception as exc:
            messagebox.showerror("Could not load chapter", str(exc))
            return

        seed_txt = self.seed.get().strip()
        seed = int(seed_txt) if seed_txt.lstrip("-").isdigit() else None
        lo, hi = self.min_len.get(), self.max_len.get()
        if lo > hi:
            lo, hi = hi, lo
        g = Generator(ch, seed=seed)

        names, misses = [], 0
        for _ in range(self.count.get()):
            try:
                names.append(g.generate(lo, hi))
            except GenerationError:
                misses += 1
        self._show(names)
        note = f"{len(names)} names from “{ch.title or label}”"
        if misses:
            note += f"  ({misses} couldn’t fit the length bounds)"
        self.status.config(text=note)

    def _show(self, names):
        self.results.config(state="normal")
        self.results.delete("1.0", tk.END)
        self.results.insert(tk.END, "\n".join(names))
        self.results.config(state="disabled")

    def _results_text(self):
        return self.results.get("1.0", "end-1c")

    def copy(self):
        txt = self._results_text()
        if not txt.strip():
            return
        self.clipboard_clear(); self.clipboard_append(txt)
        self.status.config(text="copied to clipboard")

    def save(self):
        txt = self._results_text()
        if not txt.strip():
            return
        it = self._selected()
        default = (it[0].split("  ")[0] if it else "names").replace(" ", "_") + ".txt"
        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=default,
                                            filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if path:
            open(path, "w", encoding="utf-8").write(txt + "\n")
            self.status.config(text=f"saved {path}")


def main():
    if not pathlib.Path(LIBRARY_DIR).is_dir() and not CHAPTERS_DIR.is_dir():
        print("No chapters found. Run: python3 -m pyebon.library extract")
        return
    App().mainloop()


if __name__ == "__main__":
    main()
