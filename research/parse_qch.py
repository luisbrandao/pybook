#!/usr/bin/env python3
TRACE=False
"""Faithful .qch parser following the decompiled writer (EBoN.exe:0x41b6e1).

Exploratory: parses the exact on-disk sequence and prints labeled fields.
Success criterion: the parser consumes the stream and lands exactly on the
trailing '#END' marker. Run on known chapters (debug/Luis/klingon) to interpret
the lists empirically against ground truth.
"""
import sys, struct

class R:
    def __init__(self, buf):
        self.b = buf; self.p = 0
    def u8(self):
        v = self.b[self.p]; self.p += 1; return v
    def u16(self):  # BIG-ENDIAN (writer does divmod 256, hi then lo)
        hi = self.b[self.p]; lo = self.b[self.p+1]; self.p += 2
        return hi*256 + lo
    def cstr(self):
        e = self.b.index(b"\x00", self.p)
        s = self.b[self.p:e].decode("latin-1"); self.p = e+1; return s
    def raw(self, n):
        v = self.b[self.p:self.p+n]; self.p += n; return v

def parse(path, verbose=True):
    r = R(open(path, "rb").read())
    out = {}
    r.p = 3  # 3-byte preamble: byte0 + u16 (file-type/len marker)
    # 1 magic + 5 metadata strings
    out["magic"] = r.cstr()
    out["title"] = r.cstr()
    out["line2"] = r.cstr()
    out["line3"] = r.cstr()
    out["line4"] = r.cstr()
    out["author"] = r.cstr()
    # GENOPT
    out["flags"] = r.u8()
    out["fit"] = r.u8()
    out["val"] = r.u8()
    out["opt3"] = r.u8()
    out["opt4"] = r.u8()
    out["opt5"] = r.u8()
    # consonant alphabet
    out["consonants"] = r.cstr()
    # u16 f[0x3c]
    out["p3c"] = r.u16()
    # u8 nV (inner matrix dim), u8 n68
    nV = r.u8(); out["nV"] = nV
    n68 = r.u8(); out["n68"] = n68
    out["list68"] = [(r.cstr(), r.u8()) for _ in range(n68)]
    # u8 n44 + strings
    n44 = r.u8(); out["n44"] = n44
    out["list44"] = [r.cstr() for _ in range(n44)]
    # MATRIX M1 [n44 x nV] BE16
    out["M1"] = [[r.u16() for _ in range(nV)] for _ in range(n44)]
    # u16 n48 + strings + MATRIX M2 [n48 x nV]
    n48 = r.u16(); out["n48"] = n48
    out["list48"] = [r.cstr() for _ in range(n48)]
    out["M2"] = [[r.u16() for _ in range(nV)] for _ in range(n48)]
    if TRACE: print(f"  [after M2 @ {r.p:#x}]")
    # u8 ne04 + strings
    ne04 = r.u8(); out["ne04"] = ne04
    out["list_e04"] = [r.cstr() for _ in range(ne04)]
    if TRACE: print(f"  [ne04={ne04} @ {r.p:#x}]")
    # prefix: u16 nPre, then nPre*(3-byte key: elemA, elemB, typeTag), then nPre u16 freqs
    nPre = r.u16(); out["nPre"] = nPre
    if TRACE: print(f"  [nPre={nPre} @ {r.p:#x}]")
    out["pre_keys"] = [(r.u8(), r.u8(), r.u8()) for _ in range(nPre)]
    out["pre_freq"] = [r.u16() for _ in range(nPre)]
    if TRACE: print(f"  [after pre @ {r.p:#x}] keys={out['pre_keys']} freq={out['pre_freq']}")
    # suffix
    nSuf = r.u16(); out["nSuf"] = nSuf
    if TRACE: print(f"  [nSuf={nSuf} @ {r.p:#x}]")
    out["suf_keys"] = [(r.u8(), r.u8(), r.u8()) for _ in range(nSuf)]
    out["suf_freq"] = [r.u16() for _ in range(nSuf)]
    if TRACE: print(f"  [after suf @ {r.p:#x}] keys={out['suf_keys']} freq={out['suf_freq']}")
    # structures: u8 maxS1 = maxidx+1, then maxS1 u16 struct freqs
    maxS = r.u8(); out["nStruct"] = maxS
    out["struct_freq"] = [r.u16() for _ in range(maxS)]
    # substructure counts per structure
    out["sub_counts"] = [r.u16() for _ in range(maxS)]
    # substructure freqs matrix
    out["sub_freq"] = [[r.u16() for _ in range(out["sub_counts"][i])] for i in range(maxS)]
    # substructure labels
    out["sub_labels"] = [[r.cstr() for _ in range(out["sub_counts"][i])] for i in range(maxS)]
    out["after_sub_pos"] = r.p
    # bitpacked masks (we just skip by computing sizes)
    def bits(nrows, nflags):
        per = (nflags + 7)//8
        return r.raw(nrows*per)
    out["mask1"] = bits(n44, 0x40)
    out["mask2"] = bits(0x40, n44)
    out["mask3"] = bits(0x40, 0x40)
    out["mask4"] = bits(n44, n44)
    # suffix masks: nSuf rows, two packs each (n44 then 0x40); twice
    def suf_masks():
        for _ in range(nSuf):
            bits(1, n44); bits(1, 0x40)
    suf_masks(); suf_masks()
    out["pre_pos"] = r.p
    # 127 u8 + 127 u8 validation tables
    out["valA"] = r.raw(0x7f)
    out["valB"] = r.raw(0x7f)
    out["end"] = r.raw(4).decode("latin-1")  # "#END", no trailing NUL
    out["final_pos"] = r.p
    out["filelen"] = len(r.b)
    return out

if __name__ == "__main__":
    for path in sys.argv[1:]:
        print("="*70); print(path)
        try:
            o = parse(path)
        except Exception as e:
            import traceback; traceback.print_exc(); continue
        for k in ("magic","title","flags","fit","val","opt3","opt4","opt5",
                  "consonants","p3c","nV","n68","list68","n44","list44",
                  "n48","list48","ne04","list_e04","nPre","pre_keys","pre_freq",
                  "nSuf","suf_keys","suf_freq","nStruct","struct_freq",
                  "sub_counts","sub_labels","end","final_pos","filelen"):
            v = o.get(k)
            if isinstance(v, list) and len(v) > 12:
                print(f"  {k}: ({len(v)}) {v[:12]}...")
            else:
                print(f"  {k}: {v!r}")
        print("  M1:")
        for row in o["M1"]: print("    ", row)
        if o["n48"] <= 40:
            print("  M2:")
            for row in o["M2"]: print("    ", row)
        ok = o["end"] == "#END" and o["final_pos"] == o["filelen"]
        print("  >>> LANDED ON #END:", ok, f"(end={o['end']!r} pos={o['final_pos']} len={o['filelen']})")
