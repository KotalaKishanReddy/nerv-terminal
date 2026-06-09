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
BUF_MAX       = 256  # FIX #5: cap input buffers

# ─────────────────────────────────────────────────────────────────────────────
LOGO = [
    '\u2588\u2588\u2588\u2557   \u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2588\u2588\u2588\u2588\u2557 \u2588\u2588\u2557   \u2588\u2588\u2557',
    '\u2588\u2588\u2588\u2588\u2557  \u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u2550\u2550\u255d\u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u2588\u2588\u2551   \u2588\u2588\u2551',
    '\u2588\u2588\u2554\u2588\u2588\u2557 \u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2557  \u2588\u2588\u2588\u2588\u2588\u2588\u2554\u255d\u2588\u2588\u2551   \u2588\u2588\u2551',
    '\u2588\u2588\u2551\u255a\u2588\u2588\u2557\u2588\u2588\u2551\u2588\u2588\u2554\u2550\u2550\u255d  \u2588\u2588\u2554\u2550\u2550\u2588\u2588\u2557\u255a\u2588\u2588\u2557 \u2588\u2588\u2554\u255d',
    '\u2588\u2588\u2551 \u255a\u2588\u2588\u2588\u2588\u2551\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2557\u2588\u2588\u2551  \u2588\u2588\u2551 \u255a\u2588\u2588\u2588\u2588\u2554\u255d ',
    '\u255a\u2550\u255d  \u255a\u2550\u2550\u2550\u255d\u255a\u2550\u2550\u2550\u2550\u2550\u2550\u255d\u255a\u2550\u255d  \u255a\u2550\u255d  \u255a\u2550\u2550\u2550\u255d  ',
]

LEFT_ART = (
    '\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28ff\u2847\u28b7\u28ae\u2861\u283b\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u2861\u28bb\u28ff\u28ff\n'
    '\u28ff\u287f\u2823\u280b\u28a0\u287f\u28fb\u287f\u28cb\u28b5\u28be\u28ff\u283f\u28a1\u287e\u28f9\u287f\u28a3\u28a4\u28ff\u28b7\u28a4\u2861\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u28a4\u2808\u283b\u283f\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u28bd\u28b7\u285d\u28bf\u28ff\u28ff\n'
    '\u28ff\u2801\u28a0\u28be\u28af\u28be\u28ff\u28ff\u283f\u28b5\u28ff\u28ab\u28be\u28ff\u28a3\u28ff\u28ff\u287f\u28ff\u287f\u28ff\u28ff\u28ff\u28ae\u283b\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u285d\u283f\u28b7\u28a4\u2800\u2808\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28bf\u28b7\u28bd\u28bf\n'
    '\u2803\u28bc\u28ff\u28ff\u28ff\u28ff\u283f\u2861\u283f\u28fb\u280d\u287d\u280b\u2807\u28ff\u28ff\u283f\u2818\u28ff\u28a7\u2818\u28ff\u28ff\u28ff\u28b7\u2861\u28ff\u28ff\u28ff\u28ff\u2807\u28ff\u28b7\u28b6\u287f\u283f\u2832\u2834\u2861\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28bf\u28ff\u28a7\u2861\n'
    '\u28be\u28ff\u28ff\u28ff\u287f\u280b\u28a4\u28a7\u2818\u287f\u2801\u28a4\u28ff\u2818\u28ff\u287f\u28bc\u28ff\u28ff\u28ff\u28a4\u28bb\u28ff\u28ff\u28ff\u28b7\u28ac\u28bf\u28ff\u28ff\u28b7\u2819\u28ff\u280f\u2808\u28be\u28b7\u28ac\u2800\u28ff\u28ff\u28be\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28af\u28be\u28ff\u280b\u2801\u283e\u28a4\u28ff\u28ff\u2807\u28be\u28ff\u28a0\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28bb\u28ff\u28ff\u28a7\u283b\u28ff\u28a6\u2828\u285b\u28bf\u28b7\u28ac\u28bb\u28ff\u2806\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28ff\u28ff\u283f\u28a4\u280b\u28bc\u28bb\u28ff\u28ff\u2807\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28be\u28ff\u28ff\u28ff\u28ff\u28ff\u28a6\u28bb\u28ff\u28ff\u28b7\u2861\u28bf\u28a6\u283b\u28a6\u2861\u2801\u2819\u28ff\u2838\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28ff\u28ff\u2800\u2801\u28be\u28ff\u2818\u28ff\u28ff\u2800\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28a7\u28bb\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280f\u28bf\u28ff\u2839\u28ff\u280e\u283b\u2807\u2818\u28ff\u28a7\u28a0\u2804\u28ff\u2807\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u280c\u28ff\u283f\u28a0\u28ff\u28ff\u28ff\u2818\u28ff\u287f\u2800\u28bb\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u2807\u2818\u28ff\u2800\u28bb\u28ff\u28b7\u28a4\u2861\u283f\u28bf\u28bd\u2807\u28ff\u2807\u28ff\u28ff\u28bb\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28a4\u2830\u28bf\u28ff\u28ff\u28ff\u2808\u28ff\u2807\u2800\u2800\u28bf\u285d\u28ff\u28ff\u28bf\u28ff\u28ff\u28ff\u28ff\u2861\u28ff\u28ff\u28ff\u2818\u28ff\u2803\u2818\u287f\u28b8\u2806\u283b\u28ff\u28a7\u2819\u287f\u28b6\u28a4\u28be\u28ff\u2807\u28ff\u28ff\u28a0\u2861\u28bb'
).splitlines()

