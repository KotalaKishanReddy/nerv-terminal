"""Thin re-export shim — update logic lives in root run.py."""
from __future__ import annotations
import sys, os
from pathlib import Path

def check_and_update(nerv_py=None):
    """Delegates to run.py auto_update() to keep a single source of truth."""
    run_py = Path(__file__).resolve().parent.parent / 'run.py'
    if run_py not in sys.path and str(run_py.parent) not in sys.path:
        sys.path.insert(0, str(run_py.parent))
    import run as _run  # type: ignore
    return _run.auto_update()
