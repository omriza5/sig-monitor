from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv() 

DEFAULT_INTELLIGENCE_ADJACENT = os.getenv("TARGET_DOMAIN", "bellingcat.com")
DEFAULT_SIGNAL_FILE = os.getenv("SIGNAL_FILE", "data/signals.jsonl")
DEFAULT_MAX_RECORDS = os.getenv("MAX_RECORDS", 100)

INTELLIGENCE_ADJACENT_API = f"https://web.archive.org/cdx/search/cdx?url={DEFAULT_INTELLIGENCE_ADJACENT}/*&output=json"

print(INTELLIGENCE_ADJACENT_API)
app = Flask(__name__)

@app.route('/health')
def health():
    return "OK" , 200

if __name__ == '__main__':
    app.run(debug=True, port=8000)