#!/usr/bin/env python3
"""pyebon GUI — generate names from the Everchanging Book of Names library.

A clean Tkinter front-end over the new `pyebon` engine, in two tabs:
  * Generate — a searchable list of every chapter (the 331 extracted library
            books plus your own data/seeds/*.txt seed lists) on the left, and
            generation controls (count, length, fit, seed) with the results on
            the right, with copy / save.
  * Build a chapter — paste or load a list of seed names, preview the chapter
            it makes (stats + sample names), and save it into data/seeds/ so
            it shows up in the Generate tab.

Run:  python3 pyebon_gui.py
Stdlib only (Tkinter); no external dependencies.
"""

from __future__ import annotations

import os
import pathlib
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font as tkfont

from pyebon.library import LIBRARY_DIR, load_chapter
from pyebon.preprocess import build_chapter
from pyebon.generate import Generator, GenerationError
from pyebon.splitting import split_elements

ROOT = pathlib.Path(__file__).resolve().parent
CHAPTERS_DIR = ROOT / "data" / "seeds"


# --------------------------------------------------------------------------- #
# Chapter discovery — library .json books + the user's data/seeds/*.txt lists.
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
    """Load a Chapter from either a library .json or a data/seeds/*.txt seed list."""
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
        # Open maximized; the geometry below is the fallback (double the old
        # 920x580 default, clamped to the screen) for WMs that ignore -zoomed.
        w = min(1840, self.winfo_screenwidth())
        h = min(1160, self.winfo_screenheight())
        self.geometry(f"{w}x{h}")
        self.minsize(720, 460)
        try:
            self.attributes("-zoomed", True)   # maximize (X11 / XWayland)
        except tk.TclError:
            pass
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

        s.configure("TCheckbutton", background=BG, foreground=INK)
        s.map("TCheckbutton", background=[("active", BG)])
        s.configure("TCombobox", fieldbackground=PANEL, background=PANEL,
                    bordercolor=BORDER, arrowcolor=INK)
        s.map("TCombobox", fieldbackground=[("readonly", PANEL)],
              foreground=[("readonly", INK)])

        s.configure("TNotebook", background=BG, bordercolor=BORDER, tabmargins=(0, 4, 0, 0))
        s.configure("TNotebook.Tab", background=BG, foreground=MUTED,
                    padding=(14, 6), bordercolor=BORDER)
        s.map("TNotebook.Tab",
              background=[("selected", PANEL)],
              foreground=[("selected", INK)])

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

        self.notebook = ttk.Notebook(outer)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        gen_tab = ttk.Frame(self.notebook, padding=(0, 8, 0, 0))
        self.notebook.add(gen_tab, text="Generate")
        build_tab = ttk.Frame(self.notebook, padding=(0, 8, 0, 0))
        self.notebook.add(build_tab, text="Build a chapter")
        self._build_builder(build_tab)

        gen_tab.columnconfigure(0, weight=1)
        gen_tab.rowconfigure(0, weight=1)
        paned = ttk.PanedWindow(gen_tab, orient=tk.HORIZONTAL)
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

        # info line (title on the left, a help "?" pinned to the right corner)
        inforow = ttk.Frame(right)
        inforow.grid(row=0, column=0, sticky="ew")
        inforow.columnconfigure(0, weight=1)
        self.info_var = tk.StringVar(value="")
        ttk.Label(inforow, textvariable=self.info_var, font=self.font_h).grid(
            row=0, column=0, sticky="w")
        ttk.Button(inforow, text="?", width=2, command=self._show_help).grid(
            row=0, column=1, sticky="e")

        # controls — row 0: amount/length/seed
        ctl = ttk.Frame(right)
        ctl.grid(row=1, column=0, sticky="ew", pady=8)
        self.count = tk.IntVar(value=35)
        self.min_len = tk.IntVar(value=3)
        self.max_len = tk.IntVar(value=14)
        self.seed = tk.StringVar(value="")
        self._spin(ctl, "Names", self.count, 1, 500, 0)
        self._spin(ctl, "Min", self.min_len, 1, 40, 2)
        self._spin(ctl, "Max", self.max_len, 2, 60, 4)
        ttk.Label(ctl, text="Seed").grid(row=0, column=6, padx=(12, 4))
        ttk.Entry(ctl, textvariable=self.seed, width=8).grid(row=0, column=7)
        ttk.Label(ctl, text="(blank = random)", style="Hint.TLabel").grid(
            row=0, column=8, padx=(4, 0), sticky="w")

        # controls — row 1: fit level, prefix/suffix, Generate
        self.FIT_LABELS = ["0 — loose", "1 — adjacency", "2 — skip C", "3 — skip C+V"]
        self.fit_var = tk.StringVar(value=self.FIT_LABELS[1])
        self.use_prefix = tk.BooleanVar(value=False)
        self.use_suffix = tk.BooleanVar(value=False)
        ttk.Label(ctl, text="Fit").grid(row=1, column=0, sticky="w", pady=(8, 0))
        fit_box = ttk.Combobox(ctl, textvariable=self.fit_var, values=self.FIT_LABELS,
                               state="readonly", width=13)
        fit_box.grid(row=1, column=1, columnspan=3, sticky="w", pady=(8, 0))
        ttk.Checkbutton(ctl, text="Prefix", variable=self.use_prefix).grid(
            row=1, column=4, columnspan=2, sticky="w", padx=(12, 0), pady=(8, 0))
        ttk.Checkbutton(ctl, text="Suffix", variable=self.use_suffix).grid(
            row=1, column=6, columnspan=2, sticky="w", pady=(8, 0))
        ctl.columnconfigure(8, weight=1)
        ttk.Button(ctl, text="Generate  ▸", style="Big.TButton", command=self.generate).grid(
            row=1, column=8, sticky="e", pady=(8, 0))

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
        self.edit_btn = ttk.Button(bar, text="Edit chapter", command=self.edit_selected)
        self.edit_btn.pack(side=tk.LEFT)
        self.status = ttk.Label(bar, text="", style="Hint.TLabel")
        self.status.pack(side=tk.RIGHT)

        # wire live search now that the listbox exists
        self.search_var.trace_add("write", lambda *_: self._refresh_list())

        # shortcuts
        self.bind("<Control-g>", lambda e: self.generate())
        self.bind("<Return>", self._on_return)
        # Tk has no select-all by default (Ctrl+A means "line start"); fix that
        # everywhere: the seed editor, results/preview boxes, entries, spinboxes.
        self.bind_class("Text", "<Control-a>", self._select_all_text)
        for cls in ("TEntry", "TSpinbox"):
            self.bind_class(cls, "<Control-a>", self._select_all_entry)

    @staticmethod
    def _select_all_text(event):
        event.widget.tag_add("sel", "1.0", "end-1c")
        event.widget.mark_set("insert", "1.0")
        return "break"

    @staticmethod
    def _select_all_entry(event):
        event.widget.select_range(0, tk.END)
        return "break"

    def _on_return(self, event):
        # Return inside a Text widget (the seed editor) just inserts a newline.
        if isinstance(event.widget, tk.Text):
            return
        if self.notebook.index(self.notebook.select()) == 1:
            self.preview_chapter()
        else:
            self.generate()

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
        self.edit_btn.config(state="normal" if kind == "txt" else "disabled")
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

        # Reflect this chapter's native options in the controls.
        self.fit_var.set(self.FIT_LABELS[max(0, min(3, ch.opts.fit))])
        self.use_prefix.set(bool(ch.opts.prefix) and bool(ch.prefixes))
        self.use_suffix.set(bool(ch.opts.suffix) and bool(ch.suffixes))

        skip = " · skip-fit data" if ch.adj2 else " · no skip-data (fit 2/3 = 1)"
        self.status.config(
            text=f"{len(ch.vowel_elements)} vowel · {len(ch.cons_elements)} cons · "
                 f"{len(ch.structures)} structures{skip}")

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

        # Apply the fit / prefix / suffix controls to this chapter's options.
        ch.opts.fit = int(self.fit_var.get()[0])
        ch.opts.prefix = self.use_prefix.get()
        ch.opts.suffix = self.use_suffix.get()

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

    def _show_help(self):
        win = tk.Toplevel(self)
        win.title("About the options")
        win.configure(background=self.BG)
        win.transient(self); win.resizable(False, False)
        frame = ttk.Frame(win, padding=16)
        frame.pack(fill=tk.BOTH, expand=True)

        def section(title, body):
            ttk.Label(frame, text=title, font=self.font_h).pack(anchor="w", pady=(8, 2))
            ttk.Label(frame, text=body, justify="left", wraplength=440,
                      style="Hint.TLabel").pack(anchor="w")

        ttk.Label(frame, text="How names are made", font=(self.font_h[0], 13, "bold")).pack(anchor="w")
        ttk.Label(frame, wraplength=440, justify="left", style="Hint.TLabel",
                  text="Each name is built from chunks (vowel runs and consonant runs) "
                       "taken from the chapter, arranged into a shape seen in the "
                       "source names.").pack(anchor="w", pady=(2, 0))

        section("Fit — how closely a name must echo the source",
                "0  loose: any chunk can go anywhere. Most variety, least authentic.\n"
                "1  adjacency: a chunk may only follow another chunk if that pairing "
                "was actually seen in the source.\n"
                "2  skip-C: also checks consonants one step apart (consonant-skip-vowel).\n"
                "3  skip-C+V: also checks vowels one step apart. Strictest, most authentic, "
                "fewest possible names.\n"
                "Note: the imported library books carry no skip data, so 2 and 3 behave "
                "like 1 for them. Your own seed lists support all four.")

        section("Prefix / Suffix — believable starts and ends",
                "Prefix forces the first two chunks to be a real opening seen in the "
                "source; Suffix forces the last two to be a real ending. Turn them on "
                "for names that begin and end like the originals.")

        ttk.Button(frame, text="Close", command=win.destroy).pack(anchor="e", pady=(14, 0))
        win.bind("<Escape>", lambda e: win.destroy())
        win.update_idletasks()
        # center over the main window
        x = self.winfo_rootx() + (self.winfo_width() - win.winfo_width()) // 2
        y = self.winfo_rooty() + 80
        win.geometry(f"+{max(0, x)}+{max(0, y)}")

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

    # ---- chapter builder tab --------------------------------------------- #
    def _build_builder(self, tab):
        tab.columnconfigure(0, weight=3)
        tab.columnconfigure(1, weight=2)
        tab.rowconfigure(2, weight=1)

        # left: the seed-name editor
        self.edit_path = None                      # file currently being edited
        hdr = ttk.Frame(tab)
        hdr.grid(row=0, column=0, sticky="ew", padx=(0, 12))
        hdr.columnconfigure(0, weight=1)
        ttk.Label(hdr, text="Seed names", font=self.font_h).grid(row=0, column=0, sticky="w")
        self.edit_label = ttk.Label(hdr, text="new chapter", style="Hint.TLabel")
        self.edit_label.grid(row=0, column=1, sticky="e")
        ttk.Label(tab, text="One name per line. The more you give (30+), the richer the chapter.",
                  style="Hint.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 6))

        seedbox = ttk.Frame(tab)
        seedbox.grid(row=2, column=0, sticky="nsew", padx=(0, 12))
        seedbox.rowconfigure(0, weight=1); seedbox.columnconfigure(0, weight=1)
        self.seed_text = tk.Text(seedbox, font=self.font_mono, wrap="none", undo=True,
                                 background=self.PANEL, foreground=self.INK,
                                 insertbackground=self.INK, relief="flat",
                                 highlightthickness=1, highlightbackground=self.BORDER,
                                 padx=12, pady=10, spacing1=1, spacing3=1)
        self.seed_text.grid(row=0, column=0, sticky="nsew")
        ssb = ttk.Scrollbar(seedbox, orient="vertical", command=self.seed_text.yview)
        ssb.grid(row=0, column=1, sticky="ns")
        self.seed_text.config(yscrollcommand=ssb.set)
        self.seed_text.bind("<<Modified>>", self._on_seed_edit)
        self.seed_text.tag_configure("odd", background="#F2DCC4")   # soft amber

        seedbar = ttk.Frame(tab)
        seedbar.grid(row=3, column=0, sticky="ew", pady=(8, 0), padx=(0, 12))
        ttk.Button(seedbar, text="Load .txt…", command=self.load_seed_file).pack(side=tk.LEFT)
        ttk.Button(seedbar, text="Trim", command=self.trim_seeds).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(seedbar, text="Sort", command=self.sort_seeds).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(seedbar, text="Dedup", command=self.dedup_seeds).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(seedbar, text="Odd first", command=self.find_problems).pack(side=tk.LEFT, padx=(6, 0))
        ttk.Button(seedbar, text="Clear", command=lambda: self._set_editor("")).pack(
            side=tk.LEFT, padx=(6, 0))
        self.seed_count = ttk.Label(seedbar, text="0 names", style="Hint.TLabel")
        self.seed_count.pack(side=tk.RIGHT)

        # right: preview + save
        ttk.Label(tab, text="Preview", font=self.font_h).grid(row=0, column=1, sticky="w")
        self.build_stats = tk.StringVar(value="Paste some names, then hit Preview.")
        ttk.Label(tab, textvariable=self.build_stats, style="Hint.TLabel",
                  wraplength=380, justify="left").grid(row=1, column=1, sticky="w", pady=(2, 6))

        prevbox = ttk.Frame(tab)
        prevbox.grid(row=2, column=1, sticky="nsew")
        prevbox.rowconfigure(0, weight=1); prevbox.columnconfigure(0, weight=1)
        self.preview_box = tk.Text(prevbox, font=self.font_mono, wrap="word", state="disabled",
                                   background=self.PANEL, foreground=self.INK,
                                   relief="flat", highlightthickness=1,
                                   highlightbackground=self.BORDER,
                                   padx=12, pady=10, spacing1=2, spacing3=2)
        self.preview_box.grid(row=0, column=0, sticky="nsew")
        psb = ttk.Scrollbar(prevbox, orient="vertical", command=self.preview_box.yview)
        psb.grid(row=0, column=1, sticky="ns")
        self.preview_box.config(yscrollcommand=psb.set)

        prevbar = ttk.Frame(tab)
        prevbar.grid(row=3, column=1, sticky="ew", pady=(8, 0))
        ttk.Button(prevbar, text="Preview  ▸", style="Big.TButton",
                   command=self.preview_chapter).pack(side=tk.LEFT)
        ttk.Button(prevbar, text="Save", command=self.save_seed_chapter).pack(
            side=tk.LEFT, padx=(8, 0))
        ttk.Button(prevbar, text="Save as…",
                   command=lambda: self.save_seed_chapter(save_as=True)).pack(
            side=tk.LEFT, padx=(6, 0))
        self.build_status = ttk.Label(prevbar, text="", style="Hint.TLabel")
        self.build_status.pack(side=tk.RIGHT)

    def _seed_lines(self):
        return [ln.strip() for ln in self.seed_text.get("1.0", "end-1c").splitlines() if ln.strip()]

    def _on_seed_edit(self, _event=None):
        if self.seed_text.edit_modified():
            self.seed_count.config(text=f"{len(self._seed_lines())} names")
            self.seed_text.edit_modified(False)

    def _set_editor(self, text, path=None):
        """Fill the seed editor and remember which file (if any) it edits."""
        self.seed_text.delete("1.0", tk.END)
        if text:
            self.seed_text.insert("1.0", text)
        self.edit_path = pathlib.Path(path).resolve() if path else None
        self.edit_label.config(
            text=f"editing  {self.edit_path.name}" if self.edit_path else "new chapter")

    def load_seed_file(self):
        path = filedialog.askopenfilename(initialdir=str(CHAPTERS_DIR),
                                          filetypes=[("Text", "*.txt"), ("All", "*.*")])
        if not path:
            return
        try:
            text = open(path, encoding="utf-8").read()
        except Exception as exc:
            messagebox.showerror("Could not read file", str(exc))
            return
        self._set_editor(text, path)
        self.build_status.config(text=f"loaded {pathlib.Path(path).name}")

    def edit_selected(self):
        """Open the chapter selected on the Generate tab in the builder."""
        it = self._selected()
        if not it:
            return
        label, kind, path = it
        if kind != "txt":
            messagebox.showinfo(
                "Library book",
                "Library books are compiled — they carry derived statistics, not "
                "the original name list, so there is nothing to edit. Only your "
                "data/seeds/*.txt chapters can be edited.")
            return
        try:
            text = open(path, encoding="utf-8").read()
        except Exception as exc:
            messagebox.showerror("Could not read file", str(exc))
            return
        self._set_editor(text, path)
        self.build_status.config(text=f"loaded {pathlib.Path(path).name}")
        self.notebook.select(1)

    def trim_seeds(self):
        """Clean pasted text down to one bare name per line: drop <tags>, split
        on separators (, ; / \\ | tab), keep only letters/space/hyphen/apostrophe,
        collapse whitespace and blank lines."""
        raw = self.seed_text.get("1.0", "end-1c")
        before = len(self._seed_lines())
        raw = re.sub(r"<[^>]*>", " ", raw)
        out = []
        for chunk in re.split(r"[\n,;/\\|\t]+", raw):
            name = "".join(c if (c.isalpha() or c in " '-") else " " for c in chunk)
            name = re.sub(r"\s+", " ", name).strip(" '-")
            if name:
                out.append(name.title())   # fix case: KHAL DROGO -> Khal Drogo
        self._set_editor("\n".join(out), self.edit_path)
        self.build_status.config(text=f"trimmed: {before} lines → {len(out)} names")

    @staticmethod
    def _looks_odd(name):
        """A name that probably needs a human look: spaces or any non-letter
        character in it, or stray uppercase past the first letter (KHAL)."""
        return (any(not c.isalpha() for c in name)
                or any(c.isupper() for c in name[1:]))

    def find_problems(self):
        lines = self._seed_lines()
        odd = [n for n in lines if self._looks_odd(n)]
        if not odd:
            self.build_status.config(text="no odd names found")
            return
        clean = [n for n in lines if not self._looks_odd(n)]
        self._set_editor("\n".join(odd + clean), self.edit_path)
        self.seed_text.tag_add("odd", "1.0", f"{len(odd)}.end")
        self.seed_text.mark_set("insert", "1.0")
        self.seed_text.see("1.0")
        self.build_status.config(
            text=f"{len(odd)} odd name{'s' if len(odd) != 1 else ''} moved to the top")

    def sort_seeds(self):
        lines = self._seed_lines()
        self._set_editor("\n".join(sorted(lines, key=str.casefold)), self.edit_path)
        self.build_status.config(text=f"sorted {len(lines)} names")

    def dedup_seeds(self):
        lines = self._seed_lines()
        seen, out = set(), []
        for name in lines:
            key = name.casefold()
            if key not in seen:
                seen.add(key)
                out.append(name)
        removed = len(lines) - len(out)
        self._set_editor("\n".join(out), self.edit_path)
        self.build_status.config(
            text=f"removed {removed} duplicate{'s' if removed != 1 else ''}"
            if removed else "no duplicates")

    def _build_from_editor(self):
        """Build a Chapter from the editor; returns (chapter, used, skipped) or None."""
        lines = self._seed_lines()
        usable = [n for n in lines if len(split_elements(n)) >= 2]
        if len(usable) < 2:
            messagebox.showinfo(
                "Not enough names",
                "Give at least two usable seed names (a name needs both vowels "
                "and consonants).")
            return None
        return build_chapter(usable), len(usable), len(lines) - len(usable)

    def preview_chapter(self):
        built = self._build_from_editor()
        if not built:
            return
        ch, used, skipped = built
        self.build_stats.set(
            f"{used} seeds" + (f" ({skipped} skipped — all-vowel/all-consonant)" if skipped else "")
            + f"  ·  {len(ch.vowel_elements)} vowel · {len(ch.cons_elements)} cons · "
              f"{len(ch.structures)} structures · full skip-fit data")

        g = Generator(ch)
        names, misses = [], 0
        for _ in range(35):
            try:
                names.append(g.generate(3, 14))
            except GenerationError:
                misses += 1
        self.preview_box.config(state="normal")
        self.preview_box.delete("1.0", tk.END)
        self.preview_box.insert(tk.END, "\n".join(names))
        self.preview_box.config(state="disabled")
        note = f"{len(names)} sample names (fit 3)"
        if misses:
            note += f", {misses} misses"
        self.build_status.config(text=note)

    def save_seed_chapter(self, save_as=False):
        lines = self._seed_lines()
        if not lines:
            messagebox.showinfo("Nothing to save", "The seed list is empty.")
            return
        if save_as or not self.edit_path:
            CHAPTERS_DIR.mkdir(parents=True, exist_ok=True)
            path = filedialog.asksaveasfilename(
                initialdir=str(CHAPTERS_DIR), defaultextension=".txt",
                initialfile=self.edit_path.name if self.edit_path else "my_chapter.txt",
                filetypes=[("Text", "*.txt"), ("All", "*.*")])
            if not path:
                return
            is_new = True
        else:
            path = str(self.edit_path)
            is_new = False
        open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")

        p = pathlib.Path(path).resolve()
        self.edit_path = p
        self.edit_label.config(text=f"editing  {p.name}")
        # Drop any cached build of this file so the Generate tab sees the edit.
        self._chapter_cache.pop(path, None)
        self._chapter_cache.pop(str(p), None)

        if p.parent != CHAPTERS_DIR.resolve():
            self.build_status.config(text=f"saved {p.name} (outside data/seeds — won't be listed)")
            return

        if not is_new:
            # In-place save while editing: stay on the builder.
            self.build_status.config(text=f"saved {p.name}")
            return

        # A new chapter: refresh the Generate tab and jump to it.
        self.all_items = discover_chapters()
        self.search_var.set("")
        self._refresh_list()
        for i, (_label, _kind, ipath) in enumerate(self.view_items):
            if pathlib.Path(ipath) == p:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(i)
                self.listbox.see(i)
                self._on_select()
                break
        self.build_status.config(text=f"saved {p.name}")
        self.notebook.select(0)


def main():
    if not pathlib.Path(LIBRARY_DIR).is_dir() and not CHAPTERS_DIR.is_dir():
        print("No chapters found. Run: python -m pyebon.library extract")
        return
    App().mainloop()


if __name__ == "__main__":
    main()
