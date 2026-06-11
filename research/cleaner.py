import os
import sys
from pathlib import Path

def clean_txt_files(directory_path):
    directory = Path(directory_path)
    
    if not directory.exists() or not directory.is_dir():
        print(f"Error: '{directory_path}' is not a valid directory!")
        return
    
    txt_files = directory.glob("*.txt")
    
    for txt_file in txt_files:
        try:
            # Read, clean, deduplicate, and sort
            with open(txt_file, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            
            # Remove duplicates and sort
            unique_sorted_lines = sorted(set(lines))
            
            # Write back
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(unique_sorted_lines) + '\n')
            
            print(f"✓ {txt_file.name}: {len(lines)} → {len(unique_sorted_lines)} lines")
            
        except Exception as e:
            print(f"✗ Error with {txt_file.name}: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python clean_names.py <directory_path>")
        sys.exit(1)
    
    clean_txt_files(sys.argv[1])