#!/usr/bin/env python3
"""
NERV Terminal  —  Neon Genesis Evangelion themed TUI
Dependencies: blessed, pycryptodome
"""
import sys, time, random, threading, subprocess, struct, hashlib
from pathlib import Path
from blessed import Terminal

term = Terminal()

# ─────────────────────────────────────────────────────────────────────────────
R  = lambda s: term.color_rgb(210, 20,  20)  + s + term.normal
DR = lambda s: term.color_rgb(100, 0,   0)   + s + term.normal
AM = lambda s: term.color_rgb(255, 170, 0)   + s + term.normal
OR = lambda s: term.color_rgb(255, 100, 10)  + s + term.normal
MU = lambda s: term.color_rgb(130, 110, 95)  + s + term.normal
WH = lambda s: term.color_rgb(220, 210, 190) + s + term.normal
DI = lambda s: term.color_rgb(60,  50,  45)  + s + term.normal
GN = lambda s: term.color_rgb(0,   200, 80)  + s + term.normal
BR = lambda s: term.color_rgb(255, 55,  55)  + s + term.normal
CY = lambda s: term.color_rgb(0,   190, 210) + s + term.normal
YL = lambda s: term.color_rgb(235, 225, 45)  + s + term.normal
BG_ON = term.on_color_rgb(10, 0, 0)

# ─────────────────────────────────────────────────────────────────────────────
ACCESS_CODE   = '21SEP'
BRUTE_SECONDS = 600
RICK_BASH     = 'curl -s -L https://raw.githubusercontent.com/keroserene/rickrollrc/master/roll.sh | bash'
RICK_URL_WIN  = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
ENC_FILE      = 'Encrypted.txt'
MAGIC         = b'\x89TLOCK02'
BUF_MAX       = 256

# ─────────────────────────────────────────────────────────────────────────────
LOGO = [
    '███╗   ██╗███████╗██████╗ ██╗   ██╗',
    '████╗  ██║██╔════╝██╔══██╗██║   ██║',
    '██╔██╗ ██║█████╗  ██████╔╝██║   ██║',
    '██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝',
    '██║ ╚████║███████╗██║  ██║ ╚████╔╝ ',
    '╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ',
]

