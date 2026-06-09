#!/usr/bin/env bash
# NERV Terminal — one-line installer + auto-update bootstrap
# Usage: curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.sh | bash
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
echo -e "${DIM}  GEHIRN ADVANCED RESEARCH — INSTALLER v2.0${RESET}"
echo

cmd()  { command -v "$1" &>/dev/null; }
ok()   { echo -e "${GREEN}  [ ✓ ] $*${RESET}"; }
warn() { echo -e "${AMBER}  [ * ] $*${RESET}"; }
err()  { echo -e "${RED}  [ ! ] $*${RESET}"; }

# ── detect OS ──────────────────────────────────────────────────────────────────
OS="linux"
[[ "$OSTYPE" == darwin* ]] && OS="mac"
[[ "$OS" == "Windows_NT" || -n "$WINDIR" ]] && OS="windows"
ok "Detected OS: ${OS}"

# ── python check ──────────────────────────────────────────────────────────────
warn "Checking Python..."
PYCMD=""
cmd python3 && PYCMD="python3"
[ -z "$PYCMD" ] && cmd python && PYCMD="python"
[ -z "$PYCMD" ] && { err "Python 3.8+ not found. Install from https://python.org"; exit 1; }
PYVER=$("$PYCMD" -c 'import sys; print(sys.version_info.minor)')
[ "$PYVER" -lt 8 ] && { err "Python 3.8+ required. Found 3.${PYVER}."; exit 1; }
ok "Python 3.${PYVER} found"

# ── clone or download repo ────────────────────────────────────────────────────
INSTALL_DIR="$HOME/.local/share/nerv-terminal"
warn "Installing to ${INSTALL_DIR}..."
if cmd git; then
  if [ -d "$INSTALL_DIR/.git" ]; then
    warn "Repo exists — pulling latest..."
    git -C "$INSTALL_DIR" pull --ff-only --quiet
    ok "Updated to latest"
  else
    git clone --depth 1 --quiet https://github.com/KotalaKishanReddy/nerv-terminal.git "$INSTALL_DIR"
    ok "Cloned repo"
  fi
else
  warn "git not found — downloading via curl/wget..."
  mkdir -p "$INSTALL_DIR"
  RAW="https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main"
  for f in nerv.py run.py requirements.txt; do
    if cmd curl; then
      curl -fsSL "${RAW}/${f}" -o "${INSTALL_DIR}/${f}"
    elif cmd wget; then
      wget -qO "${INSTALL_DIR}/${f}" "${RAW}/${f}"
    else
      err "Neither git, curl, nor wget found. Install one and retry."; exit 1
    fi
  done
  ok "Downloaded files"
fi

# ── venv setup ────────────────────────────────────────────────────────────────
VENV="$INSTALL_DIR/.venv"
warn "Setting up isolated venv at ${VENV}..."
"$PYCMD" -m venv "$VENV"
PY="$VENV/bin/python3"
[ ! -f "$PY" ] && PY="$VENV/bin/python"
[ ! -f "$PY" ] && PY="$VENV/Scripts/python.exe"   # Windows
warn "Installing Python deps..."
"$PY" -m pip install --quiet --upgrade pip
"$PY" -m pip install --quiet --upgrade blessed pycryptodome
ok "Dependencies installed"

# ── write launcher ────────────────────────────────────────────────────────────
mkdir -p "$HOME/.local/bin"
DEST="$HOME/.local/bin/nerv"
cat > "$DEST" << LAUNCHER
#!/usr/bin/env bash
exec "${PY}" "${INSTALL_DIR}/run.py" "\$@"
LAUNCHER
chmod +x "$DEST"
ok "Launcher written: ${DEST}"

# ── PATH reminder ─────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo
  warn "Add to your shell profile (~/.bashrc / ~/.zshrc):"
  echo -e "${DIM}      export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
  warn "Then run:  source ~/.bashrc"
fi

echo
ok "NERV Terminal installed. Run:  nerv"
echo -e "${DIM}  Updates are automatic on every launch.${RESET}"
echo
