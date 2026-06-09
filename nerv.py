#!/usr/bin/env python3
"""
NERV Terminal — Neon Genesis Evangelion themed terminal launcher
Usage: python3 nerv.py
Dependencies: blessed pyfiglet
"""

import sys
import time
import threading
from blessed import Terminal
from pyfiglet import Figlet

term = Terminal()

# ── Palette ───────────────────────────────────────────────────────────────────
def c_red(s):    return term.color_rgb(210, 25,  25)  + s + term.normal
def c_orange(s): return term.color_rgb(255, 100, 10)  + s + term.normal
def c_amber(s):  return term.color_rgb(255, 170, 0)   + s + term.normal
def c_dred(s):   return term.color_rgb(110, 0,   0)   + s + term.normal
def c_white(s):  return term.color_rgb(225, 215, 195) + s + term.normal
def c_dim(s):    return term.color_rgb(75,  65,  55)  + s + term.normal
def c_green(s):  return term.color_rgb(0,   210, 90)  + s + term.normal
def c_bright(s): return term.color_rgb(255, 60,  60)  + s + term.normal
def c_muted(s):  return term.color_rgb(140, 120, 100) + s + term.normal

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_CODE = "NERV0"   # <─ change this to your code

# ── Helpers ───────────────────────────────────────────────────────────────────
def is_space(k):     return (not k.is_sequence) and str(k) == ' '
def is_esc(k):       return k.is_sequence and k.name == 'KEY_ESCAPE'
def is_enter(k):     return (k.is_sequence and k.name == 'KEY_ENTER') or str(k) in ('\n', '\r')
def is_backspace(k): return (k.is_sequence and k.name in ('KEY_BACKSPACE', 'KEY_DELETE')) or str(k) in ('\x7f', '\b')
def key_char(k):
    if not k.is_sequence and len(str(k)) == 1:
        return str(k)
    return None

def put(row, col, text):
    print(term.move(row, max(0, col)) + text, end='', flush=True)

