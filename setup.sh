#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  NERV Terminal — Self-contained launcher
#  Works on Arch, Ubuntu, Debian, macOS, WSL
#  curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/setup.sh | bash
# ─────────────────────────────────────────────────────────────
set -e

RED='\033[1;31m'
AMBER='\033[1;33m'
DIM='\033[2m'
NC='\033[0m'

log()  { echo -e "${RED}[NERV]${NC} $*"; }
info() { echo -e "${AMBER}  >>>${NC} $*"; }

log "MAGI SYSTEM INITIALIZING..."
echo ""

# ── 1. Find python3 ──────────────────────────────────────────
PY=""
for cmd in python3 python; do
  if command -v "$cmd" &>/dev/null; then
    PY="$cmd"
    break
  fi
done
[[ -z "$PY" ]] && { log "Python 3 not found. Install it first."; exit 1; }
info "Using Python: $($PY --version)"

# ── 2. Decide where to put the code ──────────────────────────
# If run via curl|bash, download to ~/.nerv-terminal
# If run from inside a clone, use current directory
if [[ -f "$(dirname "$0")/nerv.py" ]]; then
  NERV_DIR="$(cd "$(dirname "$0")" && pwd)"
  info "Running from local clone: $NERV_DIR"
else
  NERV_DIR="$HOME/.nerv-terminal"
  log "Downloading NERV Terminal to $NERV_DIR ..."
  if command -v git &>/dev/null; then
    if [[ -d "$NERV_DIR/.git" ]]; then
      info "Updating existing clone..."
      git -C "$NERV_DIR" pull --quiet
    else
      git clone --quiet https://github.com/KotalaKishanReddy/nerv-terminal.git "$NERV_DIR"
    fi
  elif command -v curl &>/dev/null; then
    mkdir -p "$NERV_DIR"
    curl -fsSL "https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/nerv.py" \
      -o "$NERV_DIR/nerv.py"
    curl -fsSL "https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/requirements.txt" \
      -o "$NERV_DIR/requirements.txt"
  else
    log "Neither git nor curl found. Cannot download."; exit 1
  fi
  info "Downloaded to $NERV_DIR"
fi

cd "$NERV_DIR"

# ── 3. Create or reuse a virtual environment ─────────────────
VENV_DIR="$NERV_DIR/.venv"
if [[ ! -d "$VENV_DIR" ]]; then
  info "Creating virtual environment..."
  $PY -m venv "$VENV_DIR"
fi

PIP="$VENV_DIR/bin/pip"
PYTHON="$VENV_DIR/bin/python"

# ── 4. Install dependencies ───────────────────────────────────
info "Installing dependencies (blessed, pyfiglet)..."
"$PIP" install --quiet --upgrade pip
"$PIP" install --quiet -r requirements.txt

echo ""
log "ALL SYSTEMS NOMINAL. LAUNCHING PILOT INTERFACE..."
echo ""
sleep 0.4

# ── 5. Launch ─────────────────────────────────────────────────
"$PYTHON" nerv.py
