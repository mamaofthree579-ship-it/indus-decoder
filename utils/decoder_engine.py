import json
import os
import math
import pickle
from datetime import datetime
from statistics import mean
import numpy as np

# === LOAD CONFIG AND MODELS ===

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_model(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)

CONFIG_PATH = './models/model_config.json'
SEQUENCES_PATH = './data/sequences.json'
MARKOV_PATH = './models/markov_model.pkl'
SEMANTIC_PATH = './models/semantic_model.pkl'

config = load_json(CONFIG_PATH)
sequences = load_json(SEQUENCES_PATH)

# Load trained models
try:
    markov_model = load_model(MARKOV_PATH)
    semantic_model = load_model(SEMANTIC_PATH)
except Exception as e:
    print(f"⚠️ Warning: Could not load models properly. {e}")
    markov_model, semantic_model = None, None

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
    """Detect repeating and recursive patterns enhanced by Markov model."""
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
                        # Markov model adjustment
                        if markov_model:
                            prob = 1.0
                            for k in range(len(window)-1):
                                pair = (window[k], window[k+1])
                                prob *= markov_model.get(pair, 0.01)
                            if prob > 0.05:
                                patterns.append(window)
                        else:
                            patterns.append(window)
    log(f"Detected {len(patterns)} patterns (Markov-enhanced).")
    return patterns


def semantic_map(symbol, weights):
    """Map symbol to semantic meaning using embedding model."""
    base_weights = {
        "Quantum": 0.7,
        "Scalar": 0.6,
        "Consciousness": 0.9,
        "Geometric": 0.5
    }
    raw_score = sum(base_weights[k] * weights[k] for k in base_weights)
    if semantic_model:
        try:
            # Assume semantic_model returns embedding vector or similarity
            embedding = semantic_model.get(symbol, np.zeros(10))
            similarity = np.mean(np.abs(embedding))  # normalize vector magnitude
            return round((raw_score + similarity) / 2, 3)
        except Exception:
            return round(raw_score, 3)
    return round(raw_score, 3)


def harmonic_resonance(symbol_group, resonance_config):
    """Compute harmonic stability of a symbol group."""
    params = resonance_config.get('parameters', {})
    harmonics = params.get('harmonic_bands', [1])
    depth_weight = params.get('fractal_depth_weight', 1.0)
    symmetry_factor = params.get('symmetry_coupling_factor', 1.0)

    freq_sum = mean([math.sin(h * len(symbol_group)) for h in harmonics])
    return abs(freq_sum * depth_weight * symmetry_factor)


def decode_symbol_sequence(sequence):
    """Decode a single sequence into meaning layers."""
    meanings = []
    for symbol in sequence:
        s_value = semantic_map(symbol, config['algorithm']['semantic_mapping']['parameters']['field_bias_weights'])
        r_value = harmonic_resonance(sequence, config['algorithm']['resonance_model']['parameters'])
        combined = (s_value + r_value) / 2
        meanings.append({
            "symbol": symbol,
            "semantic_strength": round(s_value, 3),
            "harmonic_resonance": round(r_value, 3),
            "combined_score": round(combined, 3)
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
    log("=== Decoding process (ML-integrated) started ===")
    decoded_results = decode_all_sequences()
    output_path = config['output']['decoded_sequences_file']
    save_output(decoded_results, output_path)
    log("=== Decoding process completed ===")
