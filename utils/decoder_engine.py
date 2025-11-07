import json
import os
import math
from datetime import datetime
from statistics import mean

# === LOAD CONFIG AND DATA ===

def load_json(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if os.path.getsize(file_path) == 0:
        raise ValueError(f"File {file_path} is empty — run the decoding engine first.")
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {file_path}: {e}")
CONFIG_PATH = './models/model_config.json'
SEQUENCES_PATH = './data/sequences.json'

config = load_json(CONFIG_PATH)
sequences = load_json(SEQUENCES_PATH)

# === LOGGING ===

LOG_FILE = config['logging']['file']

def log(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as logf:
        logf.write(entry)
    if config['logging']['enabled']:
        print(entry.strip())

# === CORE DECODING FUNCTIONS ===

def detect_patterns(sequence_list, params):
    """Detect repeating and recursive patterns."""
    patterns = []
    ws = params['window_size']
    min_rep = params['min_pattern_repeats']
    sim_thresh = params['similarity_threshold']

    for seq in sequence_list:
        for i in range(len(seq) - ws):
            window = seq[i:i+ws]
            for j in range(i+1, len(seq) - ws):
                if seq[j:j+ws] == window:
                    similarity = len(set(window)) / ws
                    if similarity >= sim_thresh:
                        patterns.append(window)
    log(f"Detected {len(patterns)} patterns across all sequences.")
    return patterns


def semantic_map(symbol, weights):
    """Map symbol to meaning strength via context weighting."""
    base = {
        "Quantum": 0.7,
        "Scalar": 0.6,
        "Consciousness": 0.9,
        "Geometric": 0.5
    }
    return sum(base[k] * weights[k] for k in base)


def harmonic_resonance(symbol_group, resonance_config):
    """Compute harmonic stability of symbol group."""
    harmonics = resonance_config['harmonic_bands']
    depth_weight = resonance_config['fractal_depth_weight']
    symmetry_factor = resonance_config['symmetry_coupling_factor']
    freq_sum = mean([math.sin(h * len(symbol_group)) for h in harmonics])
    return abs(freq_sum * depth_weight * symmetry_factor)


def decode_symbol_sequence(sequence):
    """Decode a single sequence into meaning layers."""
    meanings = []
    for symbol in sequence:
        s_value = semantic_map(symbol, config['algorithm']['semantic_mapping']['parameters']['field_bias_weights'])
        r_value = harmonic_resonance(sequence, config['algorithm']['resonance_model']['parameters'])
        meanings.append({
            "symbol": symbol,
            "semantic_strength": round(s_value, 3),
            "harmonic_resonance": round(r_value, 3),
            "combined_score": round((s_value + r_value) / 2, 3)
        })
    return meanings


def decode_all_sequences():
    """Run the full decoding process."""
    all_decoded = {}
    pattern_params = config['algorithm']['pattern_recognition']['parameters']

    for key, seq in sequences.items():
        sequence_list = seq.get('symbol_sequences', [])
        patterns = detect_patterns(sequence_list, pattern_params)
        decoded_seq = [decode_symbol_sequence(s) for s in sequence_list]
        all_decoded[key] = {
            "patterns_detected": patterns,
            "decoded_sequences": decoded_seq
        }
        log(f"Decoded sequence {key} with {len(patterns)} patterns.")
    return all_decoded


# === OUTPUT HANDLER ===

def save_output(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log(f"Results saved to {path}")


# === MAIN EXECUTION ===

if __name__ == "__main__":
    log("=== Decoding process started ===")
    decoded_results = decode_all_sequences()
    output_path = config['output']['decoded_sequences_file']
    save_output(decoded_results, output_path)
    log("=== Decoding process completed ===")
