import json
import pickle
from collections import defaultdict
import os

# === CONFIG ===
DATA_PATH = './data/sequences.json'
MODEL_OUTPUT_PATH = './models/markov_model.pkl'

# === LOAD SEQUENCE DATA ===
def load_sequences(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# === TRAINING FUNCTION ===
def train_markov_model(sequences):
    """
    Train a simple Markov transition model based on symbol frequency transitions.
    """
    transitions = defaultdict(lambda: defaultdict(int))

    for key, seq_data in sequences.items():
        for sequence in seq_data.get("symbol_sequences", []):
            for i in range(len(sequence) - 1):
                current_symbol = sequence[i]
                next_symbol = sequence[i + 1]
                transitions[current_symbol][next_symbol] += 1

    # Normalize transitions into probabilities
    model = {}
    for current_symbol, next_dict in transitions.items():
        total = sum(next_dict.values())
        model[current_symbol] = {n: v / total for n, v in next_dict.items()}

    return model

# === SAVE MODEL ===
def save_model(model, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as f:
        pickle.dump(model, f)

# === MAIN EXECUTION ===
if __name__ == "__main__":
    print("Loading sequences...")
    sequences = load_sequences(DATA_PATH)
    print("Training Markov model...")
    model = train_markov_model(sequences)
    print(f"Model trained with {len(model)} symbols.")
    print("Saving model...")
    save_model(model, MODEL_OUTPUT_PATH)
    print(f"Markov model saved to {MODEL_OUTPUT_PATH}")
