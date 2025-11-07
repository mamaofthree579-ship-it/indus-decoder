import streamlit as st
import json
import os
import pandas as pd
import plotly.express as px
from utils.decoder_engine import decode_all_sequences, save_output, log, CONFIG_PATH, SEQUENCES_PATH

# === PAGE CONFIG ===
st.set_page_config(
    page_title="Indus Script Quantum Decoder",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === LOAD CONFIG AND DATA ===
with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

with open(SEQUENCES_PATH, 'r', encoding='utf-8') as f:
    sequences = json.load(f)

OUTPUT_FILE = config['output']['decoded_sequences_file']


# === SIDEBAR CONTROLS ===
st.sidebar.title("🔍 Indus Script Quantum Decoder")
st.sidebar.markdown("Explore decoded sequences, resonance maps, and harmonic structures.")

run_decoding = st.sidebar.button("Run Full Decoding 🔄")
st.sidebar.markdown("---")

show_patterns = st.sidebar.checkbox("Show Detected Patterns", True)
show_resonance = st.sidebar.checkbox("Show Harmonic Resonance Chart", True)
show_semantics = st.sidebar.checkbox("Show Semantic Strength Table", True)
show_network = st.sidebar.checkbox("Show Symbol Relationship Network", True)

st.sidebar.markdown("---")
st.sidebar.caption("Developed with ❤️ using Open Source Fractal-Decoding Framework")


# === HEADER ===
st.title("🧬 Indus Script Decoding Dashboard")
st.write("This interface visualizes the decoded Indus symbol system using harmonic, semantic, and fractal analysis methods.")


# === MAIN EXECUTION ===
if run_decoding:
    st.info("Running decoding process... Please wait.")
    results = decode_all_sequences()
    save_output(results, OUTPUT_FILE)
    st.success("✅ Decoding complete! Results saved and loaded.")
else:
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        st.warning("No decoded results found. Please run decoding first.")
        st.stop()


# === DISPLAY OUTPUT ===
sequence_options = list(results.keys())
selected_sequence = st.selectbox("Select Sequence to Explore", sequence_options)

if selected_sequence:
    seq_data = results[selected_sequence]
    decoded_sequences = seq_data["decoded_sequences"]
    patterns = seq_data["patterns_detected"]

    st.subheader(f"📜 Sequence: {selected_sequence}")
    st.markdown(f"**Patterns detected:** {len(patterns)}")

    if show_patterns:
        st.code(json.dumps(patterns, indent=2))

    # Flatten data for visualization
    flattened = []
    for seq in decoded_sequences:
        for symbol_data in seq:
            flattened.append(symbol_data)

    df = pd.DataFrame(flattened)

    if show_semantics:
        st.subheader("🧩 Semantic Strength Overview")
        st.dataframe(df)

    if show_resonance:
        st.subheader("🎵 Harmonic Resonance Distribution")
        fig = px.scatter(
            df,
            x="semantic_strength",
            y="harmonic_resonance",
            color="combined_score",
            size="combined_score",
            hover_data=["symbol"],
            title="Semantic vs Harmonic Resonance Map"
        )
        st.plotly_chart(fig, use_container_width=True)

    if show_network:
        st.subheader("🌐 Symbol Relationship Network")
        st.markdown("*(Planned Feature)* — this will visualize symbol co-occurrences as a resonance-based graph network.")


# === FOOTER ===
st.markdown("---")
st.caption("© 2025 Quantum Archaeology Foundation | Open-Source Indus Decoding Framework")
