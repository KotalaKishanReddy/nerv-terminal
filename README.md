# NERV Terminal

> *"God's in His heaven. All's right with the world."*

A Neon Genesis Evangelion themed TUI that runs entirely in your terminal.  
Inspired by the MAGI supercomputer system — CASPAR, BALTHASAR, MELCHIOR.

---

## One-line install (Linux / macOS)

```bash
curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.sh | bash
```

Then run:
```bash
nerv
```

> Updates are **automatic** — every launch silently checks GitHub for a newer version and hot-swaps it before starting.

---

## Manual install (any OS)

```bash
git clone https://github.com/KotalaKishanReddy/nerv-terminal.git
cd nerv-terminal
pip install -r requirements.txt
python run.py          # auto-update then launch
# or directly:
python nerv.py
```

## Windows (PowerShell)

```powershell
git clone https://github.com/KotalaKishanReddy/nerv-terminal.git
cd nerv-terminal
pip install -r requirements.txt
python run.py
```

---

## What it does

| Screen | Description |
|---|---|
| **NERV Splash** | Full block-logo, braille EVA art, blinking amber prompt |
| **Password gate** | Dot-masked input; wrong → `W` bruteforce / `R` retry |
| **MAGI Bruteforce** | 10-min live bars, CASPAR/BALTHASAR/MELCHIOR votes, hex stream; **ESC locked**; rick-rolls at 10:00 |
| **P & Q entry** | RSA prime inputs → AES-CBC decrypt of `Encrypted.txt` |
| **Decrypted view** | Shows plaintext output |
| **Terms & Conditions** | YES → Instagram T&C (Chinese); NO → YouTube T&C (Japanese) |
| **YES / NO** | Both paths end with a rick-roll |

**Password:** `21SEP`

---

## Dependencies

- Python 3.8+
- `blessed` — terminal rendering
- `pycryptodome` — AES decrypt

---

## Auto-update architecture

```
nerv (launcher)
  └─ run.py
       ├─ nerv_terminal/updater.py  ← polls GitHub API (max 1×/hour)
       │       └─ if new SHA → downloads nerv.py → hot-swaps it
       └─ os.execv → nerv.py        ← always runs latest
```

No background daemons. No cron jobs. Pure Python stdlib network call.

---

## License

MIT