def center(text, width):
    return max(0, (width - len(text)) // 2)

# ── Box ───────────────────────────────────────────────────────────────────────
def box_top(w):       return '┌' + '─'*(w-2) + '┐'
def box_bot(w):       return '└' + '─'*(w-2) + '┘'
def box_sep(w):       return '├' + '─'*(w-2) + '┤'
def box_row(w, s=''): return '│' + s[:w-2].ljust(w-2) + '│'

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1 — SPLASH
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash():
    art = [l for l in Figlet(font='banner3').renderText('NERV').splitlines() if l.strip()]

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

        top_label = ' NERV HEADQUARTERS '
        put(by + 1, bx + center(top_label, bw), c_muted(top_label))

        max_aw = max(len(l) for l in art) if art else 1
        logo   = art if (not narrow or max_aw <= bw - 8) else ['N  E  R  V']
        lx     = bx + center(max(logo, key=len), bw)
        ly     = by + 3
        for i, line in enumerate(logo[:bh - 12]):
            put(ly + i, lx, c_red(line[:bw]))

        art_end = ly + len(logo[:bh - 12])
        uline   = '━' * min(max(18, bw // 2), bw - 8)
        put(art_end + 1, bx + center(uline, bw), c_dred(uline))

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
                put(prompt_y, prompt_x, c_amber(prompt) if visible else ' ' * len(prompt))
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
# SCREEN 2 — PASSWORD GATE
# Strategy: draw the static frame ONCE, then only overwrite the two
# mutable rows: the code field (row_field) and the message row (row_msg).
# ─────────────────────────────────────────────────────────────────────────────
def draw_password_gate():
    typed       = []
    msg         = ''
    msg_until   = 0.0
    last_typed  = None    # track changes so we only repaint on actual input
    last_msg    = None

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w   = term.height, term.width
        narrow = w < 55

        bw = min(w, 62) if not narrow else w
        bh = 14
        bx = (w - bw) // 2
        by = max(2, (h - bh) // 2)

        # ── Draw static background + frame ONCE ──
        for row in range(h):
            put(row, 0, c_dred('░' * w))
        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by,     bx, c_red(box_top(bw)))
        put(by + 1, bx, c_red('│') + c_orange('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw - 2)) + c_red('│'))
        put(by + 2, bx, c_red(box_sep(bw)))
        put(by + 3, bx, c_red('│') + c_white('  Enter 5-character access code:'.ljust(bw - 2)) + c_red('│'))
        put(by + 4, bx, c_red(box_sep(bw)))
        # row 5 — code field  (dynamic)
        put(by + 5, bx, c_red('│') + ' ' * (bw - 2) + c_red('│'))
        put(by + 6, bx, c_red(box_sep(bw)))
        # row 7 — message row (dynamic)
        put(by + 7, bx, c_red('│') + ' ' * (bw - 2) + c_red('│'))
        put(by + 8, bx, c_red(box_sep(bw)))
        put(by + 9, bx,  c_red('│') + c_muted('  [ ENTER ] confirm'.ljust(bw - 2)) + c_red('│'))
        put(by + 10, bx, c_red('│') + c_muted('  [ BKSP  ] erase'.ljust(bw - 2))  + c_red('│'))
        put(by + 11, bx, c_red('│') + c_muted('  [ ESC   ] quit'.ljust(bw - 2))   + c_red('│'))
        put(by + 12, bx, c_red(box_sep(bw)))
        put(by + 13, bx, c_red(box_bot(bw)))

        row_field = by + 5
        row_msg   = by + 7

        def _redraw_field():
            dots = '  '.join('●' for _ in typed) if typed else '·  ·  ·  ·  ·'
            field = f'  CODE   {dots}'
            put(row_field, bx, c_red('│') + c_amber(field[:bw - 2].ljust(bw - 2)) + c_red('│'))

        def _redraw_msg(text='', is_err=False):
            col  = c_bright if is_err else c_green
            line = f'  {text}' if text else ''
            put(row_msg, bx, c_red('│') + (col(line[:bw - 2].ljust(bw - 2)) if line else ' ' * (bw - 2)) + c_red('│'))

        # Initial paint of both dynamic rows
        _redraw_field()
        _redraw_msg()

        while True:
            key = term.inkey(timeout=0.1)

            # Clear expired error message without waiting for a keypress
            if msg and time.time() >= msg_until:
                msg = ''
                _redraw_msg()

            if not key:
                continue

            if is_esc(key):
                sys.exit(0)

            if is_enter(key):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    _redraw_msg('ACCESS GRANTED', is_err=False)
                    time.sleep(0.6)
                    return True
                msg       = 'ACCESS DENIED  —  Invalid code'
                msg_until = time.time() + 1.8
                typed.clear()
                _redraw_field()
                _redraw_msg(msg, is_err=True)
                continue

            if is_backspace(key):
                if typed:
                    typed.pop()
                    _redraw_field()
                continue

            ch = key_char(key)
            if ch and ch.isalnum() and len(typed) < 5:
                typed.append(ch.upper())
                _redraw_field()


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

    put(0,     0, c_dred('░' * w))
    put(h - 1, 0, c_dred('░' * w))
    put(py,          px, c_red(box_top(pw)))
    put(py + ph - 1, px, c_red(box_bot(pw)))
    for r in range(1, ph - 1):
        put(py + r, px,          c_red('│'))
        put(py + r, px + pw - 1, c_red('│'))

    put(py + 1, px, c_red('│') + c_orange('  NERV  //  PILOT INTERFACE  v2.0'[:pw-2].ljust(pw-2)) + c_red('│'))
    put(py + 2, px, c_red(box_sep(pw)))

    row = py + 3
    iw  = pw - 4
    for i, (k, v) in enumerate(PILOT_DATA):
        col = c_amber if i % 2 == 0 else c_white
        put(row, px, c_red('│') + col(f'  {k:<12}  {v}'[:pw-2].ljust(pw-2)) + c_red('│'))
        row += 1

    bar_lbl = '  SYNC RATIO  '
    put(row, px, c_red('│') + c_muted(bar_lbl) + _sync_bar(0.413, max(6, iw - len(bar_lbl) - 2)) + c_muted('  ') + c_red('│'))
    row += 1

    put(row, px, c_red(box_sep(pw))); row += 1
    put(row, px, c_red('│') + c_orange('  COMMAND INTERFACE'.ljust(pw-2)) + c_red('│')); row += 1
    put(row, px, c_red(box_sep(pw))); row += 1
    for k, lbl in MENU:
        put(row, px, c_red('│') + c_white(f'   [ {k} ]   {lbl}'[:pw-2].ljust(pw-2)) + c_red('│'))
        row += 1
    put(row, px, c_red(box_sep(pw))); row += 1

    fb = feedback[0] if now < fb_until[0] else ''
    while row < py + ph - 2:
        line   = fb if fb and row == py + ph - 3 else ''
        filler = line[:pw-2].ljust(pw-2) if line else ' ' * (pw-2)
        put(row, px, c_red('│') + (c_bright(filler) if line else c_dim(filler)) + c_red('│'))
        row += 1

    tick = '▐▌' if int(now * 2) % 2 == 0 else '  '
    put(h - 2, 0, c_amber(f'  MAGI ONLINE {tick}   THREAT: NONE   T+{int(now)%9999:04d}s  '[:w].ljust(w)))

def draw_narrow(h, w, feedback, fb_until):
    now = time.time()
    put(0, 0, c_dred('░' * w))
    title = 'NERV  PILOT INTERFACE'
    put(1, center(title, w), c_red(title[:w]))
    put(2, 0, c_dred('─' * w))
    row = 3
    for i, (k, v) in enumerate(PILOT_DATA):
        col = c_amber if i % 2 == 0 else c_white
        put(row, 1, col(f'{k:<10}  {v}'[:w-2])); row += 1
    put(row, 1, c_muted('SYNC  ') + _sync_bar(0.413, max(4, w - 14))); row += 1
    put(row, 0, c_dred('─' * w)); row += 1
    put(row, 1, c_orange('COMMANDS')); row += 1
    for k, lbl in MENU:
        if row >= h - 4: break
        put(row, 1, c_white(f'[{k}]  {lbl}'[:w-2])); row += 1
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
            now  = time.time()
            if w < 55:
                draw_narrow(h, w, feedback, fb_until)
            else:
                draw_wide(h, w, feedback, fb_until)
            key = term.inkey(timeout=0.06)
            if not key: continue
            ch = key_char(key)
            if (ch and ch.lower() == 'q') or is_esc(key): break
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
