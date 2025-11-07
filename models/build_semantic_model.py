import pickle
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

# ---------------------------------------------------
# STEP 1: Define your symbolic lexicon and seed meanings
# ---------------------------------------------------
# These are sample entries – expand or replace them
symbolic_lexicon = {
    "spiral_arrow": "energy flow initiation directional control torsion scalar field vortex rotation",
    "nested_squares": "dimensional layering compression cubic boundary merkaba geometric structure",
    "ladder_step": "frequency ascension harmonic stacking resonance consciousness field",
    "lattice_mesh": "stabilization field projection network linkage grid scalar ley lines",
    "dual_circles": "dual polarity charge balance scalar coupling electromagnetic symmetry",
    "dot_circle": "field focus point zero consciousness connection resonance mandala center",
    "knot_loop": "information entanglement resonance link quantum coupling entangled field",
}

# ---------------------------------------------------
# STEP 2: Create text representations
# ---------------------------------------------------
symbols = list(symbolic_lexicon.keys())
descriptions = [symbolic_lexicon[s] for s in symbols]

# ---------------------------------------------------
# STEP 3: Build pipeline for semantic embedding
# ---------------------------------------------------
# 1. TF-IDF to vectorize symbolic descriptions
# 2. PCA to compress to lower-dimensional semantic space
semantic_pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(max_features=100)),
    ('pca', PCA(n_components=3))
])

semantic_vectors = semantic_pipeline.fit_transform(descriptions)

# ---------------------------------------------------
# STEP 4: Assemble the semantic model dictionary
# ---------------------------------------------------
semantic_model = {
    "symbols": symbols,
    "descriptions": descriptions,
    "embeddings": semantic_vectors,
    "pipeline": semantic_pipeline
}

# ---------------------------------------------------
# STEP 5: Save model as .pkl
# ---------------------------------------------------
with open('semantic_model.pkl', 'wb') as f:
    pickle.dump(semantic_model, f)

print("✅ semantic_model.pkl successfully created.")
