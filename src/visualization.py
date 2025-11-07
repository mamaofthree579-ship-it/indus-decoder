\"\"\"Visualization helpers (starter).
Provides simple demo plots for adjacency and interface diagram placeholders.
\"\"\"
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

def plot_adjacency_graph():
    symbols = ['Fish','Jar','Spiral','Square','Grid','DotCircle','Knot','Arrow']
    G = nx.DiGraph()
    for s in symbols:
        G.add_node(s)
    # random edges demo
    for i in range(len(symbols)):
        for j in range(len(symbols)):
            if np.random.rand() > 0.7:
                G.add_edge(symbols[i], symbols[j])
    fig, ax = plt.subplots(figsize=(6,4))
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_size=700, font_size=9, ax=ax)
    st.pyplot(fig)

def show_interface_diagram():
    st.image("assets/visuals/quantum_interface_placeholder.png", caption="Quantum-Holographic Interface (placeholder)")