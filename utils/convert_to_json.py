import csv
import json
import os
from pathlib import Path

RAW_DIR = Path("./data/raw/")
OUT_DIR = Path("./data/")
OUT_FILE = OUT_DIR / "sequences.json"

def normalize_symbol(symbol):
    """Clean and unify symbol representation."""
    return symbol.strip().upper().replace(" ", "_")

def from_csv(csv_file):
    """Load symbol sequences from CSV."""
    sequences = {}
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq_id = row.get("Sequence_ID", f"SEQ_{len(sequences)+1}")
            symbols = [normalize_symbol(s) for s in row["Symbols"].split(",")]
            sequences[seq_id] = {"symbol_sequences": [symbols]}
    return sequences

def from_text(text_file):
    """Load sequences from a plain text file (each line = sequence)."""
    sequences = {}
    with open(text_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            cleaned = [normalize_symbol(s) for s in line.strip().split()]
            sequences[f"SEQ_{i+1}"] = {"symbol_sequences": [cleaned]}
    return sequences

def save_json(data, out_path):
    os.makedirs(out_path.parent, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved {len(data)} sequences to {out_path}")

if __name__ == "__main__":
    raw_csv = RAW_DIR / "indus_signs.csv"
    raw_txt = RAW_DIR / "indus_sequences.txt"

    if raw_csv.exists():
        data = from_csv(raw_csv)
    elif raw_txt.exists():
        data = from_text(raw_txt)
    else:
        print("❌ No raw input found in ./data/raw/")
        exit(1)

    save_json(data, OUT_FILE)
