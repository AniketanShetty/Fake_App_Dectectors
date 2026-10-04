import json
import os

# Path to this file's directory
BASE_DIR = os.path.dirname(__file__)

# Path to the JSON metadata file
OFFICIAL_META_PATH = os.path.join(BASE_DIR, "dataset", "phonepe_official.json")

# Load metadata at import time
with open(OFFICIAL_META_PATH, "r", encoding="utf-8") as f:
    OFFICIAL_PHONEPE_META = json.load(f)
