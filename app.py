from flask import Flask
from dotenv import load_dotenv
import requests
import json
import os
from datetime import datetime
from urllib.parse import urlparse

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
    try:
        print("Getting signals...")
        response = requests.get(INTELLIGENCE_ADJACENT_API)
        return response.json()
    except Exception as e:
        print(f"Error fetching signals: {e}")


def write_signals_to_jsonl(data, filename=DEFAULT_SIGNAL_FILE):
    """
    Writes array of arrays to JSONL file.
    First row is treated as column headers.
    """
    if not data or len(data) < 2:
        print("No data to write")
        return
    
    headers = data[0]  
    rows = data[1:]   
    
    try:
        print(f"Writing signals to {filename}...")
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            for row in rows:
                record = dict(zip(headers, row))
                mapped = map_record(record) 
                f.write(json.dumps(mapped) + '\n')
                
    except Exception as e:
        print(f"Error writing to file: {e}")
        
def map_record(record):
    mapped = {}
    if 'timestamp' in record:
        timestamp = record['timestamp']
        dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        mapped['timestamp'] = dt.isoformat()
    if 'original' in record:
        protocol, source = extract_url_parts(record['original'])
        mapped['protocol'] = protocol
        mapped['source'] = source
    if 'length' in record:
        mapped['bytes'] = record['length']
    if 'statuscode' in record:
        pass
    
    return mapped
        
def extract_url_parts(url):
    """
    Extracts protocol and domain from URL.
    Example: 'http://www.bellingcat.com:80/' 
    Returns: ('http', 'www.bellingcat.com')
    """
    parsed = urlparse(url)
    protocol = parsed.scheme
    domain = parsed.hostname  # or parsed.netloc for 'www.bellingcat.com:80'
    
    return protocol, domain



def main():
    try:
        data = get_signals()
        write_signals_to_jsonl(data)
    except Exception as e:
        print(f"Something went wrong: {e}")

# main()

if __name__ == '__main__':
    app.run(debug=True, port=8000)