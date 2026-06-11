# `.qch` on-disk format — DEFINITIVE (from decompiled writer)

Source of truth: Ghidra decompilation of the EBoN `.qch` **writer** at
`EBoN.exe:0x41b6e1` (`/tmp/ebonW_0041b6e1.c`, kept in `re/`). This supersedes
all earlier guesswork about the matrix region. The writer accumulates the whole
file into an in-memory AnsiString buffer (`out`) one byte at a time, then writes
it to disk in a single pass. So the **on-disk byte order == the order of the
append calls** below.

## Primitive encodings (THE key discoveries)

- **str** — write AnsiString bytes then a `0x00` terminator. (Read: bytes up to NUL.)
- **u8** — one raw byte.
- **u16 = BIG-ENDIAN.** The writer does `divmod(value, 256)` and appends
  **high byte first, then low byte**. This is why every earlier little-endian
  grid search failed and why matrix dumps looked like "multiples of 256."
  Read as `hi*256 + lo`.
- **bitpack(flags[N])** — booleans packed **LSB-first**, 8 per byte; a partial
  final byte is flushed if N not a multiple of 8. Used for the structure/
  substructure validity masks.

In the writer, the chapter object pointer is `C` (`*(EBP+8)`); `f[off]` means the
field at that hex offset in `C`. Offsets are in-memory only — irrelevant to a
reader, which just consumes the stream in order. Counts are themselves emitted
into the stream, so a parser reads each count then loops.

## On-disk sequence (complete)

1. **str** magic `"EBoN 3.0"`
2. **str** title
3. **str** subtitle/line 2
4. **str** line 3
5. **str** line 4
6. **str** author/credit line
   → 6 NUL-terminated strings total (magic + 5 metadata lines).
7. **u8 GENOPT flags**: bit0 structgen `f[0x4c]`, bit1 statgen `f[0x4d]`,
   bit2 prefix `f[0x4e]`, bit3 suffix `f[0x4f]`, bit4 shuffle `f[0x50]`,
   bit7 = 0x80 if `f[1]!=0` (locked/encrypted-source marker).
8. **u8** fit level `f[0x54]`
9. **u8** val level `f[0x58]`
10. **u8** `f[0x5c]` (3rd genopt — y/u semivowel or punct mode)
11. **u8** `f[0x85498]`, **u8** `f[0x85499]` (two more option bytes)
12. **str** `?` (the 0x1148 block — single string; likely consonant alphabet)
13. **u16** `f[0x3c]` (a count/param, BE)
14. **u8 nV** `f[0xe58]` — inner matrix dimension (vowel-element count; the
    common inner-loop bound for the big adjacency matrices)
15. **u8 n68** `f[0x68]`
16. loop i in [0,n68): **str** label ; **u8** `f[0x86c+i*4]`  (element + 1 tag byte)
17. **u8 n44** `f[0x44]`
18. loop i in [0,n44): **str** label                          (n44 strings)
19. **MATRIX M1** [n44 × nV] **u16 BE**: `f[0x3e5c + i*0x80 + j*4]`
    (row stride 0x80 = 32 ints; i over n44, j over nV)
20. **u16 n48** `f[0x48]`
21. loop i in [0,n48): **str** label                          (n48 strings)
22. **MATRIX M2** [n48 × nV] **u16 BE**: `f[0x13e5c + i*0x80 + j*4]`
23. **u8 ne04** `f[0xe04]`
24. loop i in [0,ne04): **str** label
25. **u16 nPre** `f[0x33e5c]` (prefix entry count)
26. loop i in [0,nPre): **2 bytes** encoding a 2-element key with a +100 type
    tag (branch: if first elem <100 write `elem0`,`elem1-100` else
    `elem0-100`,`elem1`; the −100 marks which member is the vowel-element vs
    consonant index) then **str** label.
27. **MATRIX** [nPre] **u16 BE**: `f[0x33e64][i]` (prefix frequencies)
28. **u16 nSuf** `f[0x33e60]`
29. loop i in [0,nSuf): same 2-byte +100 key encoding + **str** label
30. **MATRIX** [nSuf] **u16 BE**: `f[0x33e68][i]` (suffix frequencies)
31. **structures**: scan `f[0x3427c + i*4]` for i in 0..0x40 (64), find the
    highest nonzero index `maxS`; **u8** `maxS+1`.
