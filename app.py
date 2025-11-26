from flask import Flask, jsonify
from dotenv import load_dotenv
import requests
import json
import os
from datetime import datetime
from urllib.parse import urlparse

load_dotenv() 

INTELLIGENCE_ADJACENT = os.getenv("TARGET_DOMAIN", "bellingcat.com")
SIGNAL_FILE = os.getenv("SIGNAL_FILE", "data/signals.jsonl")
MAX_RECORDS = os.getenv("MAX_RECORDS", 100)
APP_PORT= os.getenv("APP_PORT", 8000)

INTELLIGENCE_ADJACENT_API = f"https://web.archive.org/cdx/search/cdx?url={INTELLIGENCE_ADJACENT}/*&output=json&limit=10"

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/stats')
def stats():
    try:
        data = get_signals()
        write_signals_to_jsonl(data)
        
        agrregated_stats = get_statistics()
        print("Done!")
        return jsonify(agrregated_stats), 200
    except Exception as e:
        print(f"Error fetching signals: {e}")
        return jsonify(e), 400

def get_statistics():
    """
    Reads signals.jsonl and returns aggregated statistics.
    """
    try:    
        signals = read_signals(SIGNAL_FILE)
        return aggregate_events(signals)
    except Exception as e:
        print(f"Error aggregating statistics: {e}")
        raise

def aggregate_events(events):
    print("Aggregating signals...")
    stats = {
            "total_events": 0,
            "by_source": {},
            "by_protocol": {}
    }
    
    for event in events:    
        # Count total events
        stats["total_events"] += 1
                
        # Count by source
        source = event.get("source", "unknown")
        stats["by_source"][source] = stats["by_source"].get(source, 0) + 1
                
        # Count by protocol
        protocol = event.get("protocol", "unknown")
        stats["by_protocol"][protocol] = stats["by_protocol"].get(protocol, 0) + 1
    
    return stats
def get_signals():
    try:
        print("Getting signals...")
        response = requests.get(INTELLIGENCE_ADJACENT_API)
        return response.json()
    except Exception as e:
        print(f"Error fetching signals: {e}")
        raise


def read_signals(filename=SIGNAL_FILE):
    result = []
    try:
        print("Reading signals...")
        with open(filename, 'r') as f:
            for line in f:
                result.append(json.loads(line.strip()))
        return result
    except FileNotFoundError:
        print(f"File not found: {SIGNAL_FILE}")
        return {"total_events": 0, "by_source": {}, "by_protocol": {}}
    
    
def write_signals_to_jsonl(data, filename=SIGNAL_FILE):
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
        raise
        
def map_record(record):
    mapped = {}
    if 'timestamp' in record:
        timestamp = record['timestamp']
        dt = datetime.strptime(timestamp, '%Y%m%d%H%M%S')
        mapped['timestamp'] = dt.isoformat()
    if 'original' in record:
        protocol = extract_protocol_part(record['original'])
        mapped['protocol'] = protocol
        mapped['source'] = INTELLIGENCE_ADJACENT
    if 'length' in record:
        mapped['bytes'] = record['length'] or 0
    if 'statuscode' in record:
        status_code = record['statuscode']
        mapped['status'] = 'ok' if status_code.startswith('2') else 'error'
    
    return mapped
        
def extract_protocol_part(url):
    """
    Extracts protocol and domain from URL.
    Example: 'http://www.bellingcat.com:80/' 
    Returns: 'http'
    """
    parsed = urlparse(url)
    return parsed.scheme


if __name__ == '__main__':
    app.run(debug=True, port=APP_PORT)