#!/usr/bin/env python3
"""Exploratory decoder for EBoN .qch (Quick Chapter) binary files.

This is a scratch/analysis tool, not the final parser. It dumps the layout of
a .qch with byte offsets so we can reverse-engineer the format by cross-checking
against chapters whose seed names we know (Newkie/debug, Newkie/Luis, startrek/klingon).

Run: python qch_explore.py <file.qch> [more.qch ...]
"""
import sys
import struct


def read_cstr(buf, pos):
    end = buf.index(b"\x00", pos)
    return buf[pos:end].decode("latin-1"), end + 1


def u16(buf, pos):
    return struct.unpack_from("<H", buf, pos)[0]


def explore(path):
    buf = open(path, "rb").read()
    print(f"\n{'='*70}\n{path}  ({len(buf)} bytes)\n{'='*70}")

    pos = 0
    b0 = buf[pos]; pos += 1
    hdr = u16(buf, pos); pos += 2
    print(f"[0x000] byte0={b0}  hdr_u16=0x{hdr:04x} ({hdr})")

    # 6 c-strings: magic, title, line1, line2, author, date
    labels = ["magic", "title", "line1", "line2", "author", "date"]
    for lab in labels:
        s, pos = read_cstr(buf, pos)
        print(f"[0x{pos:03x}] {lab:7s}= {s!r}")

    # GENOPT-derived params region (unknown length) -- dump next 8 bytes raw
    print(f"[0x{pos:03x}] genopt+? raw: {buf[pos:pos+8].hex(' ')}")
    flags = buf[pos]
    print(f"         flags=0x{flags:02x}  bits: "
          f"structgen={bool(flags&1)} statgen={bool(flags&2)} shuffle={bool(flags&4)} "
          f"prefix={bool(flags&8)} suffix={bool(flags&16)} hi={flags>>5}")
    print(f"         fit?={buf[pos+1]} val?={buf[pos+2]} "
          f"next={buf[pos+3]},{buf[pos+4]},{buf[pos+5]}")

    # Dump every printable ASCII run >=1 char with its offset, to find the
    # consonant alphabet, structure-number strings, and vowelic elements.
    print("  --- ascii runs (offset: text) ---")
    i = pos
    run_start = None
    runs = []
    while i < len(buf):
        c = buf[i]
        printable = 0x21 <= c <= 0x7e  # no space, printable
        if printable:
            if run_start is None:
                run_start = i
        else:
            if run_start is not None:
                runs.append((run_start, buf[run_start:i].decode("latin-1")))
                run_start = None
        i += 1
    if run_start is not None:
        runs.append((run_start, buf[run_start:].decode("latin-1")))
    for off, txt in runs:
        print(f"    0x{off:04x}: {txt!r}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        explore(p)
