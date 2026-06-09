# 🔴 NERV Terminal

**Neon Genesis Evangelion themed terminal launcher — one command, zero setup**

```
███████████████████████████████████████████
█  NERV // GEHIRN ADVANCED RESEARCH        █
█  MAGI SYSTEM v3.0 | TOKYO-3 NETWORK      █
███████████████████████████████████████████
```

---

## ⚡ One-liner (curl | bash)

```bash
curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/setup.sh | bash
```

That's it. No `pip install`, no venv setup, no cloning. Paste and watch it boot.

---

## Manual install (clone)

```bash
git clone https://github.com/KotalaKishanReddy/nerv-terminal
cd nerv-terminal
bash setup.sh
```

---

## What `setup.sh` does

1. Detects your Python 3 installation
2. Downloads the repo (if run via curl) or uses the local clone
3. Creates an isolated `.venv` — **no system packages touched** (fixes Arch `externally-managed-environment`)
4. Installs `blessed` + `pyfiglet` inside the venv
5. Launches `nerv.py` automatically

---

## Requirements

- Python 3.8+
- Terminal with truecolor support:
  - ✅ Kitty, Alacritty, WezTerm, Windows Terminal, iTerm2
  - ✅ WSL (Windows Terminal recommended)
  - ⚠️ Old `cmd.exe` — limited color

---

## Controls

### Screen 1 — NERV Splash
| Key | Action |
|-----|--------|
| `SPACE` | Enter Pilot Interface |
| `ESC` | Exit |

### Screen 2 — Pilot Interface
| Key | Action |
|-----|--------|
| `A` | Activate EVA Unit |
| `S` | Sync Uplink |
| `D` | Tactical Display |
| `M` | MAGI Query |
| `Q` / `ESC` | Exit |

---

## Features

**Screen 1 — NERV Splash**
- Full-screen hex scanline noise background
- Giant ASCII `NERV` logo (`pyfiglet` banner3 font)
- Classification text: `MAGI SYSTEM v3.0 | TOKYO-3 TACTICAL NETWORK`
- Blinking amber `[ PRESS SPACE TO INITIALIZE PILOT INTERFACE ]` prompt

**Screen 2 — Pilot Interface**
- Left panel: EVA-01 silhouette + sync ratio bar
- Right panel: Animated Shinji head (blink / tilt / look-right at 180ms)
- Center panel: Pilot data table + command menu
- Bottom ticker: Live MAGI status + session timer

---

## Dependencies

| Library | Purpose |
|---------|--------|
| `blessed` | Terminal UI — colors, positioning, fullscreen, keyboard |
| `pyfiglet` | ASCII art font rendering for NERV logo |

---

## License
MIT
