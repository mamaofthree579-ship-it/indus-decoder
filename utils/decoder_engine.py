"""
decoder_engine.py
Core decoding engine for Indus Script Reconstruction Project
Author: Open-Source Foundation (2025)
"""

import json
import os
import math
from datetime import datetime
from statistics import mean

# === PATH CONSTANTS ===
CONFIG_PATH = "./models/model_config.json"
SEQUENCES_PATH = "./data/sequences.json"

# === UTILITY FUNCTIONS ===
def load_json(file_path):
    """Load JSON safely with descriptive error handling."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing required file: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in {file_path}: {e}")

def ensure_dir(path: str):
    """Ensure directory exists before writing files."""
    os.makedirs(os.path.dirname(path), exist_ok=True)

# === INITIALIZE DATA ===
config = load_json(CONFIG_PATH)
sequences = load_json(SEQUENCES_PATH)

LOG_FILE = config.get("logging", {}).get("file", "./logs/decoding_log.txt")

# === LOGGING ===
def log(message: str, level: str = "INFO"):
    """Log messages both to console and file if enabled."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    if config.get("logging", {}).get("enabled", True):
        print(entry)
    ensure_dir(LOG_FILE)
    with open(LOG_FILE, "a", encoding="utf-8") as logf:
        logf.write(entry + "\n")

# === CORE DECODE FUNCTIONS ===
def detect_patterns(sequence_list, params):
    """Detect recurring symbol clusters within sequences."""
    if not sequence_list:
        return []

    ws = params.get("window_size", 3)
    sim_thresh = params.get("similarity_threshold", 0.8)
    min_rep = params.get("min_pattern_repeats", 2)
    patterns = []

    for seq in sequence_list:
        if not seq:
            continue
        length = len(seq)
        for i in range(length - ws + 1):
            window = tuple(seq[i:i + ws])
            repeat_count = sum(1 for j in range(i + 1, length - ws + 1)
                               if tuple(seq[j:j + ws]) == window)
            if repeat_count >= min_rep:
                uniqueness = len(set(window)) / ws
                if uniqueness >= sim_thresh:
                    patterns.append(window)

    unique_patterns = [list(p) for p in set(patterns)]
    log(f"Pattern detection complete: {len(unique_patterns)} unique patterns found.")
    return unique_patterns


def semantic_map(symbol: str, weights: dict):
    """Map individual symbol to semantic value based on weight vector."""
    base = {
        "Quantum": 0.7,
        "Scalar": 0.6,
        "Consciousness": 0.9,
        "Geometric": 0.5
    }
    try:
        value = sum(base[k] * weights.get(k, 1.0) for k in base)
    except Exception:
        value = sum(base.values()) / len(base)
    return value


def harmonic_resonance(symbol_group, resonance_cfg):
    """Compute harmonic stability and resonance of a group."""
    if not symbol_group:
        return 0.0
    harmonics = resonance_cfg.get("harmonic_bands", [1, 3, 5, 7])
    depth_weight = resonance_cfg.get("fractal_depth_weight", 1.25)
    symmetry_factor = resonance_cfg.get("symmetry_coupling_factor", 0.85)
    freq_sum = mean(math.sin(h * len(symbol_group)) for h in harmonics)
    return abs(freq_sum * depth_weight * symmetry_factor)


def decode_symbol_sequence(sequence, cfg):
    """Decode a single sequence into multilayer meanings."""
    if not sequence:
        return []

    field_bias = cfg["algorithm"]["semantic_mapping"]["parameters"]["field_bias_weights"]
    resonance_cfg = cfg["algorithm"]["resonance_model"]["parameters"]

    meanings = []
    for symbol in sequence:
        s_value = semantic_map(symbol, field_bias)
        r_value = harmonic_resonance(sequence, resonance_cfg)
        meanings.append({
            "symbol": symbol,
            "semantic_strength": round(s_value, 3),
            "harmonic_resonance": round(r_value, 3),
            "combined_score": round((s_value + r_value) / 2, 3)
        })
    return meanings


def decode_all_sequences(cfg, seq_data):
    """Run full pipeline on all sequences."""
    results = {}
    pattern_params = cfg["algorithm"]["pattern_recognition"]["parameters"]

    for key, seq_entry in seq_data.items():
        sequence_list = seq_entry.get("symbol_sequences", [])
        patterns = detect_patterns(sequence_list, pattern_params)
        decoded_batches = [decode_symbol_sequence(s, cfg) for s in sequence_list]

        results[key] = {
            "patterns_detected": patterns,
            "decoded_sequences": decoded_batches
        }
        log(f"Decoded sequence '{key}' with {len(patterns)} pattern(s).")

    return results

# === OUTPUT HANDLER ===
def save_output(data, cfg):
    """Save decoded data to output directory."""
    output_path = cfg["output"]["decoded_sequences_file"]
    ensure_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log(f"Results written to {output_path}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    log("=== Decoding process initiated ===")
    decoded_results = decode_all_sequences(config, sequences)
    save_output(decoded_results, config)
    log("=== Decoding process completed successfully ===")
