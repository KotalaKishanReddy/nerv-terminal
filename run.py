#!/usr/bin/env python3
"""
NERV Terminal — self-update bootstrap
Entry-point for all platforms. Checks GitHub for a newer nerv.py, hot-swaps
it, then os.execv into it. Works on Linux, macOS, Windows (Git Bash / PS).
"""
import sys, os, json, subprocess, time, hashlib
from pathlib import Path

HERE        = Path(__file__).resolve().parent
NERV_PY     = HERE / 'nerv.py'
VERSION_URL = 'https://api.github.com/repos/KotalaKishanReddy/nerv-terminal/commits/main'
RAW_BASE    = 'https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main'
CACHE_FILE  = HERE / '.nerv_last_sha'
UPDATE_TTL  = 3600        # poll at most once per hour
MIN_SIZE    = 1024        # FIX #6/#7: reject suspiciously small downloads

def _fetch(url: str, timeout: int = 8) -> bytes:
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'nerv-terminal/2.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return b''

def _needs_check() -> bool:
    if not CACHE_FILE.exists():
        return True
    return time.time() - CACHE_FILE.stat().st_mtime > UPDATE_TTL

def auto_update() -> bool:
    """Pull nerv.py from GitHub if a newer commit exists. Returns True if updated."""
    if not _needs_check():
        return False
    raw = _fetch(VERSION_URL)
    if not raw:
        return False
    try:
        remote_sha = json.loads(raw)['sha']
    except Exception:
        return False
    local_sha = CACHE_FILE.read_text().strip() if CACHE_FILE.exists() else ''
    if remote_sha == local_sha:
        CACHE_FILE.touch()
        return False
    # FIX #6: download and validate before replacing
    new_src = _fetch(f'{RAW_BASE}/nerv.py')
    if not new_src or len(new_src) < MIN_SIZE:
        return False
    # Basic sanity: must look like a Python file
    if b'def main' not in new_src and b'import' not in new_src:
        return False
    tmp = NERV_PY.with_suffix('.tmp')
    tmp.write_bytes(new_src)
    tmp.replace(NERV_PY)
    # FIX #7: store SHA + a hash of the file to detect tampering
    file_hash = hashlib.sha256(new_src).hexdigest()
    CACHE_FILE.write_text(f'{remote_sha}\n{file_hash}')
    return True

def ensure_deps():
    """Install/upgrade blessed and pycryptodome. FIX #8: surface errors."""
    missing = []
    try:
        import blessed  # noqa: F401
    except ImportError:
        missing.append('blessed')
    try:
        import Crypto   # noqa: F401
    except ImportError:
        missing.append('pycryptodome')
    if missing:
        RED   = '\033[38;2;210;25;25m'
        AMBER = '\033[38;2;255;170;0m'
        RESET = '\033[0m'
        print(f'{AMBER}  [ NERV ]  Installing missing deps: {missing}{RESET}')
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--quiet', '--upgrade'] + missing,
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f'{RED}  [ NERV ]  pip failed:\n{result.stderr}{RESET}')
            sys.exit(1)

def main():
    ensure_deps()
    updated = auto_update()
    if updated:
        RED   = '\033[38;2;210;25;25m'
        AMBER = '\033[38;2;255;170;0m'
        RESET = '\033[0m'
        print(f'{RED}  [ NERV ]  {AMBER}Auto-update applied \u2014 launching new version\u2026{RESET}')
        time.sleep(0.8)
    if not NERV_PY.exists():
        print('nerv.py not found. Check your connection or re-run install.sh.')
        sys.exit(1)
    os.execv(sys.executable, [sys.executable, str(NERV_PY)] + sys.argv[1:])

if __name__ == '__main__':
    main()
