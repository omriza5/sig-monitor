from app import get_signals, write_signals_to_jsonl

if __name__ == '__main__':
    data = get_signals()
    write_signals_to_jsonl(data)
    print("Done! Signals written to file.")