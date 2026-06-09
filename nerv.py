#!/usr/bin/env python3
"""
NERV Terminal — Neon Genesis Evangelion themed terminal launcher
Usage: python3 nerv.py
Dependencies: blessed pyfiglet
"""

import sys
import time
import random
import threading
from blessed import Terminal
from pyfiglet import Figlet

term = Terminal()

# ── Palette ───────────────────────────────────────────────────────────────────
def c_red(s):      return term.color_rgb(210, 25,  25)  + s + term.normal
def c_orange(s):   return term.color_rgb(255, 100, 10)  + s + term.normal
def c_amber(s):    return term.color_rgb(255, 170, 0)   + s + term.normal
def c_dred(s):     return term.color_rgb(110, 0,   0)   + s + term.normal
def c_white(s):    return term.color_rgb(225, 215, 195) + s + term.normal
def c_dim(s):      return term.color_rgb(75,  65,  55)  + s + term.normal
def c_green(s):    return term.color_rgb(0,   210, 90)  + s + term.normal
def c_bright(s):   return term.color_rgb(255, 60,  60)  + s + term.normal
def c_muted(s):    return term.color_rgb(140, 120, 100) + s + term.normal

# ── Helpers ───────────────────────────────────────────────────────────────────
def is_space(k):  return (not k.is_sequence) and str(k) == ' '
def is_esc(k):    return k.is_sequence and k.name == 'KEY_ESCAPE'
def key_char(k):
    if not k.is_sequence and len(str(k)) == 1:
        return str(k).lower()
    return None

def put(row, col, text):
    print(term.move(row, max(0, col)) + text, end='', flush=True)

