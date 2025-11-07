import streamlit as st
import json
import os
import pandas as pd
from utils.decoder_engine import decode_all_sequences, save_output, load_json, log

# === PATHS ===
CONFIG_PATH = './models/model_config.json'
SEQUENCES_PATH = './data/sequences.json'
OUTPUT_PATH = './outputs/decoded_results.json'
LOG_PATH = './logs/decoding_log.txt'


# === HELPER FUNCTIONS ===
def load_config():
    return load_json(CONFIG_PATH)


def load_sequences():
    return load_json(SEQUENCES_PATH)


def save_uploaded_json(uploaded_file, save_path):
    """Save uploaded file as JSON."""
    content = json.load(uploaded_file)
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    st.success(f"File saved to {save_path}")


def convert_to_json(uploaded_file, save_path):
    """Convert CSV or TXT to JSON if needed."""
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        json_data = df.to_dict(orient='records')
    elif uploaded_file.name.endswith('.txt'):
        lines = uploaded_file.read().decode('utf-8').splitlines()
        json_data = {"lines": lines}
    else:
        st.error("Unsupported file type for conversion.")
        return False

    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    st.success(f"Converted and saved to {save_path}")
    return True


def display_decoded_results():
    if os.path.exists(OUTPUT_PATH):
        with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
            decoded = json.load(f)

        for key, data in decoded.items():
            st.subheader(f"🧩 Decoded Sequence: {key}")
            st.json(data)

            # Flatten for dataframe display
            flattened = []
            for seq in data['decoded_sequences']:
                for sym in seq:
                    flattened.append(sym)
            df = pd.DataFrame(flattened)
            st.dataframe(df)
    else:
        st.warning("No decoded results found yet.")


def display_logs():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r', encoding='utf-8') as logf:
            logs = logf.read()
        st.text_area("🗒️ Log Output", logs, height=250)
    else:
        st.warning("No logs found yet.")


# === STREAMLIT APP ===

st.set_page_config(page_title="Indus Script Quantum Decoder", layout="wide")

st.title("🔮 Indus Script Quantum Decoder")
st.markdown("""
This tool runs the **Indus Script Decoding Algorithm (IVC Algorithm)**  
— a hybrid of pattern recognition, fractal harmonic mapping, and semantic resonance modeling.
""")

st.sidebar.header("⚙️ Controls")

# --- File Upload Section ---
st.sidebar.subheader("📤 Upload Data / Models")

upload_option = st.sidebar.selectbox(
    "Choose upload type:",
    ["Upload Sequences", "Upload Model Config"]
)

uploaded_file = st.sidebar.file_uploader("Upload a file", type=["json", "csv", "txt"])

if uploaded_file:
    if upload_option == "Upload Sequences":
        target_path = SEQUENCES_PATH
    else:
        target_path = CONFIG_PATH

    if uploaded_file.name.endswith('.json'):
        save_uploaded_json(uploaded_file, target_path)
    else:
        convert_to_json(uploaded_file, target_path)

# --- Run Decoding ---
if st.sidebar.button("🚀 Run Decoding Process"):
    st.info("Decoding process started...")
    results = decode_all_sequences()
    save_output(results, OUTPUT_PATH)
    st.success("Decoding complete! Results saved.")
    st.balloons()

# --- Tabs for viewing results ---
tab1, tab2, tab3 = st.tabs(["📊 Decoded Results", "⚙️ Config & Data", "🗒️ Logs"])

with tab1:
    st.header("Decoded Results")
    display_decoded_results()

with tab2:
    st.header("Current Configuration")
    st.json(load_config())
    st.header("Current Symbol Sequences")
    st.json(load_sequences())

with tab3:
    st.header("System Logs")
    display_logs()
    if st.button("🔁 Refresh Logs"):
        st.experimental_rerun()

# --- Footer ---
st.markdown("---")
st.caption("Developed as part of the **Indus Quantum Linguistic Reconstruction Project** 🧬")