RIGHT_ART = (
    '\u28ff\u287f\u2803\u2801\u28be\u28ff\u2818\u2803\u287b\u28a4\u2800\u28fb\u280f\u283b\u28bf\u2800\u2809\u28a0\u28a4\u283a\u283f\u283b\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u2861\u283b\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u2861\u28bb\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u287f\u2823\u280b\u28a0\u287f\u28fb\u287f\u28cb\u28b5\u28be\u28ff\u283f\u28a1\u287e\u28f9\u287f\u28a3\u28a4\u28ff\u28b7\u28a4\u2861\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u28a4\u2808\u283b\u283f\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28b7\u28bd\u28b7\u285d\u28bf\u28ff\u28ff\n'
    '\u28ff\u2801\u28a0\u28be\u28af\u28be\u28ff\u28ff\u283f\u28b5\u28ff\u28ab\u28be\u28ff\u28a3\u28ff\u28ff\u287f\u28ff\u287f\u28ff\u28ff\u28ff\u28ae\u283b\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u285d\u283f\u28b7\u28a4\u2800\u2808\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28bf\u28b7\u28bd\u28bf\n'
    '\u2803\u28bc\u28ff\u28ff\u28ff\u28ff\u283f\u2861\u283f\u28fb\u280d\u287d\u280b\u2807\u28ff\u28ff\u283f\u2818\u28ff\u28a7\u2818\u28ff\u28ff\u28ff\u28b7\u2861\u28ff\u28ff\u28ff\u28ff\u2807\u28ff\u28b7\u28b6\u287f\u283f\u2832\u2834\u2861\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28bf\u28ff\u28a7\u2861\n'
    '\u28be\u28ff\u28ff\u28ff\u287f\u280b\u28a4\u28a7\u2818\u287f\u2801\u28a4\u28ff\u2818\u28ff\u287f\u28bc\u28ff\u28ff\u28ff\u28a4\u28bb\u28ff\u28ff\u28ff\u28b7\u28ac\u28bf\u28ff\u28ff\u28b7\u2819\u28ff\u280f\u2808\u28be\u28b7\u28ac\u2800\u28ff\u28ff\u28be\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28af\u28be\u28ff\u280b\u2801\u283e\u28a4\u28ff\u28ff\u2807\u28be\u28ff\u28a0\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28bb\u28ff\u28ff\u28a7\u283b\u28ff\u28a6\u2828\u285b\u28bf\u28b7\u28ac\u28bb\u28ff\u2806\u28bf\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28ff\u28ff\u283f\u28a4\u280b\u28bc\u28bb\u28ff\u28ff\u2807\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28be\u28ff\u28ff\u28ff\u28ff\u28ff\u28a6\u28bb\u28ff\u28ff\u28b7\u2861\u28bf\u28a6\u283b\u28a6\u2861\u2801\u2819\u28ff\u2838\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28ff\u28ff\u2800\u2801\u28be\u28ff\u2818\u28ff\u28ff\u2800\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28a7\u28bb\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280f\u28bf\u28ff\u2839\u28ff\u280e\u283b\u2807\u2818\u28ff\u28a7\u28a0\u2804\u28ff\u2807\u28ff\u28ff\u28ff\u28ff\u28ff\n'
    '\u28ff\u28ff\u280c\u28ff\u283f\u28a0\u28ff\u28ff\u28ff\u2818\u28ff\u287f\u2800\u28bb\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u280e\u28ff\u28ff\u28ff\u28ff\u28ff\u28ff\u2807\u2818\u28ff\u2800\u28bb\u28ff\u28b7\u28a4\u2861\u283f\u28bf\u28bd\u2807\u28ff\u2807\u28ff\u28ff\u28bb\u28ff\u28ff\n'
    '\u28ff\u28ff\u28ff\u28a4\u2830\u28bf\u28ff\u28ff\u28ff\u2808\u28ff\u2807\u2800\u2800\u28bf\u285d\u28ff\u28ff\u28bf\u28ff\u28ff\u28ff\u28ff\u2861\u28ff\u28ff\u28ff\u2818\u28ff\u2803\u2818\u287f\u28b8\u2806\u283b\u28ff\u28a7\u2819\u287f\u28b6\u28a4\u28be\u28ff\u2807\u28ff\u28ff\u28a0\u2861\u28bb'
).splitlines()

