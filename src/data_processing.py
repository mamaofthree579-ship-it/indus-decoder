\"\"\"Data processing utilities (starter).
Functions:
- normalize_symbol_image: Accepts raw image bytes and returns a feature vector placeholder.
\"\"\"
from PIL import Image
import io, numpy as np

def normalize_symbol_image(img_bytes):
    \"\"\"Convert uploaded image to a simple normalized grayscale thumbnail and return as vector.
    This is a placeholder — replace with proper vectorization (SVG parsing, skeletonization, shape descriptors).
    \"\"\"
    img = Image.open(io.BytesIO(img_bytes)).convert("L")
    img = img.resize((64,64))
    arr = np.array(img)/255.0
    return arr.flatten()
