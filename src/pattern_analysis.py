\"\"\"Pattern analysis utilities (starter).
Provide adjacency analysis, Markov-style prediction placeholders.
\"\"\"
import numpy as np
def build_dummy_markov():
    # simple dummy adjacency matrix for demo purposes
    symbols = ['Fish','Jar','Spiral','Square','Grid','DotCircle','Knot','Arrow']
    mat = np.random.rand(len(symbols), len(symbols))
    return symbols, mat