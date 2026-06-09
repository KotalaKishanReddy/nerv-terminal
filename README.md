# 🔴 NERV Terminal Interface

> *"God's in his heaven, all's right with the world."*

A Neon Genesis Evangelion themed TUI launcher built with Python + `blessed`.
Braille ASCII art sourced from [emojicombos.com/evangelion-ascii-art](https://emojicombos.com/evangelion-ascii-art).

[![CI](https://github.com/KotalaKishanReddy/nerv-terminal/actions/workflows/ci.yml/badge.svg)](https://github.com/KotalaKishanReddy/nerv-terminal/actions)
[![PyPI](https://img.shields.io/pypi/v/nerv-terminal)](https://pypi.org/project/nerv-terminal/)

## Install

```bash
pip install nerv-terminal
nerv
```

Or run from source:

```bash
git clone https://github.com/KotalaKishanReddy/nerv-terminal
cd nerv-terminal
pip install -e .
nerv
```

## Controls

| Key | Action |
|-----|--------|
| `SPACE` | Splash → Pilot Interface |
| `Q` / `ESC` | Quit |

## Requirements

- Python 3.8+
- Truecolor terminal: Kitty · Alacritty · WezTerm · Windows Terminal (WSL)

## Release to PyPI

```bash
git tag v1.0.0
git push origin v1.0.0
```

Set up PyPI Trusted Publisher at https://pypi.org/manage/account/publishing/

## License

MIT
