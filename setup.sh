#!/usr/bin/env bash
set -e
echo "[NERV] Installing dependencies..."
pip install -r requirements.txt
echo "[NERV] Launching..."
python nerv.py