ART_W = 50

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
def hbar(w): return '\u2501' * w
def box_t(w): return '\u250c' + '\u2500'*(w-2) + '\u2510'
def box_b(w): return '\u2514' + '\u2500'*(w-2) + '\u2518'
def box_s(w): return '\u251c' + '\u2500'*(w-2) + '\u2524'

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
def splash():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        PAD = 1; GAP = 2
        if W >= 110:
            lx = PAD; rx = W - PAD - ART_W
            px = lx + ART_W + GAP; pw = rx - GAP - px
            for art, ax in ((LEFT_ART, lx),(RIGHT_ART, rx)):
                rows = art[:H-2]; sy = max(0,(H-len(rows))//2)
                for i,ln in enumerate(rows): put(sy+i, ax, R(ln[:ART_W]))
        elif W >= 70:
            rx = W - PAD - ART_W; pw = rx - GAP - PAD; px = PAD
            ra = RIGHT_ART[:H-2]; sy = max(0,(H-len(ra))//2)
            for i,ln in enumerate(ra): put(sy+i, rx, R(ln[:ART_W]))
        else:
            pw = min(W-2, 64); px = (W-pw)//2
        pw = max(42, pw); py = max(1,(H-24)//2)
        put(py, px, R('\u2580'*pw))
        hdr = 'NERV HEADQUARTERS'
        put(py+1, px+ctr(hdr,pw), MU(hdr))
        ly = py+3; lx2 = px+ctr(LOGO[0],pw)
        for i,ln in enumerate(LOGO): put(ly+i, lx2, R(ln))
        div_y = ly+len(LOGO)+1
        div = hbar(min(pw-4,36))
        put(div_y, px+ctr(div,pw), DR(div))
        labels = [('GEHIRN ADVANCED RESEARCH',AM),('MAGI SYSTEM  v3.0',MU),('CLASSIFICATION  TOP SECRET',MU)]
        for i,(txt,col) in enumerate(labels): put(div_y+2+i, px+ctr(txt,pw), col(txt))
        bot_y = div_y+2+len(labels)+2
        put(bot_y, px, R('\u2584'*pw))
        prom_y = bot_y-2
        prompt = '[ PRESS SPACE TO INITIALIZE ]'
        prom_x = px+ctr(prompt,pw)
        sub = '\u30cd\u30eb\u30d5  \u7b2c3\u65b0\u6771\u4eac\u5e02  GEO-FRONT SUBLEVEL 7'
        put(div_y+2+len(labels)+1, px+ctr(sub,pw), DI(sub))
        stop = threading.Event()
        def blink():
            v = True
            while not stop.is_set():
                put(prom_y, prom_x, AM(prompt) if v else BG_ON+' '*len(prompt)+term.normal)
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
        """FIX #4: extracted so frame can be repainted any time."""
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('\u2502')+OR('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('\u2502')+WH('  Enter access code:'.ljust(bw-2))+R('\u2502'))
        put(by+4, bx, R(box_s(bw)))
        put(by+5, bx, R('\u2502')+' '*(bw-2)+R('\u2502'))
        put(by+6, bx, R(box_s(bw)))
        put(by+7, bx, R('\u2502')+' '*(bw-2)+R('\u2502'))
        put(by+8, bx, R(box_s(bw)))
        put(by+9, bx, R('\u2502')+MU('  ENTER \u2500 confirm   BKSP \u2500 erase   ESC \u2500 quit'.ljust(bw-2))+R('\u2502'))
        put(by+10,bx, R(box_s(bw)))
        put(by+11,bx, R(box_b(bw)))
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw = min(W,62); bh = 12
        bx = (W-bw)//2;  by = max(2,(H-bh)//2)
        _draw_frame(bx, by, bw)
        def field():
            dots = '  '.join('\u25cf' for _ in typed) if typed else '\u00b7  \u00b7  \u00b7  \u00b7  \u00b7'
            put(by+5, bx, R('\u2502')+AM(f'  CODE  {dots}'[:bw-2].ljust(bw-2))+R('\u2502'))
        def msgrow(txt='', col=BR):
            content = f'  {txt}' if txt else ''
            put(by+7, bx, R('\u2502')+(col(content[:bw-2].ljust(bw-2)) if content else ' '*(bw-2))+R('\u2502'))
        field(); msgrow()
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    msgrow('ACCESS GRANTED', GN); time.sleep(0.8); return
                msgrow('ACCESS DENIED  \u2014  W: brute-force   R: retry', BR)
                time.sleep(0.6); typed.clear(); field()
                while True:  # inner W/R loop
                    k2 = term.inkey(timeout=0.2)
                    if not k2: continue
                    c2 = kch(k2)
                    if c2 and c2.lower() == 'w': brute_force(); return
                    if c2 and c2.lower() == 'r':
                        # FIX #4: repaint full frame before resuming
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
    ('CASPAR    \u2500 INITIALISING',       0.00, 0.15),
    ('CASPAR    \u2500 DICTIONARY LAYER I', 0.15, 0.28),
    ('BALTHASAR \u2500 HASH EXPANSION',     0.28, 0.42),
    ('BALTHASAR \u2500 ENTROPY ANALYSIS',   0.42, 0.55),
    ('MELCHIOR  \u2500 NEURAL MATCH',       0.55, 0.68),
    ('MELCHIOR  \u2500 DEEP CIPHER',        0.68, 0.80),
    ('MAGI CORE \u2500 COLLATION',          0.80, 0.92),
    ('MAGI CORE \u2500 UNLOCKING\u2026',    0.92, 1.00),
]
HEX = '0123456789ABCDEF'
def rnd_hex(w): return ' '.join(''.join(random.choices(HEX,k=4)) for _ in range(max(1,w//5)))
def pbar(p, w, cf=GN, ce=DI): f=int(w*p); return cf('\u2588'*f)+ce('\u2591'*max(0,w-f))

# FIX #1: vstatus defined OUTSIDE brute_force so it is not recreated on every tick
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
        # FIX #2: guard minimum height
        needed = by+27
        if H < needed: by = max(0, H-27)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('\u2502')+BR('  MAGI \u2500 MANUAL DECRYPTION ENGAGED'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('\u2502')+MU('  Authentication failed. Running brute-force recovery.'.ljust(bw-2))+R('\u2502'))
        put(by+4, bx, R(box_s(bw)))
        put(by+7, bx, R(box_s(bw)))
        put(by+10,bx, R(box_s(bw)))
        put(by+17,bx, R(box_s(bw)))
        put(by+21,bx, R(box_s(bw)))
        put(by+24,bx, R(box_s(bw)))
        put(by+25,bx, R('\u2502')+MU('  No way in without password  \u2014  ESC locked during bruteforce'.ljust(bw-2))+R('\u2502'))
        put(by+26,bx, R(box_b(bw)))
        hbuf = [''] * 6; last = -1
        while True:
            term.inkey(timeout=0)  # drain — ESC locked
            now=time.time(); el=min(now-t0,T); pct=el/T; rem=max(0,T-el)
            sec=int(el)
            if sec == last: time.sleep(0.12); continue
            last=sec; mm,ss=divmod(int(rem),60)
            put(by+5, bx, R('\u2502')+MU('  OVERALL  ')+pbar(pct,bw2,AM,DI)+MU('  ')+R('\u2502'))
            put(by+6, bx, R('\u2502')+AM(f'  {pct*100:5.1f}%  \u2500  ETA {mm:02d}:{ss:02d}'.ljust(bw-2))+R('\u2502'))
            pl,pp = PHASES[-1][0], 1.0
            for lb,p0,p1 in PHASES:
                if pct <= p1:
                    pl=lb; pp=max(0.,min(1.,(pct-p0)/max(1e-4,p1-p0))); break
            put(by+8, bx, R('\u2502')+CY(f'  {pl}'[:bw-2].ljust(bw-2))+R('\u2502'))
            put(by+9, bx, R('\u2502')+MU('  PHASE    ')+pbar(pp,bw2,CY,DI)+MU('  ')+R('\u2502'))
            hbuf = hbuf[1:] + [rnd_hex(bw-6)]
            for i,ln in enumerate(hbuf):
                put(by+11+i, bx, R('\u2502')+(DI if i<4 else MU)(f'  {ln}'[:bw-2].ljust(bw-2))+R('\u2502'))
            for i,(nm,thrs,lbs) in enumerate(MAGI_VOTES):  # FIX #1: use module-level _vstatus
                col,lbl = _vstatus(pct, thrs, lbs)
                put(by+18+i, bx, R('\u2502')+col(f'  {nm}  \u2500\u2500  {lbl}'[:bw-2].ljust(bw-2))+R('\u2502'))
            tk = '\u258a' if sec%2==0 else '\u2589'
            put(by+22, bx, R('\u2502')+YL(f'  {tk}  REMAINING  {mm:02d} min  {ss:02d} sec'.ljust(bw-2))+R('\u2502'))
            tck=['SCANNING KEY SPACE\u2026','TESTING PERMUTATIONS\u2026','CROSS-REFERENCING DB\u2026','MAGI CONSENSUS\u2026','DECRYPTION ACTIVE\u2026']
            put(by+23, bx, R('\u2502')+MU(f'  {tck[sec%len(tck)]}'[:bw-2].ljust(bw-2))+R('\u2502'))
            if pct >= 1.0:
                put(by+22, bx, R('\u2502')+GN('  RICK ROLLING YOU NOW  \u2014  NO WAY IN WITHOUT PASSWORD'.ljust(bw-2))+R('\u2502'))
                time.sleep(1.0); rick_open(); time.sleep(2.0); return

# ─────────────────────────────────────────────────────────────────────────────
def pq_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,80); bh=14; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('\u2502')+OR('  ENTER P AND Q VALUES'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('\u2502')+WH('  Paste both values separated by whitespace, or as p=.. q=..'.ljust(bw-2))+R('\u2502'))
        put(by+4, bx, R('\u2502')+WH('  These will be used to decrypt Encrypted.txt'.ljust(bw-2))+R('\u2502'))
        put(by+5, bx, R(box_s(bw)))
        for r in range(6,11): put(by+r, bx, R('\u2502')+' '*(bw-2)+R('\u2502'))
        put(by+11,bx, R(box_s(bw)))
        put(by+12,bx, R('\u2502')+MU('  ENTER to submit    ESC to quit'.ljust(bw-2))+R('\u2502'))
        put(by+13,bx, R(box_b(bw)))
        buf = []
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_bs(k):
                if buf: buf.pop()
                put(by+6, bx, R('\u2502')+WH(('  '+''.join(buf))[-(bw-2):].ljust(bw-2))+R('\u2502'))
                continue
            if is_ret(k):
                raw = ''.join(buf).strip()
                if 'p=' in raw and 'q=' in raw:
                    p = raw.split('p=',1)[1].split()[0].strip(',;')
                    q = raw.split('q=',1)[1].split()[0].strip(',;')
                else:
                    parts = raw.split(); p,q = (parts+['',''])[:2]
                if p and q:
                    put(by+8, bx, R('\u2502')+GN('  Running decryption\u2026'.ljust(bw-2))+R('\u2502'))
                    time.sleep(0.5); return p, q
                put(by+8, bx, R('\u2502')+BR('  Could not parse p and q. Try again.'.ljust(bw-2))+R('\u2502'))
                continue
            c = kch(k)
            if c and len(buf) < BUF_MAX:  # FIX #5: cap buffer
                buf.append(c)
                put(by+6, bx, R('\u2502')+WH(('  '+''.join(buf))[-(bw-2):].ljust(bw-2))+R('\u2502'))

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
        put(by+1, bx, R('\u2502')+OR('  DECRYPTION COMPLETE \u2014 MAGI OUTPUT'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R(box_s(bw)))
        for i,ln in enumerate(lines):
            put(by+3+i, bx, R('\u2502')+'  '+WH(ln[:iw].ljust(iw))+'  '+R('\u2502'))
        fr = by+3+vis
        put(fr,   bx, R(box_s(bw)))
        put(fr+1, bx, R('\u2502')+MU('  Decryption successful. Proceed?'.ljust(bw-2))+R('\u2502'))
        put(fr+2, bx, R('\u2502')+AM('  ENTER \u2500 next   ESC \u2500 abort'.ljust(bw-2))+R('\u2502'))
        put(fr+3, bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k): return

# ─────────────────────────────────────────────────────────────────────────────
def terms_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,86); bh=14; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('\u2502')+OR('  NERV TERMS & CONDITIONS'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('\u2502')+WH('  Do you accept the following terms?'.ljust(bw-2))+R('\u2502'))
        put(by+4, bx, R(box_s(bw)))
        put(by+5, bx, R('\u2502')+AM('  YES  \u2500  \u5df2\u9605\u8bfb\u5e76\u540c\u610f Instagram \u670d\u52a1\u6761\u6b3e (Chinese)'.ljust(bw-2))+R('\u2502'))
        put(by+6, bx, R('\u2502')+MU('  NO   \u2500  YouTube \u30b5\u30fc\u30d3\u30b9\u5229\u7528\u898f\u7d04 (Japanese)'.ljust(bw-2))+R('\u2502'))
        put(by+7, bx, R(box_s(bw)))
        put(by+8, bx, R('\u2502')+WH('  Type YES or NO and press ENTER'.ljust(bw-2))+R('\u2502'))
        put(by+9, bx, R('\u2502')+' '*(bw-2)+R('\u2502'))
        put(by+10,bx, R('\u2502')+' '*(bw-2)+R('\u2502'))
        put(by+11,bx, R(box_s(bw)))
        put(by+12,bx, R('\u2502')+MU('  ESC to exit'.ljust(bw-2))+R('\u2502'))
        put(by+13,bx, R(box_b(bw)))
        buf = []
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k):
                return ''.join(buf).strip().lower() == 'yes'
            c = kch(k)
            if c and c.isalpha() and len(buf) < BUF_MAX:  # FIX #5
                buf.append(c.upper())
                put(by+10, bx, R('\u2502')+WH(('  '+''.join(buf))[-(bw-2):].ljust(bw-2))+R('\u2502'))

# ─────────────────────────────────────────────────────────────────────────────
def yes_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,80); bh=12; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('\u2502')+BR('  YAYYYYYYYYYY'.ljust(bw-2))+R('\u2502'))
        put(by+2, bx, R('\u2502')+BR('  you got a secret message !!!!'.ljust(bw-2))+R('\u2502'))
        put(by+3, bx, R(box_s(bw)))
        put(by+4, bx, R('\u2502')+AM('  \u30cd\u30eb\u30d5\u6a5f\u5bc6\u6587\u66f8 \u2500 TOP SECRET \u2500 FINAL INTEL'.ljust(bw-2))+R('\u2502'))
        put(by+5, bx, R('\u2502')+WH('  press ENTER to reveal the secret message'.ljust(bw-2))+R('\u2502'))
        put(by+6, bx, R(box_s(bw)))
        put(by+7, bx, R('\u2502')+MU('  SHINJI  ASUKA  REI  \u2014  all waiting for you to know'.ljust(bw-2))+R('\u2502'))
        put(by+8, bx, R('\u2502')+MU('  do not be afraid  \u2014  this is definitely not a rick-roll'.ljust(bw-2))+R('\u2502'))
        put(by+9, bx, R(box_s(bw)))
        put(by+10,bx, R('\u2502')+DI('  [ ENTER to proceed ]   [ ESC to cowardly flee ]'.ljust(bw-2))+R('\u2502'))
        put(by+11,bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k): rick_open(); return

def no_screen():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,80); bh=10; bx=(W-bw)//2; by=max(1,(H-bh)//2)
        put(by,  bx, R(box_t(bw)))
        put(by+1,bx, R('\u2502')+BR('  REFUSED  \u2014  MAGI OVERRIDE ACTIVATED'.ljust(bw-2))+R('\u2502'))
        put(by+2,bx, R(box_s(bw)))
        put(by+3,bx, R('\u2502')+MU('  You refused. NERV does not accept refusal.'.ljust(bw-2))+R('\u2502'))
        put(by+4,bx, R('\u2502')+MU('  Redirecting to mandatory training material.'.ljust(bw-2))+R('\u2502'))
        put(by+5,bx, R(box_s(bw)))
        put(by+6,bx, R('\u2502')+AM('  Deploying classified footage directly to terminal\u2026'.ljust(bw-2))+R('\u2502'))
        put(by+7,bx, R('\u2502')+DI('  (there is no escape)'.ljust(bw-2))+R('\u2502'))
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
