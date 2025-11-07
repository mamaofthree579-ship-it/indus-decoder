\"\"\"Utility helpers.\"\"\"
import os
def resource_path(*parts):
    here = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(here, "..", *parts))