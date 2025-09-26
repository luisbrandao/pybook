
#!/usr/bin/env python3
"""Enhanced Custom Random Name Generator

Key upgrades
------------
1. **Smarter split**: tries to break names around vowels so
   prefix = up to (and incl.) first vowel
   suffix = from last vowel onward
   middle = in between
   → Falls back to length‑ratio heuristic when vowels are absent.

2. **Weighted sampling**: pools remember how many times each
   (prefix|middle|suffix) appeared; `random.choices` uses those counts.

3. **Infinite mode**: pass `--count 0` (or omit `--count`) to generate
   names indefinitely until interrupted (Ctrl‑C / SIGINT).
"""

import argparse
import pathlib
import random
import sys
from collections import Counter
from typing import Iterator, List, Tuple, Optional

VOWELS = set("aeiouAEIOUáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛäëïöüÄËÏÖÜyY")


# --------------------------- splitting heuristic --------------------------- #
def vowel_positions(name: str) -> List[int]:
    return [i for i, ch in enumerate(name) if ch in VOWELS]

def split_name(name: str) -> Tuple[str, str, str]:
    """
    Split a name into phonetic syllables: prefix, middle, suffix.
    
    Args:
        name: Input name string
        
    Returns:
        Tuple of (prefix, middle, suffix) strings
    """
    if not name:
        return ("", "", "")
    
    name = name.lower()
    vowels = set('aeiou')
    syllables = []
    i = 0
    
    while i < len(name):
        syllable = ""
        
        # Add consonants at the beginning
        while i < len(name) and name[i] not in vowels:
            syllable += name[i]
            i += 1
        
        # Add one vowel
        if i < len(name) and name[i] in vowels:
            syllable += name[i]
            i += 1
        
        if syllable:
            syllables.append(syllable)
    
    # Convert to the required format
    if len(syllables) <= 2:
        prefix = syllables[0] if len(syllables) > 0 else ""
        suffix = syllables[1] if len(syllables) > 1 else ""
        middle = ""
    elif len(syllables) == 3:
        prefix = syllables[0]
        middle = syllables[1]
        suffix = syllables[2]
    else:
        prefix = syllables[0]
        middle = "".join(syllables[1:-1])
        suffix = syllables[-1]
    
    return (prefix, middle, suffix)


# --------------------------- pooling phase -------------------------------- #
def build_weighted_pools(names: List[str]):
    p_counter, m_counter, s_counter = Counter(), Counter(), Counter()
    for raw in names:
        p, m, s = split_name(raw)
        if p:
            p_counter[p] += 1
        if m:
            m_counter[m] += 1
        if s:
            s_counter[s] += 1
    if not (p_counter and m_counter and s_counter):
        raise ValueError("Insufficient data after preprocessing.")
    return p_counter, m_counter, s_counter


# --------------------------- generation phase ----------------------------- #
def weighted_choice(counter: Counter) -> str:
    population = list(counter.keys())
    weights = list(counter.values())
    return random.choices(population, weights=weights, k=1)[0]

# --------------------------------------------------------------------------- #
def dump_counters(label: str, counter: Counter) -> None:
    """Pretty‑print a Counter sorted by descending frequency."""
    total = sum(counter.values())
    print(f"\n=== {label} ({len(counter)} unique | {total} total) ===")
    for part, freq in counter.most_common():
        print(f"{part:<15} {freq}")


def generate_name(pools: Tuple[Counter, Counter, Counter],
                  min_len: int, max_len: int) -> str:
    p_counter, m_counter, s_counter = pools
    for _ in range(1000):
        name = (weighted_choice(p_counter)
                + weighted_choice(m_counter)
                + weighted_choice(s_counter))
        if min_len <= len(name) <= max_len:
            return name
    raise RuntimeError("Unable to build a name within the requested length bounds.")


def infinite_generator(pools, min_len, max_len) -> Iterator[str]:
    while True:
        yield generate_name(pools, min_len, max_len)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Enhanced random name generator.")
    parser.add_argument("chapter", type=pathlib.Path, help="Path to chapter .txt file.")
    parser.add_argument("-n", "--count", type=int, default=0,
                        help="Number of names to generate (0 = infinite, default 0).")
    parser.add_argument("-m", "--min", dest="min_len", type=int, default=2,
                        help="Minimum length of generated names (default 2).")
    parser.add_argument("-x", "--max", dest="max_len", type=int, default=20,
                        help="Maximum length of generated names (default 20).")
    parser.add_argument("-s", "--seed", type=int, help="Random seed for reproducibility.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Dump prefix/middle/suffix pools and exit")

    args = parser.parse_args(argv)

    if args.seed is not None:
        random.seed(args.seed)

    if not args.chapter.is_file():
        sys.exit(f"Error: cannot read file '{args.chapter}'")

    names = [line.strip() for line in args.chapter.read_text(encoding='utf‑8').splitlines() if line.strip()]
    if not names:
        sys.exit("Error: chapter file contains no names.")

    try:
        pools = build_weighted_pools(names)
        if args.debug:
            dump_counters("Prefix", pools[0])
            dump_counters("Middle", pools[1])
            dump_counters("Suffix", pools[2])

    except ValueError as e:
        sys.exit(f"Error: {e}")

    try:
        if args.count > 0:
            for _ in range(args.count):
                print(generate_name(pools, args.min_len, args.max_len))
        else:
            print("(Generating forever — press Ctrl‑C to stop)\n")
            for name in infinite_generator(pools, args.min_len, args.max_len):
                print(name)
    except KeyboardInterrupt:
        print("\n\nExiting. Goodbye!")

if __name__ == "__main__":
    main()
