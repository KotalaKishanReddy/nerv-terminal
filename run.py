#!/usr/bin/env python3
"""
NERV Terminal — self-update bootstrap
This is the entry-point. It checks GitHub for a newer version of nerv.py
before launching it. Works on Linux, macOS, Windows (Git Bash / PowerShell).
"""
import sys, os, json, hashlib, subprocess, time
from pathlib import Path

HERE       = Path(__file__).resolve().parent
NERV_PY    = HERE / 'nerv.py'
VERSION_URL = 'https://api.github.com/repos/KotalaKishanReddy/nerv-terminal/commits/main'
RAW_BASE    = 'https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main'
CACHE_FILE  = HERE / '.nerv_last_sha'
UPDATE_TTL  = 3600   # check at most once per hour

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
    age = time.time() - CACHE_FILE.stat().st_mtime
    return age > UPDATE_TTL

def auto_update() -> bool:
    """Pull nerv.py from GitHub if a newer commit exists. Returns True if updated."""
    if not _needs_check():
        return False
    raw = _fetch(VERSION_URL)
    if not raw:
        return False
    try:
        data = json.loads(raw)
        remote_sha = data['sha']
    except Exception:
        return False
    local_sha = CACHE_FILE.read_text().strip() if CACHE_FILE.exists() else ''
    if remote_sha == local_sha:
        CACHE_FILE.touch()
        return False
    # New commit — download fresh nerv.py
    new_src = _fetch(f'{RAW_BASE}/nerv.py')
    if not new_src or len(new_src) < 512:
        return False
    tmp = NERV_PY.with_suffix('.tmp')
    tmp.write_bytes(new_src)
    tmp.replace(NERV_PY)
    CACHE_FILE.write_text(remote_sha)
    return True

def ensure_deps():
    """Install/upgrade blessed and pycryptodome inside the current Python env."""
    try:
        import blessed, Crypto  # noqa: F401
    except ImportError:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '--quiet',
             '--upgrade', 'blessed', 'pycryptodome'],
            check=False
        )

def main():
    ensure_deps()
    updated = auto_update()

    # Brief flash in terminal if an update was applied
    if updated:
        RED   = '\033[38;2;210;25;25m'
        AMBER = '\033[38;2;255;170;0m'
        RESET = '\033[0m'
        print(f'{RED}  [ NERV ]  {AMBER}Auto-update applied — launching new version…{RESET}')
        time.sleep(0.8)

    if not NERV_PY.exists():
        print('nerv.py not found and could not be downloaded. Check your connection.')
        sys.exit(1)

    # Replace the current process with the updated nerv.py
    os.execv(sys.executable, [sys.executable, str(NERV_PY)] + sys.argv[1:])

if __name__ == '__main__':
    main()
