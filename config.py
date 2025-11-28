import os


INTELLIGENCE_ADJACENT = os.getenv("TARGET_DOMAIN", "bellingcat.com")
INTELLIGENCE_ADJACENT_API = f"https://web.archive.org/cdx/search/cdx?url={INTELLIGENCE_ADJACENT}/*&output=json&limit=10"
SIGNAL_FILE = os.getenv("SIGNAL_FILE", "data/signals.jsonl")
MAX_RECORDS = os.getenv("MAX_RECORDS", 100)
APP_PORT= os.getenv("APP_PORT", 8000)