# NERV Terminal

> *"God's in His heaven. All's right with the world."*

A Neon Genesis Evangelion themed TUI that runs entirely in your terminal.  
Inspired by the MAGI supercomputer — CASPAR, BALTHASAR, MELCHIOR.

---

## ⚡ Install

### Linux / macOS
```bash
curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.sh | bash
```
Then run:
```bash
nerv
```

---

### Windows — PowerShell
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
irm https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.ps1 | iex
```
Then run (after restarting terminal):
```
nerv
```

---

### Windows — CMD (no PowerShell)
```cmd
curl -fsSL https://raw.githubusercontent.com/KotalaKishanReddy/nerv-terminal/main/install.ps1 -o install.ps1
powershell -ExecutionPolicy Bypass -File install.ps1
```

---

### Manual (any OS)
```bash
git clone https://github.com/KotalaKishanReddy/nerv-terminal.git
cd nerv-terminal
pip install -r requirements.txt
python run.py
```

---

### pip (any OS)
```bash
pip install git+https://github.com/KotalaKishanReddy/nerv-terminal.git
nerv
```

---

> **Updates are automatic** — every launch silently checks GitHub for a newer version and hot-swaps before starting. No cron, no daemons.

---

## Screens

| Screen | Description |
|---|---|
| **NERV Splash** | Block logo, braille EVA art, blinking amber prompt |
| **Password gate** | Dot-masked input — password: `21SEP` |
| **MAGI Bruteforce** | 10-min bars, CASPAR/BALTHASAR/MELCHIOR votes, hex stream; **ESC locked**; rick-rolls at 10:00 |
| **P & Q entry** | RSA prime inputs → AES-CBC decrypt of `Encrypted.txt` |
| **Decrypted view** | Shows plaintext |
| **Terms & Conditions** | YES → Instagram T&C in Chinese; NO → YouTube T&C in Japanese |
| **YES / NO** | Both paths end in a rick-roll |

---

## Auto-update architecture

```
nerv  (launcher)
  └─ run.py
       ├─ nerv_terminal/updater.py  ← polls GitHub API (max 1×/hr)
       │       └─ new SHA? → downloads nerv.py → hot-swaps
       └─ os.execv → nerv.py
```

---

## Dependencies

- Python 3.8+
- `blessed` — terminal rendering
- `pycryptodome` — AES decrypt

---

## License

MIT
