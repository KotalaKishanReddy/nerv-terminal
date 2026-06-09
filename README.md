# 🔴 NERV Terminal

**Neon Genesis Evangelion themed terminal launcher**

```
███████████████████████████████████████████
█  NERV // GEHIRN ADVANCED RESEARCH        █
█  MAGI SYSTEM v3.0 | TOKYO-3 NETWORK      █
███████████████████████████████████████████
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch
python nerv.py
```

Or one-shot:
```bash
chmod +x setup.sh && ./setup.sh
```

## Requirements

- Python 3.8+
- Terminal with 256-color / truecolor support:
  - ✅ Kitty, Alacritty, WezTerm, iTerm2, Windows Terminal
  - ✅ WSL (Windows Terminal recommended)
  - ⚠️ Old `cmd.exe` — limited color support

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

## Features

**Screen 1 — NERV Splash**
- Full-screen hex scanline noise background
- ASCII NERV logo via `pyfiglet` (`banner3` font)
- Classification block: `MAGI SYSTEM v3.0 | TOKYO-3 TACTICAL NETWORK`
- Blinking amber `[ PRESS SPACE TO INITIALIZE PILOT INTERFACE ]` prompt

**Screen 2 — Pilot Interface**
- Left panel: EVA-01 silhouette + sync ratio progress bar
- Right panel: Animated Shinji head (blink / tilt / look-right frames at 180ms)
- Center panel: Pilot data table + command menu (`A/S/D/M/Q`)
- Bottom ticker: Live MAGI status + session timer

## Dependencies

| Library | Purpose |
|---------|--------|
| `blessed` | Terminal UI — colors, positioning, keyboard input, fullscreen |
| `pyfiglet` | ASCII art font rendering for the NERV logo |

## Extending

To wire up the menu actions, open `nerv.py` and find the key handler in `draw_pilot_interface()`:

```python
elif str(key).lower() in ('a', 's', 'd', 'm'):
    msg = { ... }
```

Replace the placeholder strings with calls to your own functions — more screens coming soon!

## License
MIT
