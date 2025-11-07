import streamlit as st
import json
import pandas as pd
import plotly.express as px
from utils.decoder_engine import decode_symbol_sequence, load_json, log
from utils.decoder_engine import load_json
import os

OUTPUT_PATH = './outputs/decoded_results.json'

if not os.path.exists(OUTPUT_PATH) or os.path.getsize(OUTPUT_PATH) == 0:
    st.warning("Decoded results not found. Running decoder engine now...")
    from utils.decoder_engine import decode_all_sequences, save_output
    decoded_data = decode_all_sequences()
    save_output(decoded_data, OUTPUT_PATH)
else:
    decoded_data = load_json(OUTPUT_PATH)
    
# === PAGE CONFIG ===
st.set_page_config(
    page_title="Indus Script Quantum Decoder",
    layout="wide",
    page_icon="🔮"
)

# === TITLE ===
st.title("🔮 Indus Script Quantum Decoder")
st.markdown("This interactive tool visualizes the reconstructed Indus symbol logic and resonance analysis framework.")

# === LOAD CONFIG AND DATA ===
CONFIG_PATH = './models/model_config.json'
OUTPUT_PATH = './outputs/decoded_results.json'
SEQUENCES_PATH = './data/sequences.json'

config = load_json(CONFIG_PATH)
try:
    decoded_data = load_json(OUTPUT_PATH)
except FileNotFoundError:
    decoded_data = {}

# === SIDEBAR ===
st.sidebar.header("⚙️ Control Panel")

option = st.sidebar.selectbox(
    "Select View",
    ["Decoded Sequences", "Pattern Analysis", "Symbol Explorer", "Upload & Decode"]
)

# === VIEW 1: DECODED SEQUENCES ===
if option == "Decoded Sequences":
    st.subheader("🧩 Decoded Sequence Data")
    if decoded_data:
        for seq_id, content in decoded_data.items():
            st.markdown(f"### Sequence {seq_id}")
            df = pd.DataFrame(content['decoded_sequences'][0])
            fig = px.bar(
                df,
                x='symbol',
                y='combined_score',
                hover_data=['semantic_strength', 'harmonic_resonance'],
                title=f"Harmonic Resonance Map — {seq_id}"
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(df)
    else:
        st.warning("No decoded data found. Run the decoder first.")

# === VIEW 2: PATTERN ANALYSIS ===
elif option == "Pattern Analysis":
    st.subheader("🔁 Pattern Recognition Results")
    if decoded_data:
        pattern_summary = []
        for seq_id, content in decoded_data.items():
            pattern_summary.append({
                "Sequence ID": seq_id,
                "Patterns Found": len(content['patterns_detected'])
            })
        st.dataframe(pd.DataFrame(pattern_summary))
    else:
        st.warning("No pattern data found.")

# === VIEW 3: SYMBOL EXPLORER ===
elif option == "Symbol Explorer":
    st.subheader("🧠 Symbol Semantic and Resonance Explorer")
    symbol_input = st.text_input("Enter a symbol or short sequence (comma-separated):", "Spiral,Square")
    if st.button("Decode Symbol Sequence"):
        symbols = [s.strip() for s in symbol_input.split(",")]
        result = decode_symbol_sequence(symbols)
        df = pd.DataFrame(result)
        st.dataframe(df)
        fig = px.line(df, x='symbol', y='combined_score', markers=True, title="Symbol Energy Profile")
        st.plotly_chart(fig, use_container_width=True)
        avg_score = df['combined_score'].mean()
        st.success(f"Average combined resonance score: **{avg_score:.3f}**")

# === VIEW 4: UPLOAD & DECODE ===
elif option == "Upload & Decode":
    st.subheader("📤 Upload Your Own Sequence JSON")
    uploaded_file = st.file_uploader("Upload a JSON file containing new symbol sequences", type=['json'])
    if uploaded_file:
        data = json.load(uploaded_file)
        st.json(data)
        if st.button("Run Decoding"):
            st.info("Running decoding process...")
            results = {}
            for key, seq in data.items():
                sequences = seq.get('symbol_sequences', [])
                decoded = [decode_symbol_sequence(s) for s in sequences]
                results[key] = {"decoded_sequences": decoded}
            st.success("Decoding complete! Displaying results:")
            st.json(results)
            df = pd.DataFrame(results[list(results.keys())[0]]['decoded_sequences'][0])
            st.dataframe(df)

# === FOOTER ===
st.markdown("---")
st.caption("Developed as part of the Indus Script Quantum-Harmonic Reconstruction Project 🕉️")
