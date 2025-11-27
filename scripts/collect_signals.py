import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import get_signals, write_signals_to_jsonl

if __name__ == '__main__':
    data = get_signals()
    write_signals_to_jsonl(data)
    print("Done! Signals written to file.")