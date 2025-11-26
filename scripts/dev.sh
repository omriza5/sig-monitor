#!/bin/bash

# Get the command argument
COMMAND=$1

case $COMMAND in
  test)
    pytest
    ;;
  
  collect)
    python3 collect_signals.py
    ;;
  
  run-local)
    python3 app.py
    ;;
  
  *)
    echo "Usage: ./dev.sh {test|collect|run-local}"
    echo ""
    exit 1
    ;;
esac
