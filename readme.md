# Enhanced Custom Random Name Generator

A sophisticated Python-based name generator that creates realistic-sounding names by analyzing patterns from input text files. The program uses intelligent vowel-aware splitting and weighted sampling to generate names that sound natural and authentic.

## Features

- **Smart Name Analysis**: Uses vowel-aware heuristics to split names into prefix, middle, and suffix components
- **Weighted Sampling**: Considers frequency of name parts for more realistic generation
- **Infinite Generation Mode**: Generate names continuously until interrupted
- **Customizable Length**: Set minimum and maximum name lengths
- **Debug Mode**: Inspect how names are broken down into components
- **Reproducible Results**: Use seeds for consistent output

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

Simply clone or download the repository. The program is ready to use without additional installation steps.

## Usage

### Basic Syntax

```bash
python name_generator_enhanced.py <chapter_file> [options]
```

### Command Line Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--count` | `-n` | Number of names to generate (0 = infinite) | 0 |
| `--min` | `-m` | Minimum length of generated names | 2 |
| `--max` | `-x` | Maximum length of generated names | 20 |
| `--seed` | `-s` | Random seed for reproducibility | None |
| `--debug` | `-d` | Show name component analysis and exit | False |
| `--help` | `-h` | Show help message | - |

## Examples

### 1. Generate 10 Greek Male Names

```bash
python name_generator_enhanced.py chapters/Greek-male.txt -n 10
```

Sample output:
```
Alexios
Dimitris
Theodoros
Nikolas
Panagiotis
Georgios
Konstantinos
Athanasios
Christophoros
Spyridon
```

### 2. Generate Female Viking Names Continuously

```bash
python name_generator_enhanced.py chapters/Viking-female.txt
```

This will generate names infinitely until you press Ctrl+C:
```
(Generating forever — press Ctrl-C to stop)

Astrid
Sigrid
Ingrid
Helga
Brunhild
...
```

### 3. Generate Short Roman Names (3-6 characters)

```bash
python name_generator_enhanced.py chapters/Roman-male.txt -n 5 -m 3 -x 6
```

Sample output:
```
Marcus
Gaius
Lucius
Titus
Brutus
```

### 4. Generate Names with Specific Seed (Reproducible)

```bash
python name_generator_enhanced.py chapters/Gods-female.txt -n 5 -s 42
```

This will always generate the same names when using seed 42.

### 5. Debug Mode - Analyze Name Components

```bash
python name_generator_enhanced.py chapters/ST-Klingon.txt -d -n 5
```

Sample output:
```
=== Prefix (15 unique | 45 total) ===
K'E             3
Gor             2
Worf            2
...

=== Middle (23 unique | 67 total) ===
'tagh           4
logh            3
ang             2
...

=== Suffix (18 unique | 52 total) ===
on              5
agh             4
oS              3
...
```

### 6. Generate Long Fantasy Names

```bash
python name_generator_enhanced.py chapters/Greek-male.txt -n 8 -m 8 -x 15
```

### 7. Generate Surnames

```bash
python name_generator_enhanced.py chapters/Surnames-various.txt -n 10 -m 4 -x 12
```

## Available Name Collections

The `chapters/` directory contains various name collections:

- `Gods-female.txt` / `Gods-male.txt` - Mythological deity names
- `Greek-female.txt` / `Greek-male.txt` - Greek names
- `Roman-female.txt` / `Roman-male.txt` - Roman names
- `Viking-female.txt` / `Viking-male.txt` - Norse/Viking names
- `ST-Klingon.txt` / `ST-Romulan.txt` - Star Trek alien names
- `Planetas.txt` - Planet names
- `Surnames-various.txt` - Various surnames

## How It Works

### 1. Name Analysis
The program analyzes input names using a smart splitting algorithm:

- **Vowel-aware splitting**: For names with 2+ vowels, splits at first and last vowel boundaries
- **Single vowel handling**: Keeps first and last characters as prefix/suffix
- **Fallback method**: Uses length ratios (30%/20%) when vowel method fails

### 2. Component Weighting
Each component (prefix, middle, suffix) is weighted by frequency of appearance in the source text.

### 3. Generation
Names are assembled by randomly selecting components based on their weights, ensuring results stay within specified length bounds.

## Tips for Best Results

1. **Use appropriate source files**: Match the style you want (Greek names for Greek-style results)
2. **Adjust length bounds**: Shorter bounds for punchy names, longer for elaborate ones  
3. **Try different seeds**: Find a seed that produces names you like
4. **Use debug mode**: Understand how your source names are being analyzed
5. **Combine sources**: Create custom name files by combining different sources

## GUI Version

A GUI version (`name_generator_gui.py`) is also available for users who prefer a graphical interface.

## Troubleshooting

### "Insufficient data after preprocessing"
- Your source file may be too small or have names that are too short
- Try a different source file or add more names to your current file

### "Unable to build a name within the requested length bounds"
- Your min/max length settings may be too restrictive
- Try widening the length range or using a different source file

### File encoding issues
- Ensure your text files are saved in UTF-8 encoding
- The program handles various Unicode characters including accented letters

## License

This project is open source. Feel free to modify and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.