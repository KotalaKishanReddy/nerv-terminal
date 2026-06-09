#!/usr/bin/env bash
set -e

RED='\033[38;2;210;25;25m'
AMBER='\033[38;2;255;170;0m'
GREEN='\033[38;2;0;210;90m'
DIM='\033[38;2;75;65;55m'
RESET='\033[0m'

echo
echo -e "${RED}  ███╗   ██╗███████╗██████╗ ██╗   ██╗${RESET}"
echo -e "${RED}  ████╗  ██║██╔════╝██╔══██╗██║   ██║${RESET}"
echo -e "${RED}  ██╔██╗ ██║█████╗  ██████╔╝██║   ██║${RESET}"
echo -e "${RED}  ██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝${RESET}"
echo -e "${RED}  ██║ ╚████║███████╗██║  ██║ ╚████╔╝ ${RESET}"
echo -e "${RED}  ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ${RESET}"
echo -e "${DIM}  GEHIRN ADVANCED RESEARCH — INSTALLER v1.1${RESET}"
echo

cmd()  { command -v "$1" &>/dev/null; }
ok()   { echo -e "${GREEN}  [ ✓ ] $*${RESET}"; }
warn() { echo -e "${AMBER}  [ * ] $*${RESET}"; }
err()  { echo -e "${RED}  [ ! ] $*${RESET}"; }

# ── python check ──────────────────────────────────────────────────────────────
warn "Checking dependencies..."
if ! cmd python3; then
  err "python3 not found. Install Python 3.8+ first."; exit 1
fi
PYVER=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYVER" -lt 8 ]; then
  err "Python 3.8+ required. Found 3.${PYVER}."; exit 1
fi
ok "Python 3.${PYVER} found"

# ── download nerv.py ──────────────────────────────────────────────────────────
RAW="https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/nerv.py"
warn "Downloading nerv.py..."
if cmd curl; then
  curl -fsSL "$RAW" -o "/tmp/nerv_main.py"
elif cmd wget; then
  wget -qO "/tmp/nerv_main.py" "$RAW"
else
  err "Neither curl nor wget found."; exit 1
fi
ok "Downloaded nerv.py"

# ── detect if pip is externally managed (Arch, Ubuntu 23+, etc.) ─────────────
PIP_BIN=""
cmd pip3 && PIP_BIN="pip3" || true
[ -z "$PIP_BIN" ] && cmd pip && PIP_BIN="pip" || true

USE_VENV=0
if [ -n "$PIP_BIN" ]; then
  # test if pip will refuse due to PEP 668
  if $PIP_BIN install --dry-run --quiet blessed 2>&1 | grep -q 'externally-managed'; then
    USE_VENV=1
  fi
else
  USE_VENV=1
fi

VENV="$HOME/.local/share/nerv-venv"
DEST="$HOME/.local/bin/nerv"
mkdir -p "$HOME/.local/bin"

if [ "$USE_VENV" -eq 1 ]; then
  warn "System pip is externally managed — using isolated venv..."
  warn "Creating venv at ${VENV}..."
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install --quiet --upgrade blessed pyfiglet
  cp /tmp/nerv_main.py "$VENV/nerv.py"
  # write a tiny bash launcher that uses the venv python
  cat > "$DEST" << LAUNCHER
#!/usr/bin/env bash
exec "$VENV/bin/python3" "$VENV/nerv.py" "\$@"
LAUNCHER
  chmod +x "$DEST"
else
  warn "Installing packages (blessed, pyfiglet)..."
  $PIP_BIN install --quiet --upgrade blessed pyfiglet
  cp /tmp/nerv_main.py "$DEST"
  chmod +x "$DEST"
  # ensure shebang is correct
  sed -i '1s|.*|#!/usr/bin/env python3|' "$DEST"
fi

ok "Packages installed"
ok "Launcher written to ${DEST}"

# ── PATH reminder ──────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo
  warn "~/.local/bin is not in your PATH. Add this to ~/.bashrc or ~/.zshrc:"
  echo -e "${DIM}        export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
  warn "Then reload:  source ~/.bashrc"
fi

echo
ok "Done! Run:  nerv"
echo
