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

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_CODE = "NERV0"   # change later

# ── Helpers ───────────────────────────────────────────────────────────────────
def is_space(k):  return (not k.is_sequence) and str(k) == ' '
def is_esc(k):    return k.is_sequence and k.name == 'KEY_ESCAPE'
def is_enter(k):
    return (k.is_sequence and k.name in ('KEY_ENTER',)) or str(k) in ('\n', '\r')

def is_backspace(k):
    return (k.is_sequence and k.name in ('KEY_BACKSPACE', 'KEY_DELETE')) or str(k) in ('\x7f', '\b')

def key_char(k):
    if not k.is_sequence and len(str(k)) == 1:
        return str(k)
    return None

def put(row, col, text):
    print(term.move(row, max(0, col)) + text, end='', flush=True)

def center(text, width):
    return max(0, (width - len(text)) // 2)

# ── Box ───────────────────────────────────────────────────────────────────────
def box_top(w):        return '┌' + '─' * (w-2) + '┐'
def box_bot(w):        return '└' + '─' * (w-2) + '┘'
def box_sep(w):        return '├' + '─' * (w-2) + '┤'
def box_row(w, s=''):  return '│' + s[:w-2].ljust(w-2) + '│'

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1 — SPLASH
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash():
    fig_main = Figlet(font='banner3')
    art = [l for l in fig_main.renderText('NERV').splitlines() if l.strip()]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w   = term.height, term.width
        narrow = w < 50

        for row in range(h):
            put(row, 0, c_dred('░' * w))

        bw = min(w, 64) if not narrow else w
        bh = h - 4
        bx = (w - bw) // 2
        by = 2

        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by,          bx, c_red('▀' * bw))
        put(by + bh - 1, bx, c_red('▄' * bw))

        # refined logo framing
        top_label = ' NERV HEADQUARTERS '
        put(by + 1, bx + center(top_label, bw), c_muted(top_label))

        max_aw = max(len(l) for l in art) if art else 1
        logo   = art if (not narrow or max_aw <= bw - 8) else ['N  E  R  V']
        lx     = bx + center(max(logo, key=len), bw)
        ly     = by + 3
        for i, line in enumerate(logo[:bh - 12]):
            put(ly + i, lx, c_red(line[:bw]))

        art_end = ly + len(logo[:bh - 12])

        underline = '━' * min(max(18, bw // 2), bw - 8)
        put(art_end + 1, bx + center(underline, bw), c_dred(underline))

        tags = [
            ('GEHIRN ADVANCED RESEARCH',   c_amber),
            ('MAGI SYSTEM  v3.0',          c_muted),
            ('CLASSIFICATION  TOP SECRET', c_muted),
        ]
        for i, (txt, col) in enumerate(tags):
            short = txt[:bw - 4]
            put(art_end + 3 + i, bx + center(short, bw), col(short))

        prompt   = '[ SPACE ]  START' if narrow else '[ PRESS SPACE TO INITIALIZE ]'
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
            if not key:
                continue
            if is_space(key):
                stop_ev.set()
                t.join(0.7)
                while term.inkey(timeout=0):
                    pass
                break
            if is_esc(key):
                stop_ev.set()
                sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2 — PASSWORD GATE
# ─────────────────────────────────────────────────────────────────────────────
def draw_password_gate():
    typed = []
    error = ''
    error_until = 0.0

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        while True:
            print(term.clear)
            h, w = term.height, term.width
            narrow = w < 55

            for row in range(h):
                put(row, 0, c_dred('░' * w))

            bw = min(w, 62) if not narrow else w
            bh = min(h - 4, 15)
            bx = (w - bw) // 2
            by = max(2, (h - bh) // 2)

            for row in range(bh):
                put(by + row, bx, term.on_black + ' ' * bw + term.normal)

            put(by,          bx, c_red(box_top(bw)))
            put(by + 1,      bx, c_red('│') + c_orange('  MAGI AUTHENTICATION'.ljust(bw - 2)) + c_red('│'))
            put(by + 2,      bx, c_red(box_sep(bw)))
            put(by + 3,      bx, c_red('│') + c_white('  Enter access code to proceed.'.ljust(bw - 2)) + c_red('│'))
            put(by + 4,      bx, c_red('│') + c_muted('  Input is masked. Press Enter to confirm.'.ljust(bw - 2)) + c_red('│'))
            put(by + 5,      bx, c_red(box_sep(bw)))

            masked = ' '.join('●' for _ in typed)
            if not masked:
                masked = '· · · · ·'
            field = f'  CODE  {masked}'
            put(by + 6, bx, c_red('│') + c_amber(field[:bw - 2].ljust(bw - 2)) + c_red('│'))

            hint = '  5-character alphanumeric code'
            put(by + 7, bx, c_red('│') + c_muted(hint[:bw - 2].ljust(bw - 2)) + c_red('│'))

            msg = ''
            if time.time() < error_until:
                msg = error
            put(by + 8, bx, c_red('│') + (c_bright(msg[:bw - 2].ljust(bw - 2)) if msg else ' ' * (bw - 2)) + c_red('│'))

            footer = '  [ ENTER ] confirm    [ BACKSPACE ] erase    [ ESC ] quit'
            put(by + 10, bx, c_red('│') + c_muted(footer[:bw - 2].ljust(bw - 2)) + c_red('│'))
            put(by + 11, bx, c_red(box_bot(bw)))

            key = term.inkey(timeout=0.08)
            if not key:
                continue
            if is_esc(key):
                sys.exit(0)
            if is_enter(key):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    return True
                error = '  ACCESS DENIED  —  Invalid code'
                error_until = time.time() + 1.8
                typed.clear()
                continue
            if is_backspace(key):
                if typed:
                    typed.pop()
                continue

            ch = key_char(key)
            if ch and ch.isalnum() and len(typed) < 5:
                typed.append(ch.upper())

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 3 — PILOT INTERFACE
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
    filled = int(width * pct)
    return c_green('█' * filled) + c_dim('░' * max(0, width - filled))


def draw_wide(h, w, feedback, fb_until):
    now = time.time()
    pw  = min(w, 70)
    px  = (w - pw) // 2
    py  = 2
    ph  = h - 4

    put(0, 0, c_dred('░' * w))
    put(h - 1, 0, c_dred('░' * w))

    put(py,          px, c_red(box_top(pw)))
    put(py + ph - 1, px, c_red(box_bot(pw)))
    for row in range(1, ph - 1):
        put(py + row, px, c_red('│'))
        put(py + row, px + pw - 1, c_red('│'))

    title = '  NERV  //  PILOT INTERFACE  v2.0'
    put(py + 1, px, c_red('│') + c_orange(title[:pw-2].ljust(pw-2)) + c_red('│'))
    put(py + 2, px, c_red(box_sep(pw)))

    inner_w = pw - 4
    row = py + 3

    for i, (k, v) in enumerate(PILOT_DATA):
        cell = f'  {k:<12}  {v}'
        col = c_amber if i % 2 == 0 else c_white
        put(row, px, c_red('│') + col(cell[:pw-2].ljust(pw-2)) + c_red('│'))
        row += 1

    bar_label = '  SYNC RATIO  '
    bar_space = max(6, inner_w - len(bar_label) - 2)
    put(row, px, c_red('│') + c_muted(bar_label) + _sync_bar(0.413, bar_space) + c_muted('  ') + c_red('│'))
    row += 1

    put(row, px, c_red(box_sep(pw)))
    row += 1
    put(row, px, c_red('│') + c_orange('  COMMAND INTERFACE'.ljust(pw-2)) + c_red('│'))
    row += 1
    put(row, px, c_red(box_sep(pw)))
    row += 1

    for key, label in MENU:
        entry = f'   [ {key} ]   {label}'
        put(row, px, c_red('│') + c_white(entry[:pw-2].ljust(pw-2)) + c_red('│'))
        row += 1

    put(row, px, c_red(box_sep(pw)))
    row += 1

    fb = feedback[0] if now < fb_until[0] else ''
    while row < py + ph - 2:
        line = fb if fb and row == py + ph - 3 else ''
        filler = line[:pw-2].ljust(pw-2) if line else ' ' * (pw - 2)
        col = c_bright if line else c_dim
        put(row, px, c_red('│') + col(filler) + c_red('│'))
        row += 1

    tick = '▐▌' if int(now * 2) % 2 == 0 else '  '
    bar = f'  MAGI ONLINE {tick}   THREAT: NONE   T+{int(now)%9999:04d}s  '
    put(h - 2, 0, c_amber(bar[:w].ljust(w)))


def draw_narrow(h, w, feedback, fb_until):
    now = time.time()

    put(0, 0, c_dred('░' * w))
    title = 'NERV  PILOT INTERFACE'
    put(1, center(title, w), c_red(title[:w]))
    put(2, 0, c_dred('─' * w))

    row = 3
    for i, (k, v) in enumerate(PILOT_DATA):
        line = f'{k:<10}  {v}'
        col = c_amber if i % 2 == 0 else c_white
        put(row, 1, col(line[:w-2]))
        row += 1

    bar_w = max(4, w - 14)
    put(row, 1, c_muted('SYNC  ') + _sync_bar(0.413, bar_w))
    row += 1

    put(row, 0, c_dred('─' * w))
    row += 1
    put(row, 1, c_orange('COMMANDS'))
    row += 1
    for key, label in MENU:
        if row >= h - 4:
            break
        put(row, 1, c_white(f'[{key}]  {label}'[:w-2]))
        row += 1

    put(row, 0, c_dred('─' * w))
    fb = feedback[0] if now < fb_until[0] else ''
    put(h - 3, 0, c_bright(fb[:w].ljust(w)))
    put(h - 2, 0, c_dred('─' * w))
    tick = '▐▌' if int(now * 2) % 2 == 0 else '  '
    put(h - 1, 0, c_amber(f'{tick}  T+{int(now)%9999:04d}s'[:w].ljust(w)))


def draw_pilot_interface():
    feedback = ['']
    fb_until = [0.0]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        while True:
            h, w = term.height, term.width
            now = time.time()
            narrow = w < 55

            if narrow:
                draw_narrow(h, w, feedback, fb_until)
            else:
                draw_wide(h, w, feedback, fb_until)

            key = term.inkey(timeout=0.06)
            if not key:
                continue
            ch = key_char(key)

            if ch and ch.lower() == 'q' or is_esc(key):
                break
            elif ch and ch.lower() in MSGS:
                feedback[0] = MSGS[ch.lower()]
                fb_until[0] = now + 2.5

# ─────────────────────────────────────────────────────────────────────────────
def main():
    try:
        draw_splash()
        draw_password_gate()
        draw_pilot_interface()
    except KeyboardInterrupt:
        pass
    finally:
        print(term.clear + term.normal)
        print(c_red('\n  [ NERV ]  Session terminated.\n'))

if __name__ == '__main__':
    main()
