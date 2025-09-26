import os

def clean_ebn_debug():
    input_file = "ebnDebug.txt"
    output_file = "chapters/ebnReady.txt"
    
    # Create the chapters directory if it doesn't exist
    os.makedirs("chapters", exist_ok=True)
    
    # Read the input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: {input_file} not found!")
        return
    
    # Process the lines
    cleaned_lines = []
    
    for i, line in enumerate(lines):
        line = line.strip()  # Remove leading/trailing whitespace
        
        # Skip the first line (index 0)
        if i == 0:
            continue
            
        # Skip empty lines
        if not line:
            continue
            
        # Skip lines with dots (…)
        if '…' in line or '.' in line:
            continue
            
        # Add valid lines to our cleaned list
        cleaned_lines.append(line)
    
    # Write to output file (this will overwrite if file exists)
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for line in cleaned_lines:
                f.write(line + '\n')
        
        print(f"Successfully cleaned file. Output written to {output_file}")
        print(f"Processed {len(cleaned_lines)} valid lines.")
        
    except Exception as e:
        print(f"Error writing to {output_file}: {e}")

if __name__ == "__main__":
    clean_ebn_debug()