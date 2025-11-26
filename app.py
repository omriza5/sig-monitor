from flask import Flask
from dotenv import load_dotenv
import requests
import os

load_dotenv() 

DEFAULT_INTELLIGENCE_ADJACENT = os.getenv("TARGET_DOMAIN", "bellingcat.com")
DEFAULT_SIGNAL_FILE = os.getenv("SIGNAL_FILE", "data/signals.jsonl")
DEFAULT_MAX_RECORDS = os.getenv("MAX_RECORDS", 100)

INTELLIGENCE_ADJACENT_API = f"https://web.archive.org/cdx/search/cdx?url={DEFAULT_INTELLIGENCE_ADJACENT}/*&output=json&limit=10"

app = Flask(__name__)

@app.route('/health')
def health():
    return "OK" , 200

def get_signals():
    response = requests.get(INTELLIGENCE_ADJACENT_API)
    data = response.json()
    

# get_signals()

if __name__ == '__main__':
    app.run(debug=True, port=8000)