# Exact braille art — 36 rows, used as tiling background
BIG_ART = [
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀0⠀0⠀0⡄⡄0⡄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀0⡄⡄0⡄⣼⣿⣿⢟⢿⣿⣿⣿⣫⡄⡄0⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⢟⣿⣿⢟⢛⣛⢿⣿⡋⢿⢿⣿⣿⣿⣿⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⣤⢿⢞⢷⣫⢛⢮⢮⢟⢯⢷⡖⢽⢿⣾⠷⢿⣬⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡣⣿⢞⣿⠷⣣⢛⠬⢧⣕⢑⢟⢷⡖⢿⣾⣿⢟⣿⢶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠜⣿⠏⠷⣣⢛⠬⢧⣕⢑⢟⢷⠍⢿⣿⢟⣿⢾⢶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢟⢟⡪⢿⣯⢤⢾⢤⢟⣐⢟⢎⢺⢛⢾⡪⢿⣿⣛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠈⠊⢠⣛⢞⣿⣿⣣⣡⣻⢟⢴⢟⣾⣥⢡⣿⣿⠘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠎⢟⣿⣿⣿⣫⢟⠁⣖⡝⢟⢺⣣⣯⢟⣋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠈⣣⣛⣖⢯⢾⣫⣿⣗⣨⣠⠃⠉⠐⠜⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠡⡽⠋⢟⠐⢛⠃⠉⠀⠙⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣤⢾⣿⣿⣷⣶⣤⡲⣶⣶⣶⠰⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⣿⣿⢟⠉⣻⣿⣿⢯⣻⣻⣿⣿⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢼⣿⣿⣿⢧⣢⢼⣿⢩⢷⢞⢯⣿⣿⣿⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣿⣿⣿⢟⢼⣿⠇⣿⣿⣿⣿⣿⢟⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣬⢿⣿⣿⣿⢟⠋⠁⠈⢛⣨⣿⣿⣿⣽⣿⢟⢩⣤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢾⣿⢟⣻⠰⢟⢿⣷⠀⠀⠀⢠⢟⢷⣿⣢⠂⣭⢛⢼⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⢟⣻⠐⢟⢿⣷⠀⠀⠀⢾⡰⢿⣿⠁⣿⠇⣿⢟⢿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⢟⣿⣿⠆⡆⢞⣿⢟⠀⠀⠀⢟⢾⣿⢟⣨⢟⢟⠀⢠⢞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⣩⣿⢛⠣⣣⣽⣿⠁⠀⠀⢼⣿⣿⣿⠷⣿⠃⢟⠁⠘⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⢛⢃⠣⣽⣿⠀⠀⠀⢼⣿⣿⣿⠷⣿⠃⢟⠁⠀⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⢷⣶⣿⢟⠀⠀⠀⢟⢞⢟⢟⣷⢟⢟⠀⢠⢟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⢟⣿⣿⢟⢟⣿⠀⠀⠀⢟⣻⢟⢟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⠀⠀⠀⠀⢿⣹⢟⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⣿⣿⣿⣿⣿⠀⠀⠀⠀⢾⠄⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⣿⢞⣿⣿⣯⢷⠀⠀⠀⢼⣿⣣⠀⠀⠀⠀⠀⣐⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢾⢞⢿⣿⣿⣿⢷⠀⠁⠀⣿⣿⣯⢞⢷⣤⢠⠀⠀⠀⢾⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣨⣿⢞⢿⣿⣿⣿⢧⠀⠰⠀⣿⣿⣿⣿⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⢾⣿⣿⣿⢶⠀⢼⣿⣿⣿⣿⣶⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⢟⣷⠀⢼⣿⣿⣿⣿⢟⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⢟⢛⢟⡰⢛⣿⣿⣿⢷⡹⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⢟⢛⣛⢿⢰⢛⣿⢾⣹⣿⣣⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢟⢛⢟⢳⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
    '⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⢟⠋⠋⡣⣠⣥⣿⣿⣿⣻⢟⢷⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀',
]

# ─────────────────────────────────────────────────────────────────────────────
def put(row, col, text):
    if row < 0 or col < 0: return
    sys.stdout.write(term.move(row, col) + text)
    sys.stdout.flush()

def fill(h, w):
    line = BG_ON + ' ' * w + term.normal
    for r in range(h):
        sys.stdout.write(term.move(r, 0) + line)
    sys.stdout.flush()

