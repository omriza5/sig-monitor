from flask import Flask, jsonify
from dotenv import load_dotenv
from config import APP_PORT
from scripts.collect_signals import get_signals, write_signals_to_jsonl, get_statistics

load_dotenv() 

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

if __name__ == '__main__':
    app.run(debug=True, port=int(APP_PORT), host='0.0.0.0')