def center(text, width):
    return max(0, (width - len(text)) // 2)

def hline(w, char='─'):
    return char * w

# ── Box ───────────────────────────────────────────────────────────────────────
def box_top(w):        return '┌' + '─' * (w-2) + '┐'
def box_bot(w):        return '└' + '─' * (w-2) + '┘'
def box_sep(w):        return '├' + '─' * (w-2) + '┤'
def box_row(w, s=''):  return '│' + s[:w-2].ljust(w-2) + '│'

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1 — SPLASH
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash():
    fig = Figlet(font='banner3')
    art = [l for l in fig.renderText('NERV').splitlines() if l.strip()]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w   = term.height, term.width
        NARROW = w < 50

        # ── Subtle scanline bg ──
        SCAN = '░'
        for row in range(h):
            put(row, 0, c_dred(SCAN * w))

        # ── Center card ──
        bw = min(w, 58) if not NARROW else w
        bh = h - 4
        bx = (w - bw) // 2
        by = 2

        # Black fill
        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        # Top / bottom accent bars
        put(by,          bx, c_red('▀' * bw))
        put(by + bh - 1, bx, c_red('▄' * bw))

        # ── NERV logo ──
        max_aw = max(len(l) for l in art) if art else 1
        logo   = art if (not NARROW or max_aw <= bw - 2) else ['N  E  R  V']
        lx     = bx + center(max(logo, key=len), bw)
        ly     = by + 2
        for i, line in enumerate(logo[:bh - 9]):
            put(ly + i, lx, c_red(line[:bw]))

        art_end = ly + len(logo[:bh - 9])

        # ── Thin divider ──
        put(art_end + 1, bx + 2, c_dred('─' * (bw - 4)))

        # ── Tag lines ──
        tags = [
            ('GEHIRN ADVANCED RESEARCH',  c_amber),
            ('MAGI SYSTEM  v3.0',         c_muted),
            ('CLASSIFICATION  TOP SECRET', c_muted),
        ]
        for i, (txt, col) in enumerate(tags):
            short = txt[:bw - 4]
            put(art_end + 2 + i, bx + center(short, bw), col(short))

        # ── Blinking prompt ──
        prompt   = '[ SPACE ]  START' if NARROW else '[ PRESS SPACE TO INITIALIZE ]'
        prompt_y = by + bh - 3
        prompt_x = bx + center(prompt, bw)
        stop_ev  = threading.Event()

        def blink():
            visible = True
            while not stop_ev.is_set():
                txt = c_amber(prompt) if visible else ' ' * len(prompt)
                put(prompt_y, prompt_x, txt)
                visible = not visible
                stop_ev.wait(0.55)

        t = threading.Thread(target=blink, daemon=True)
        t.start()

        while True:
            key = term.inkey(timeout=0.05)
            if not key: continue
            if is_space(key):
                stop_ev.set(); t.join(0.7)
                while term.inkey(timeout=0): pass
                break
            if is_esc(key):
                stop_ev.set(); sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2 — PILOT INTERFACE
# ─────────────────────────────────────────────────────────────────────────────
PILOT_DATA = [
    ('PILOT',     'IKARI, SHINJI'),
    ('UNIT',      'EVA-01'),
    ('SYNC',      '41.3 %'),
    ('A.T.FIELD', 'ACTIVE'),
    ('STATUS',    'STANDBY'),
    ('THREAT',    'ANGEL  CL.4'),
]

MENU = [
    ('A', 'ACTIVATE EVA'),
    ('S', 'SYNC UPLINK'),
    ('D', 'TACTICAL DISPLAY'),
    ('M', 'MAGI QUERY'),
    ('Q', 'EXIT'),
]

MSGS = {
    'a': '  >>  ACTIVATING EVA UNIT  —  STANDBY',
    's': '  >>  INITIATING SYNC UPLINK  ...',
    'd': '  >>  LOADING TACTICAL DISPLAY  ...',
    'm': '  >>  QUERYING MAGI SYSTEM  ...',
}


def _sync_bar(pct, width):
    """Simple block progress bar."""
    filled = int(width * pct)
    return c_green('█' * filled) + c_dim('░' * (width - filled))


def draw_wide(h, w, feedback, fb_until):
    now = time.time()
    PW  = min(w, 70)          # total panel width
    PX  = (w - PW) // 2      # left offset (centered)
    PY  = 2
    PH  = h - 4

    # ── Noise strip top & bottom ──
    put(0,     0, c_dred('░' * w))
    put(h - 1, 0, c_dred('░' * w))

    # ── Outer box ──
    put(PY,          PX, c_red(box_top(PW)))
    put(PY + PH - 1, PX, c_red(box_bot(PW)))
    for row in range(1, PH - 1):
        put(PY + row, PX,          c_red('│'))
        put(PY + row, PX + PW - 1, c_red('│'))

    # ── Title bar ──
    title = '  NERV  //  PILOT INTERFACE  v2.0'
    put(PY + 1, PX, c_red('│') + c_orange(title[:PW-2].ljust(PW-2)) + c_red('│'))
    put(PY + 2, PX, c_red(box_sep(PW)))

    IW = PW - 4   # inner width
    IX = PX + 2   # inner x
    row = PY + 3

    # ── Pilot data table ──
    for i, (k, v) in enumerate(PILOT_DATA):
        cell = f'  {k:<12}  {v}'
        col  = c_amber if i % 2 == 0 else c_white
        put(row, PX, c_red('│') + col(cell[:PW-2].ljust(PW-2)) + c_red('│'))
        row += 1

    # Sync bar row
    bar_label = '  SYNC RATIO  '
    bar_space  = IW - len(bar_label) - 2
    put(row, PX, c_red('│') + c_muted(bar_label)
        + _sync_bar(0.413, bar_space)
        + c_muted('  ') + c_red('│'))
    row += 1

    put(row, PX, c_red(box_sep(PW))); row += 1

    # ── Commands ──
    put(row, PX, c_red('│') + c_orange('  COMMAND INTERFACE'[:PW-2].ljust(PW-2)) + c_red('│'))
    row += 1
    put(row, PX, c_red(box_sep(PW))); row += 1

    for key, label in MENU:
        entry = f'   [ {key} ]   {label}'
        put(row, PX, c_red('│') + c_white(entry[:PW-2].ljust(PW-2)) + c_red('│'))
        row += 1

    put(row, PX, c_red(box_sep(PW))); row += 1

    # ── Feedback / status ──
    fb = feedback[0] if now < fb_until[0] else ''
    while row < PY + PH - 2:
        line = fb if fb and row == PY + PH - 3 else ''
        col  = c_bright if line else c_dim
        filler = line[:PW-2].ljust(PW-2) if line else ' ' * (PW-2)
        put(row, PX, c_red('│') + col(filler) + c_red('│'))
        row += 1

    # ── Bottom ticker ──
    tick = '▐▌' if int(now * 2) % 2 == 0 else '  '
    bar  = f'  MAGI ONLINE {tick}   THREAT: NONE   T+{int(now)%9999:04d}s  '
    put(h - 2, 0, c_amber(bar[:w].ljust(w)))


def draw_narrow(h, w, feedback, fb_until):
    """Clean minimal single-column layout for phones."""
    now = time.time()

    # ── Header ──
    put(0, 0, c_dred('░' * w))
    title = 'NERV  PILOT INTERFACE'
    put(1, center(title, w), c_red(title[:w]))
    put(2, 0, c_dred('─' * w))

    row = 3

    # ── Pilot data ──
    for i, (k, v) in enumerate(PILOT_DATA):
        line = f'{k:<10}  {v}'
        col  = c_amber if i % 2 == 0 else c_white
        put(row, 1, col(line[:w-2]))
        row += 1

    # Inline sync bar
    bar_w = max(4, w - 14)
    put(row, 1, c_muted('SYNC  ') + _sync_bar(0.413, bar_w))
    row += 1

    put(row, 0, c_dred('─' * w)); row += 1

    # ── Commands ──
    put(row, 1, c_orange('COMMANDS')); row += 1
    for key, label in MENU:
        if row >= h - 4: break
        put(row, 1, c_white(f'[{key}]  {label}'[:w-2]))
        row += 1

    put(row, 0, c_dred('─' * w)); row += 1

    # ── Feedback ──
    fb = feedback[0] if now < fb_until[0] else ''
    put(h - 3, 0, c_bright(fb[:w].ljust(w)))

    # ── Ticker ──
    put(h - 2, 0, c_dred('─' * w))
    tick = '▐▌' if int(now * 2) % 2 == 0 else '  '
    put(h - 1, 0, c_amber(f'{tick}  T+{int(now)%9999:04d}s'[:w].ljust(w)))


def draw_pilot_interface():
    feedback = ['']
    fb_until = [0.0]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)

        while True:
            h, w   = term.height, term.width
            now    = time.time()
            NARROW = w < 55

            if NARROW:
                draw_narrow(h, w, feedback, fb_until)
            else:
                draw_wide(h, w, feedback, fb_until)

            key = term.inkey(timeout=0.06)
            if not key: continue
            ch = key_char(key)

            if ch == 'q' or is_esc(key):
                break
            elif ch in MSGS:
                feedback[0] = MSGS[ch]
                fb_until[0] = now + 2.5


# ─────────────────────────────────────────────────────────────────────────────
def main():
    try:
        draw_splash()
        draw_pilot_interface()
    except KeyboardInterrupt:
        pass
    finally:
        print(term.clear + term.normal)
        print(c_red('\n  [ NERV ]  Session terminated.\n'))

if __name__ == '__main__':
    main()