32. loop i in [0,maxS]: **u16 BE** `f[0x3427c+i*4]`  (structure frequencies, by C/V-pattern number)
33. loop i in [0,maxS]: **u16 BE** `f[0x3437c+i*4]`  (substructure count per structure)
34. loop i in [0,maxS]: loop j in [0, that count): **u16 BE** `f[0x3447c][i][j]` (substructure freqs)
35. loop i in [0,maxS]: loop j in [0, that count): **str** substructure label
    (NOTE: ordering of 34/35 — verify empirically; writer emits the freq
    matrix block then the label block.)
36. **bitpacked validity masks** (each row LSB-first, 8/byte):
    - n44 rows × 64 flags  : `f[i*0x40 + 0x34484 + j]`, j 0..0x40   → 8 bytes/row
    - 64 rows × n44 flags   : `f[i*0x200 + 0x3c484 + j]`, j 0..n44  → ceil(n44/8)/row
    - 64 rows × 64 flags    : `f[i*0x40 + 0x44484 + j]`            → 8 bytes/row
    - n44 rows × n44 flags  : `f[i*0x200 + 0x45484 + j]`
    - nSuf rows: two packs — `f[0x85484][i][j]` (j 0..n44) and
      `f[0x85484][i][100+j]` (j 0..0x40)
    - nSuf rows: two packs — `f[0x85488][i][j]` (j 0..n44) and `[100+j]` (j 0..0x40)
37. **127 × u8** `f[0x33e74+i*4]` (validation/letter-freq table A, i 0..0x7f)
38. **127 × u8** `f[0x34078+i*4]` (validation/letter-freq table B)
39. **str** `"#END"` (DAT_0049859d)

## VALIDATED against reader + known seeds (corrections to the above)

Cross-checked with the **reader** (`EBoN.exe:0x41cd90`, `re/qch_reader_decompiled.c`)
and a faithful Python parser (`re/parse_qch.py`) that lands **exactly on `#END`**
for debug, Luis, and Klingon. Corrections/confirmations:

- **3-byte preamble** before the magic (`00 68 01` in debug); magic is then
  read-and-discarded for validation.
- **`nV = f[0xe58]`** is the matrix inner dimension, **not** the vowel count:
  debug=6, Luis=8, Klingon=7. It tracks the max structure length / fit window.
- **Consonant elements ARE stored** — `list48` is the consonant-element list
  (multi-letter clusters: Klingon has 114 incl. `KT, TB, NN, BR`). This
  **overturns** the earlier "consonants are single letters only" assumption.
  So: `list44` = vowel elements, `list48` = consonant elements.
- **M1** `[len(list44) × nV]` and **M2** `[len(list48) × nV]` are BE16 freq
  tables: `M1` over vowel elements, `M2` over consonant elements. Columns are a
  **fit-distance index** the generator computes from (position, struct length)
  via `>>1` halving — EBoN's L1/L2/L3 fitting, not a plain adjacency/position.
- **Prefix/suffix entries are 3 bytes each, NO string**: `(elemA, elemB, tag)`
  where `tag==0x56('V')` means elemB is the vowel (else elemA); the vowel index
  is stored +100 internally. Followed by `nPre`/`nSuf` BE16 frequencies.
  VALIDATED on debug seeds: prefixes `(0,0)`→BA, `(1,3)`→CO; suffixes
  `(0,2)`→BI, `(1,5)`→CY. Element indices: consonants by `list48` position,
  vowels by `list44` position.
- **Structures**: `u8 count` = (max nonzero structure index)+1 (debug=9 because
  structure #8 = CVCVCV is the only one used); then `count` BE16 struct freqs,
  `count` BE16 substructure-counts, then nested BE16 substructure freqs and
  nested NUL-terminated substructure labels (debug: `"111111"`).
- **`#END`** is the last 4 bytes with **no trailing NUL**.

The full validated read order lives in `re/parse_qch.py`.

## What this unlocks

M1 (`0x3e5c`) and M2 (`0x13e5c`) are the two big [count × nV] frequency
matrices — the **fit-level adjacency** that was the whole blocker. With BE16
decoding we can now extract them and assign their semantics (L1 C↔V, L2, L3,
start/end) empirically against Klingon's known seed adjacency. Prefix/suffix
keys (steps 26–30) and structures (31–35) are also fully recoverable.

Helper functions for reference: `FUN_00429f74(stream,&out,byte)` = append byte;
`FUN_0048a5dc(&dst,v,0x100)` = divmod→{dst[0]=v/256, dst[1]=v%256} (BE16);
`FUN_00491944/491ab8/491a74` = AnsiString init/assign/free.
