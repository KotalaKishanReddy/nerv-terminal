"""Standalone updater module — also importable by nerv.py at runtime."""
import json, sys, time
from pathlib import Path

HERE        = Path(__file__).resolve().parent.parent
CACHE_FILE  = HERE / '.nerv_last_sha'
VERSION_URL = 'https://api.github.com/repos/KotalaKishanReddy/nerv-terminal/commits/main'
RAW_BASE    = 'https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main'
UPDATE_TTL  = 3600


def _fetch(url: str, timeout: int = 8) -> bytes:
    try:
        import urllib.request
        req = urllib.request.Request(url, headers={'User-Agent': 'nerv-terminal/2.0'})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return b''


def check_and_update(nerv_py: Path = HERE / 'nerv.py') -> bool:
    """Returns True if nerv.py was replaced with a newer version."""
    if CACHE_FILE.exists() and time.time() - CACHE_FILE.stat().st_mtime < UPDATE_TTL:
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
        CACHE_FILE.touch(); return False
    new_src = _fetch(f'{RAW_BASE}/nerv.py')
    if not new_src or len(new_src) < 512:
        return False
    tmp = nerv_py.with_suffix('.tmp')
    tmp.write_bytes(new_src)
    tmp.replace(nerv_py)
    CACHE_FILE.write_text(remote_sha)
    return True
