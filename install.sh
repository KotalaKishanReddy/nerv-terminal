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
echo -e "${DIM}  GEHIRN ADVANCED RESEARCH — INSTALLER v1.0${RESET}"
echo

# ── dependency check ──────────────────────────────────────────────────────────
check() {
  command -v "$1" &>/dev/null
}

echo -e "${AMBER}  [ * ] Checking dependencies...${RESET}"

if ! check python3; then
  echo -e "${RED}  [ ! ] python3 not found. Install Python 3.8+ first.${RESET}"
  exit 1
fi

PYVER=$(python3 -c 'import sys; print(sys.version_info.minor)')
if [ "$PYVER" -lt 8 ]; then
  echo -e "${RED}  [ ! ] Python 3.8+ required. Found 3.${PYVER}.${RESET}"
  exit 1
fi

if ! check pip3 && ! check pip; then
  echo -e "${RED}  [ ! ] pip not found. Install pip first.${RESET}"
  exit 1
fi

PIP=$(check pip3 && echo pip3 || echo pip)

echo -e "${GREEN}  [ ✓ ] Python 3.${PYVER} found${RESET}"

# ── install python deps ────────────────────────────────────────────────────────
echo -e "${AMBER}  [ * ] Installing Python packages (blessed, pyfiglet)...${RESET}"
$PIP install --quiet --upgrade blessed pyfiglet
echo -e "${GREEN}  [ ✓ ] Packages installed${RESET}"

# ── download nerv.py ──────────────────────────────────────────────────────────
DEST="$HOME/.local/bin/nerv"
mkdir -p "$HOME/.local/bin"

echo -e "${AMBER}  [ * ] Downloading nerv.py...${RESET}"

if check curl; then
  curl -fsSL "https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/nerv.py" -o "$DEST"
elif check wget; then
  wget -qO "$DEST" "https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/nerv.py"
else
  echo -e "${RED}  [ ! ] Neither curl nor wget found. Cannot download.${RESET}"
  exit 1
fi

chmod +x "$DEST"
echo -e "${GREEN}  [ ✓ ] Installed to ${DEST}${RESET}"

# ── PATH check ────────────────────────────────────────────────────────────────
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
  echo
  echo -e "${AMBER}  [ ! ] Add this to your shell config (~/.bashrc or ~/.zshrc):${RESET}"
  echo -e "${DIM}        export PATH=\"\$HOME/.local/bin:\$PATH\"${RESET}"
  echo
fi

echo -e "${GREEN}  [ ✓ ] Done. Run:  nerv${RESET}"
echo