def ctr(text, width): return max(0, (width - len(text)) // 2)
def hbar(w): return '━' * w
def box_t(w): return '┌' + '─'*(w-2) + '┐'
def box_b(w): return '└' + '─'*(w-2) + '┘'
def box_s(w): return '├' + '─'*(w-2) + '┤'

def clear_buf():
    while term.inkey(timeout=0): pass

def wrap(text, w):
    words = text.split(); lines, cur = [], ''
    for word in words:
        t = word if not cur else f'{cur} {word}'
        if len(t) <= w: cur = t
        else: lines.append(cur); cur = word
    if cur: lines.append(cur)
    return lines or ['']

def is_sp(k):  return not k.is_sequence and str(k) == ' '
def is_esc(k): return k.is_sequence and k.name == 'KEY_ESCAPE'
def is_ret(k): return (k.is_sequence and k.name == 'KEY_ENTER') or str(k) in ('\n','\r')
def is_bs(k):  return (k.is_sequence and k.name in ('KEY_BACKSPACE','KEY_DELETE')) or str(k) in ('\x7f','\b')
def is_up(k):  return k.is_sequence and k.name in ('KEY_UP',   'KEY_LEFT')
def is_dn(k):  return k.is_sequence and k.name in ('KEY_DOWN', 'KEY_RIGHT')
def is_tab(k): return not k.is_sequence and str(k) == '\t'
def kch(k):    return str(k) if not k.is_sequence and len(str(k))==1 else None

def rick_open():
    import platform
    sys.stdout.write(term.clear + term.normal)
    sys.stdout.flush()
    if platform.system() == 'Windows':
        subprocess.run(['powershell','-Command',f'Start-Process "{RICK_URL_WIN}"'], check=False)
        return
    try:
        subprocess.run(['bash','-c', RICK_BASH], check=False)
    except FileNotFoundError:
        subprocess.run(['sh','-c',
            f'xdg-open "{RICK_URL_WIN}" 2>/dev/null || open "{RICK_URL_WIN}" 2>/dev/null || true'],
            check=False)

# ─────────────────────────────────────────────────────────────────────────────
def _draw_art_bg(H, W):
    """Draw BIG_ART once centred on screen; fill remaining with dark bg."""
    art_h = len(BIG_ART)
    art_w = max(len(r) for r in BIG_ART)
    # fill background first
    for r in range(H):
        sys.stdout.write(term.move(r, 0) + BG_ON + ' ' * W + term.normal)
    # draw art centred
    start_r = max(0, (H - art_h) // 2)
    start_c = max(0, (W - art_w) // 2)
    for i, row in enumerate(BIG_ART):
        r = start_r + i
        if r >= H: break
        put(r, start_c, DR(row))
    sys.stdout.flush()

def splash():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        _draw_art_bg(H, W)
        pw = min(W-4, 48); px = (W-pw)//2
        py = max(1, (H-22)//2)
        put(py, px, R('▀'*pw))
        hdr = 'NERV HEADQUARTERS'
        put(py+1, px+ctr(hdr,pw), MU(hdr))
        ly = py+3; lx2 = px+ctr(LOGO[0],pw)
        for i,ln in enumerate(LOGO): put(ly+i, lx2, R(ln))
        div_y = ly+len(LOGO)+1
        div = hbar(min(pw-4, 36))
        put(div_y, px+ctr(div,pw), DR(div))
        labels = [('GEHIRN ADVANCED RESEARCH',AM),('MAGI SYSTEM  v3.0',MU),('CLASSIFICATION  TOP SECRET',MU)]
        for i,(txt,col) in enumerate(labels): put(div_y+2+i, px+ctr(txt,pw), col(txt))
        sub = 'ネルフ  第3新東京市  GEO-FRONT SUBLEVEL 7'
        put(div_y+2+len(labels)+1, px+ctr(sub,pw), DI(sub))
        bot_y = div_y+2+len(labels)+2
        put(bot_y, px, R('▄'*pw))
        prom_y = bot_y-2
        prompt = '[ PRESS SPACE TO INITIALIZE ]'
        prom_x = px+ctr(prompt,pw)
        stop = threading.Event()
        def blink():
            v = True
            while not stop.is_set():
                put(prom_y, prom_x, AM(prompt) if v else DR(' '*len(prompt)))
                v = not v; stop.wait(0.55)
        t = threading.Thread(target=blink, daemon=True); t.start()
        while True:
            k = term.inkey(timeout=0.05)
            if not k: continue
            if is_sp(k): stop.set(); t.join(0.8); clear_buf(); return
            if is_esc(k): stop.set(); sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
def password_gate():
    typed = []
    def _draw_frame(bx, by, bw):
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('│')+WH('  Enter access code:'.ljust(bw-2))+R('│'))
        put(by+4, bx, R(box_s(bw)))
        put(by+5, bx, R('│')+' '*(bw-2)+R('│'))
        put(by+6, bx, R(box_s(bw)))
        put(by+7, bx, R('│')+' '*(bw-2)+R('│'))
        put(by+8, bx, R(box_s(bw)))
        put(by+9, bx, R('│')+MU('  ENTER ─ confirm   BKSP ─ erase   ESC ─ quit'.ljust(bw-2))+R('│'))
        put(by+10,bx, R(box_s(bw)))
        put(by+11,bx, R(box_b(bw)))
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw = min(W,62); bh = 12
        bx = (W-bw)//2;  by = max(2,(H-bh)//2)
        _draw_frame(bx, by, bw)
        def field():
            dots = '  '.join('●' for _ in typed) if typed else '·  ·  ·  ·  ·'
            put(by+5, bx, R('│')+AM(f'  CODE  {dots}'[:bw-2].ljust(bw-2))+R('│'))
        def msgrow(txt='', col=BR):
            content = f'  {txt}' if txt else ''
            put(by+7, bx, R('│')+(col(content[:bw-2].ljust(bw-2)) if content else ' '*(bw-2))+R('│'))
        field(); msgrow()
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    msgrow('ACCESS GRANTED', GN); time.sleep(0.8); return
                msgrow('ACCESS DENIED  —  W: brute-force   R: retry', BR)
                time.sleep(0.6); typed.clear(); field()
                while True:
                    k2 = term.inkey(timeout=0.2)
                    if not k2: continue
                    c2 = kch(k2)
                    if c2 and c2.lower() == 'w': brute_force(); return
                    if c2 and c2.lower() == 'r':
                        fill(H, W); _draw_frame(bx,by,bw); field(); msgrow(); break
                    if is_esc(k2): sys.exit(0)
                continue
            if is_bs(k):
                if typed: typed.pop(); field()
                continue
            c = kch(k)
            if c and c.isalnum() and len(typed) < 5:
                typed.append(c.upper()); field()

# ─────────────────────────────────────────────────────────────────────────────
PHASES = [
    ('CASPAR    ─ INITIALISING',       0.00, 0.15),
    ('CASPAR    ─ DICTIONARY LAYER I', 0.15, 0.28),
    ('BALTHASAR ─ HASH EXPANSION',     0.28, 0.42),
    ('BALTHASAR ─ ENTROPY ANALYSIS',   0.42, 0.55),
    ('MELCHIOR  ─ NEURAL MATCH',       0.55, 0.68),
    ('MELCHIOR  ─ DEEP CIPHER',        0.68, 0.80),
    ('MAGI CORE ─ COLLATION',          0.80, 0.92),
    ('MAGI CORE ─ UNLOCKING…',    0.92, 1.00),
]
HEX = '0123456789ABCDEF'
def rnd_hex(w): return ' '.join(''.join(random.choices(HEX,k=4)) for _ in range(max(1,w//5)))
def pbar(p, w, cf=GN, ce=DI): f=int(w*p); return cf('█'*f)+ce('░'*max(0,w-f))

def _vstatus(pct, thrs, lbs):
    col = BR if pct < thrs[0] else AM if pct < thrs[1] else GN
    lbl = lbs[0] if pct < thrs[0] else lbs[1] if pct < thrs[1] else lbs[2]
    return col, lbl

MAGI_VOTES = [
    ('CASPAR   ', (0.33,0.50), ('ANALYZING  ','PATTERN FOUND','APPROVED')),
    ('BALTHASAR', (0.50,0.75), ('COMPUTING  ','CONVERGING   ','APPROVED')),
    ('MELCHIOR ', (0.72,0.95), ('DEEP SCAN  ','KEY MATCH    ','APPROVED')),
]

def brute_force():
    T = BRUTE_SECONDS; t0 = time.time()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw = min(W,70); bx=(W-bw)//2; by=1; bw2=bw-14
        needed = by+27
        if H < needed: by = max(0, H-27)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+BR('  MAGI ─ MANUAL DECRYPTION ENGAGED'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('│')+MU('  Authentication failed. Running brute-force recovery.'.ljust(bw-2))+R('│'))
        put(by+4, bx, R(box_s(bw)))
        put(by+7, bx, R(box_s(bw)))
        put(by+10,bx, R(box_s(bw)))
        put(by+17,bx, R(box_s(bw)))
        put(by+21,bx, R(box_s(bw)))
        put(by+24,bx, R(box_s(bw)))
        put(by+25,bx, R('│')+MU('  No way in without password  —  ESC locked during bruteforce'.ljust(bw-2))+R('│'))
        put(by+26,bx, R(box_b(bw)))
        hbuf = [''] * 6; last = -1
        while True:
            term.inkey(timeout=0)
            now=time.time(); el=min(now-t0,T); pct=el/T; rem=max(0,T-el)
            sec=int(el)
            if sec == last: time.sleep(0.12); continue
            last=sec; mm,ss=divmod(int(rem),60)
            put(by+5, bx, R('│')+MU('  OVERALL  ')+pbar(pct,bw2,AM,DI)+MU('  ')+R('│'))
            put(by+6, bx, R('│')+AM(f'  {pct*100:5.1f}%  ─  ETA {mm:02d}:{ss:02d}'.ljust(bw-2))+R('│'))
            pl,pp = PHASES[-1][0], 1.0
            for lb,p0,p1 in PHASES:
                if pct <= p1:
                    pl=lb; pp=max(0.,min(1.,(pct-p0)/max(1e-4,p1-p0))); break
            put(by+8, bx, R('│')+CY(f'  {pl}'[:bw-2].ljust(bw-2))+R('│'))
            put(by+9, bx, R('│')+MU('  PHASE    ')+pbar(pp,bw2,CY,DI)+MU('  ')+R('│'))
            hbuf = hbuf[1:] + [rnd_hex(bw-6)]
            for i,ln in enumerate(hbuf):
                put(by+11+i, bx, R('│')+(DI if i<4 else MU)(f'  {ln}'[:bw-2].ljust(bw-2))+R('│'))
            for i,(nm,thrs,lbs) in enumerate(MAGI_VOTES):
                col,lbl = _vstatus(pct, thrs, lbs)
                put(by+18+i, bx, R('│')+col(f'  {nm}  ──  {lbl}'[:bw-2].ljust(bw-2))+R('│'))
            tk = '▊' if sec%2==0 else '▉'
            put(by+22, bx, R('│')+YL(f'  {tk}  REMAINING  {mm:02d} min  {ss:02d} sec'.ljust(bw-2))+R('│'))
            tck=['SCANNING KEY SPACE…','TESTING PERMUTATIONS…','CROSS-REFERENCING DB…','MAGI CONSENSUS…','DECRYPTION ACTIVE…']
            put(by+23, bx, R('│')+MU(f'  {tck[sec%len(tck)]}'[:bw-2].ljust(bw-2))+R('│'))
            if pct >= 1.0:
                put(by+22, bx, R('│')+GN('  RICK ROLLING YOU NOW  —  NO WAY IN WITHOUT PASSWORD'.ljust(bw-2))+R('│'))
                time.sleep(1.0); rick_open(); time.sleep(2.0); return

# ─────────────────────────────────────────────────────────────────────────────
def pq_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,80); bh=14; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  ENTER P AND Q VALUES'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('│')+WH('  Paste both values separated by whitespace, or as p=.. q=..'.ljust(bw-2))+R('│'))
        put(by+4, bx, R('│')+WH('  These will be used to decrypt Encrypted.txt'.ljust(bw-2))+R('│'))
        put(by+5, bx, R(box_s(bw)))
        for r in range(6,11): put(by+r, bx, R('│')+' '*(bw-2)+R('│'))
        put(by+11,bx, R(box_s(bw)))
        put(by+12,bx, R('│')+MU('  ENTER to submit    ESC to quit'.ljust(bw-2))+R('│'))
        put(by+13,bx, R(box_b(bw)))
        buf = []
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_bs(k):
                if buf: buf.pop()
                put(by+6, bx, R('│')+WH(('  '+''.join(buf))[-(bw-2):].ljust(bw-2))+R('│'))
                continue
            if is_ret(k):
                raw = ''.join(buf).strip()
                if 'p=' in raw and 'q=' in raw:
                    p = raw.split('p=',1)[1].split()[0].strip(',;')
                    q = raw.split('q=',1)[1].split()[0].strip(',;')
                else:
                    parts = raw.split(); p,q = (parts+['',''])[:2]
                if p and q:
                    put(by+8, bx, R('│')+GN('  Running decryption…'.ljust(bw-2))+R('│'))
                    time.sleep(0.5); return p, q
                put(by+8, bx, R('│')+BR('  Could not parse p and q. Try again.'.ljust(bw-2))+R('│'))
                continue
            c = kch(k)
            if c and len(buf) < BUF_MAX:
                buf.append(c)
                put(by+6, bx, R('│')+WH(('  '+''.join(buf))[-(bw-2):].ljust(bw-2))+R('│'))

def decrypt_file(p_str, q_str):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        p = int(p_str, 16) if p_str.startswith(('0x','0X')) else int(p_str)
        q = int(q_str, 16) if q_str.startswith(('0x','0X')) else int(q_str)
        data = Path(ENC_FILE).read_bytes()
        if not data.startswith(MAGIC):
            return Path(ENC_FILE).read_text(errors='ignore')[:1600]
        off = len(MAGIC)
        flags = data[off]; off += 1
        if flags & 0x01:
            off += 32
            hint_len = struct.unpack_from('H', data, off)[0]; off += 2
            off += hint_len
        T = struct.unpack_from('Q', data, off)[0]; off += 8
        nb_len = struct.unpack_from('H', data, off)[0]; off += 2
        n_stored = int.from_bytes(data[off:off+nb_len],'big'); off += nb_len
        iv = data[off:off+16]; off += 16
        ct_len = struct.unpack_from('I', data, off)[0]; off += 4
        ct = data[off:off+ct_len]
        phi = (p-1)*(q-1)
        key_int = pow(2, pow(2,T,phi), n_stored)
        key_bytes = key_int.to_bytes((n_stored.bit_length()+7)//8,'big')
        k = hashlib.sha256(key_bytes).digest()
        pt = unpad(AES.new(k, AES.MODE_CBC, iv).decrypt(ct), 16)
        return pt.decode('utf-8','ignore')
    except Exception as e:
        try: return Path(ENC_FILE).read_text(errors='ignore')[:1600]
        except: return f'(could not open {ENC_FILE}: {e})'

def show_decrypted(text):
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,80); iw=bw-6
        lines=wrap(text,iw); vis=min(len(lines),max(4,H-10))
        lines=lines[:vis]; bh=vis+7
        bx=max(0,(W-bw)//2); by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  DECRYPTION COMPLETE — MAGI OUTPUT'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        for i,ln in enumerate(lines):
            put(by+3+i, bx, R('│')+'  '+WH(ln[:iw].ljust(iw))+'  '+R('│'))
        fr = by+3+vis
        put(fr,   bx, R(box_s(bw)))
        put(fr+1, bx, R('│')+MU('  Decryption successful. Proceed?'.ljust(bw-2))+R('│'))
        put(fr+2, bx, R('│')+AM('  ENTER ─ next   ESC ─ abort'.ljust(bw-2))+R('│'))
        put(fr+3, bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k): return

# ─────────────────────────────────────────────────────────────────────────────
def terms_screen():
    sel = 0  # 0=YES 1=NO
    def _draw(bx, by, bw):
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  NERV TERMS & CONDITIONS'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('│')+WH('  Do you accept the following terms?'.ljust(bw-2))+R('│'))
        put(by+4, bx, R(box_s(bw)))
        yes_txt = '⮚  YES  —  已阅读并同意 Instagram 服务条款'
        no_txt  = '⮚  NO   —  YouTube サービス利用規約'
        hl = lambda s: term.color_rgb(255,220,0)+term.bold+s+term.normal
        yes_col = hl if sel==0 else MU
        no_col  = hl if sel==1 else MU
        yes_pfx = '▶ ' if sel==0 else '  '
        no_pfx  = '▶ ' if sel==1 else '  '
        put(by+5, bx, R('│')+yes_col(f'  {yes_pfx}{yes_txt}'[:bw-2].ljust(bw-2))+R('│'))
        put(by+6, bx, R('│')+no_col( f'  {no_pfx}{no_txt}' [:bw-2].ljust(bw-2))+R('│'))
        put(by+7, bx, R(box_s(bw)))
        put(by+8, bx, R('│')+DI('  ↑↓ / Tab ─ move   ENTER ─ confirm   Y/N ─ jump   ESC ─ quit'.ljust(bw-2))+R('│'))
        put(by+9, bx, R(box_b(bw)))
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        _draw_art_bg(H, W)
        bw = min(W, 76); bh = 10
        bx = (W-bw)//2; by = max(1,(H-bh)//2)
        _draw(bx, by, bw)
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_up(k) or is_dn(k) or is_tab(k):
                sel = 1 - sel; _draw(bx, by, bw)
            elif is_ret(k):
                return sel == 0
            else:
                c = kch(k)
                if c and c.lower() == 'y': sel = 0; _draw(bx, by, bw)
                elif c and c.lower() == 'n': sel = 1; _draw(bx, by, bw)

# ─────────────────────────────────────────────────────────────────────────────
def yes_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        _draw_art_bg(H, W)
        bw=min(W,80); bh=12; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+BR('  YAYYYYYYYYYY'.ljust(bw-2))+R('│'))
        put(by+2, bx, R('│')+BR('  you got a secret message !!!!'.ljust(bw-2))+R('│'))
        put(by+3, bx, R(box_s(bw)))
        put(by+4, bx, R('│')+AM('  ネルフ機密文書 ─ TOP SECRET ─ FINAL INTEL'.ljust(bw-2))+R('│'))
        put(by+5, bx, R('│')+WH('  press ENTER to reveal the secret message'.ljust(bw-2))+R('│'))
        put(by+6, bx, R(box_s(bw)))
        put(by+7, bx, R('│')+MU('  SHINJI  ASUKA  REI  —  all waiting for you to know'.ljust(bw-2))+R('│'))
        put(by+8, bx, R('│')+MU('  do not be afraid  —  this is definitely not a rick-roll'.ljust(bw-2))+R('│'))
        put(by+9, bx, R(box_s(bw)))
        put(by+10,bx, R('│')+DI('  [ ENTER to proceed ]   [ ESC to cowardly flee ]'.ljust(bw-2))+R('│'))
        put(by+11,bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k): rick_open(); return

def no_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        _draw_art_bg(H, W)
        bw=min(W,80); bh=10; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,  bx, R(box_t(bw)))
        put(by+1,bx, R('│')+BR('  REFUSED  —  MAGI OVERRIDE ACTIVATED'.ljust(bw-2))+R('│'))
        put(by+2,bx, R(box_s(bw)))
        put(by+3,bx, R('│')+MU('  You refused. NERV does not accept refusal.'.ljust(bw-2))+R('│'))
        put(by+4,bx, R('│')+MU('  Redirecting to mandatory training material.'.ljust(bw-2))+R('│'))
        put(by+5,bx, R(box_s(bw)))
        put(by+6,bx, R('│')+AM('  Deploying classified footage directly to terminal…'.ljust(bw-2))+R('│'))
        put(by+7,bx, R('│')+DI('  (there is no escape)'.ljust(bw-2))+R('│'))
        put(by+8,bx, R(box_s(bw)))
        put(by+9,bx, R(box_b(bw)))
        time.sleep(1.5)
        rick_open()

# ─────────────────────────────────────────────────────────────────────────────
def main():
    try:
        splash()
        password_gate()
        p, q = pq_screen()
        text = decrypt_file(p, q)
        show_decrypted(text)
        accepted = terms_screen()
        if accepted: yes_screen()
        else: no_screen()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        sys.stdout.write(term.clear + term.normal)
        sys.stdout.write(R('\n  [ NERV ]  Session terminated. Rei is disappointed.\n\n'))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
