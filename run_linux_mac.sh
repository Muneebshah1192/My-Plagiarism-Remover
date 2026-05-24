#!/usr/bin/env bash
set -e
echo "Starting Originality Studio Pro..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
python app.py
