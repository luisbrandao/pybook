# EBoN `.qch` (Quick Chapter) binary format — reverse-engineering notes

Status: **skeleton mapped & validated** against known-seed chapters
(`Newkie/debug.qch` = BABEBI/COCUCY, `Newkie/Luis.qch` = BABEBIBO/CACECICO,
`startrek/klingon.qch` which also has a plaintext `.ebn`). Little-endian,
uint16 throughout. Strings are NUL-terminated, latin-1.

A `.qch` is the *compiled* form of a chapter: the original seed names are NOT
stored, but everything the generator needs (element inventories, structures,
frequencies, prefix/suffix pools, fit/adjacency tables) is.

## Layout

| Offset | Field | Notes |
|--------|-------|-------|
| 0x00 | `byte0` = 0x00 | constant |
| 0x01 | `hdr_u16` | purpose TBD (varies per file; not file length, not name count) |
| 0x03 | `magic` cstr | `"EBoN 3.0"` |
| … | `title` cstr | e.g. `"Klingon"` |
| … | `line1` cstr | |
| … | `line2` cstr | |
| … | `author` cstr | |
| … | `date` cstr | (often `"0"` in compiled form) |
| … | GENOPT block | see below |
| … | consonant alphabet cstr | consonants actually present, e.g. `"BC"`, `"ABCDGHJKLMNPRSTVWEIOQUYZ"` |
| … | structure table | ASCII structure-number strings + freqs |
| … | vowelic element list | NUL-separated element strings, e.g. `A E I O U Y`, empty string terminates |
| … | frequency / adjacency matrices | sparse uint16 tables (fit levels) |
| … | prefix / suffix pools | 2-element combos, stored with letters (seen as `B C`, `C…C` runs) |
| … | substructure table | ASCII digit strings, e.g. `"111111"`, `"11111111"` |
| … | more matrices, incl. 0xFFFF-padded fixed tables | 0xFFFF = empty/unused slot |
| … | footer counts | e.g. `"22"` |
| EOF-4 | `"#END"` | constant terminator |

## GENOPT block (confirmed)

`flags fit val 00 00 00`

- `flags` bitfield: `structgen=1, statgen=2, shuffle=4, prefix=8, suffix=16`
  (debug/Luis = `0x07` = structgen|statgen|shuffle ✓ matches their GENOPT)
- `fit` = fitting level byte (debug/Luis = 1 ✓)
- `val` = validation level byte (debug/Luis = 1 ✓)
- trailing bytes likely y/u semivowel + prefix/suffix detail toggles

## Structure numbering (from Doc/3, validated)

Alternating C/V elements. Even-length-starting-C series:
`CVCV=4, CVCVC=6, CVCVCV=8, CVCVCVC=10, CVCVCVCV=12`.
- debug seeds BABEBI/COCUCY → CVCVCV = **8** ✓ (saw `'8'`, substruct `'111111'`)
- Luis seeds BABEBIBO/CACECICO → CVCVCVCV = **12** ✓ (saw `'12'`, substruct `'11111111'`)

Substructure = per-element lengths (all `1` here since every element is a single letter).

## Still to pin down

- Exact `hdr_u16` meaning.
- Precise boundaries/encoding of the fit-level adjacency matrices (level 1/2/3
  from Doc/3) and how prefix vs suffix pools are delimited.
- Element-frequency table location (for `statgen` weighting).

For "inspiration" fidelity we mainly need: vowelic elements, consonants,
structures+substructures+freqs, prefix/suffix pools, and per-element freqs.
The full adjacency matrices are the nice-to-have that most affects name "feel".

## Update — decoder built, scope of remaining work

`pyebon/qch.py` now decodes, validated across debug/Luis/klingon and confirmed
sensible on locked chapters (Quenya, Latin, Sindarin):
- metadata, GENOPT (flags/fit/val), alphabet, **structure numbers**, and the
  **vowelic element inventory** (rich: diphthongs like `A'E`, `EE'`, `OIO`).

Header sub-layout pinned down (between alphabet and vowel list):
`00 02  <elemCount> 01 "<structNum>\0"  02 <vowelCount>  <vowel cstrs...> 00`.

Key structural finding: **there is NO consonant-element string list.** Per Doc/3
("consonants fit only as single letters"), consonant clusters are NOT stored;
they are rebuilt letter-by-letter from the alphabet via the letter-level
adjacency matrices. So the only thing missing for full generation is the
**matrix region** (starts right after the vowel list, e.g. klingon ~0x10d):
large sparse `uint16` tables holding:
- level-1 (consonant-letter ↔ vowel-element) adjacency + frequency,
- level-2 (consonant-letter ↔ consonant-letter across a vowel),
- level-3 (vowel-element ↔ vowel-element across a consonant),
- start/end, and prefix/suffix vectors,
then a 0xFFFF-padded fixed table, footer counts, and `#END`.

Index spaces: consonant letters by position in the alphabet field; vowel
elements by position in the vowel list. With klingon's known seeds we can
compute expected adjacency counts and match them to byte offsets to deduce the
exact matrix layout — that's the remaining (sizable but bounded) RE task.

`qch_to_chapter()` bridges what we have into the engine, but only supports
**fit:0** generation (rough) until the matrices are decoded.
