#!/usr/bin/env python3
"""
NERV Terminal — Neon Genesis Evangelion themed terminal launcher
Usage: python3 nerv.py
Dependencies: blessed pyfiglet
Optional external tool: chafa (for final GIF playback)
"""

import os
import sys
import time
import random
import shutil
import tempfile
import threading
import subprocess
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
def c_cyan(s):   return term.color_rgb(0,   200, 220) + s + term.normal
def c_yellow(s): return term.color_rgb(240, 230, 50)  + s + term.normal

# ── Config ────────────────────────────────────────────────────────────────────
ACCESS_CODE    = "NERV0"
BRUTE_SECONDS  = 10 * 60
FINAL_GIF_URL  = "https://i.redd.it/fktuppkre7p51.gif"

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

def center_x(text, width):
    return max(0, (width - len(text)) // 2)

def box_top(w):
    return '┌' + '─' * (w - 2) + '┐'

def box_bot(w):
    return '└' + '─' * (w - 2) + '┘'

def box_sep(w):
    return '├' + '─' * (w - 2) + '┤'

def clear_key_buffer():
    while term.inkey(timeout=0):
        pass

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1 — SPLASH
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash():
    art = [l for l in Figlet(font='banner3').renderText('NERV').splitlines() if l.strip()]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        narrow = w < 50

        for row in range(h):
            put(row, 0, c_dred('░' * w))

        bw = min(w, 64) if not narrow else w
        bh = h - 4
        bx = (w - bw) // 2
        by = 2

        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by, bx, c_red('▀' * bw))
        put(by + bh - 1, bx, c_red('▄' * bw))

        top_label = ' NERV HEADQUARTERS '
        put(by + 1, bx + center_x(top_label, bw), c_muted(top_label))

        max_aw = max(len(l) for l in art) if art else 1
        logo = art if (not narrow or max_aw <= bw - 8) else ['N  E  R  V']
        lx = bx + center_x(max(logo, key=len), bw)
        ly = by + 3
        for i, line in enumerate(logo[:bh - 12]):
            put(ly + i, lx, c_red(line[:bw]))

        art_end = ly + len(logo[:bh - 12])
        uline = '━' * min(max(18, bw // 2), bw - 8)
        put(art_end + 1, bx + center_x(uline, bw), c_dred(uline))

        for i, (txt, col) in enumerate([
            ('GEHIRN ADVANCED RESEARCH', c_amber),
            ('MAGI SYSTEM  v3.0', c_muted),
            ('CLASSIFICATION  TOP SECRET', c_muted),
        ]):
            short = txt[:bw - 4]
            put(art_end + 3 + i, bx + center_x(short, bw), col(short))

        prompt = '[ SPACE ]  START' if narrow else '[ PRESS SPACE TO INITIALIZE ]'
        prompt_y = by + bh - 3
        prompt_x = bx + center_x(prompt, bw)
        stop_ev = threading.Event()

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
            if not key:
                continue
            if is_space(key):
                stop_ev.set()
                t.join(0.7)
                clear_key_buffer()
                break
            if is_esc(key):
                stop_ev.set()
                sys.exit(0)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2 — PASSWORD GATE
# ─────────────────────────────────────────────────────────────────────────────
def draw_password_gate():
    typed = []
    msg = ''
    msg_until = 0.0

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        narrow = w < 55
        bw = min(w, 62) if not narrow else w
        bh = 14
        bx = (w - bw) // 2
        by = max(2, (h - bh) // 2)

        for row in range(h):
            put(row, 0, c_dred('░' * w))
        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by, bx, c_red(box_top(bw)))
        put(by + 1, bx, c_red('│') + c_orange('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw - 2)) + c_red('│'))
        put(by + 2, bx, c_red(box_sep(bw)))
        put(by + 3, bx, c_red('│') + c_white('  Enter access code to continue:'.ljust(bw - 2)) + c_red('│'))
        put(by + 4, bx, c_red(box_sep(bw)))
        put(by + 5, bx, c_red('│') + ' ' * (bw - 2) + c_red('│'))
        put(by + 6, bx, c_red(box_sep(bw)))
        put(by + 7, bx, c_red('│') + ' ' * (bw - 2) + c_red('│'))
        put(by + 8, bx, c_red(box_sep(bw)))
        put(by + 9, bx, c_red('│') + c_muted('  [ ENTER ] confirm'.ljust(bw - 2)) + c_red('│'))
        put(by + 10, bx, c_red('│') + c_muted('  [ BKSP  ] erase'.ljust(bw - 2)) + c_red('│'))
        put(by + 11, bx, c_red('│') + c_muted('  [ ESC   ] quit'.ljust(bw - 2)) + c_red('│'))
        put(by + 12, bx, c_red(box_sep(bw)))
        put(by + 13, bx, c_red(box_bot(bw)))

        row_field = by + 5
        row_msg = by + 7

        def _field():
            dots = '  '.join('●' for _ in typed) if typed else '·  ·  ·  ·  ·'
            put(row_field, bx, c_red('│') + c_amber(f'  CODE   {dots}'[:bw - 2].ljust(bw - 2)) + c_red('│'))

        def _msg(text='', col=None):
            if col is None:
                col = c_bright
            line = f'  {text}' if text else ''
            put(row_msg, bx, c_red('│') + (col(line[:bw - 2].ljust(bw - 2)) if line else ' ' * (bw - 2)) + c_red('│'))

        _field()
        _msg()

        while True:
            if msg and time.time() >= msg_until:
                msg = ''
                _msg()

            key = term.inkey(timeout=0.1)
            if not key:
                continue

            if is_esc(key):
                sys.exit(0)

            if is_enter(key):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    _msg('ACCESS GRANTED', col=c_green)
                    time.sleep(0.7)
                    return True
                _msg('ACCESS DENIED  —  initiating brute-force...', col=c_bright)
                time.sleep(1.2)
                typed.clear()
                _field()
                _msg('[ W ] wait for MAGI decrypt   [ R ] retry code', col=c_amber)
                while True:
                    k2 = term.inkey(timeout=0.2)
                    if not k2:
                        continue
                    ch2 = key_char(k2)
                    if ch2 and ch2.lower() == 'w':
                        return draw_brute_force()
                    if ch2 and ch2.lower() == 'r':
                        _msg()
                        break
                    if is_esc(k2):
                        sys.exit(0)
                continue

            if is_backspace(key):
                if typed:
                    typed.pop()
                    _field()
                continue

            ch = key_char(key)
            if ch and ch.isalnum() and len(typed) < 5:
                typed.append(ch.upper())
                _field()

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2b — MAGI BRUTE-FORCE COUNTDOWN
# ─────────────────────────────────────────────────────────────────────────────
BRUTE_PHASES = [
    ('CASPAR  ── INITIALISING KEY SEARCH', 0.00, 0.12),
    ('CASPAR  ── DICTIONARY LAYER I', 0.12, 0.22),
    ('BALTHASAR ─ PARALLEL HASH EXPANSION', 0.22, 0.35),
    ('BALTHASAR ─ ENTROPY ANALYSIS', 0.35, 0.47),
    ('MELCHIOR ── NEURAL PATTERN MATCH', 0.47, 0.60),
    ('MELCHIOR ── DEEP CIPHER TRAVERSAL', 0.60, 0.72),
    ('MAGI CORE  ─ COLLATION', 0.72, 0.83),
    ('MAGI CORE  ─ FINAL BRUTE PASS', 0.83, 0.96),
    ('MAGI CORE  ─ UNLOCKING…', 0.96, 1.00),
]

HEX_CHARS = '0123456789ABCDEF'

def _rand_hex(n=32):
    return ' '.join(''.join(random.choices(HEX_CHARS, k=4)) for _ in range(max(1, n // 4)))

def _prog_bar(pct, width, col_fill=None, col_empty=None):
    filled = int(width * pct)
    f = (col_fill or c_green)('█' * filled)
    e = (col_empty or c_dim)('░' * max(0, width - filled))
    return f + e

def draw_brute_force():
    total = BRUTE_SECONDS
    start_ts = time.time()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        h, w = term.height, term.width
        print(term.clear)

        for row in range(h):
            put(row, 0, c_dred('░' * w))

        bw = min(w, 72)
        bx = (w - bw) // 2
        by = 1
        bh = min(h - 2, 28)

        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by, bx, c_red(box_top(bw)))
        put(by + 1, bx, c_red('│') + c_bright('  MAGI SYSTEM  —  MANUAL DECRYPTION ENGAGED'.ljust(bw - 2)) + c_red('│'))
        put(by + 2, bx, c_red(box_sep(bw)))
        put(by + 3, bx, c_red('│') + c_muted('  Authentication failed. Running brute-force key recovery.'.ljust(bw - 2)) + c_red('│'))
        put(by + 4, bx, c_red('│') + c_muted('  Do not close this terminal. Process cannot be paused.'.ljust(bw - 2)) + c_red('│'))
        put(by + 5, bx, c_red(box_sep(bw)))
        put(by + 8, bx, c_red(box_sep(bw)))
        put(by + 11, bx, c_red(box_sep(bw)))
        put(by + 18, bx, c_red(box_sep(bw)))
        put(by + 22, bx, c_red(box_sep(bw)))
        put(by + 25, bx, c_red(box_sep(bw)))
        put(by + 26, bx, c_red('│') + c_muted('  [ ESC ] abort'.ljust(bw - 2)) + c_red('│'))
        put(by + 27, bx, c_red(box_bot(bw)))

        R_OVERALL_BAR = by + 6
        R_OVERALL_PCT = by + 7
        R_PHASE_LBL = by + 9
        R_PHASE_BAR = by + 10
        R_HEX_START = by + 12
        R_CASPAR = by + 19
        R_BALTHASAR = by + 20
        R_MELCHIOR = by + 21
        R_CLOCK = by + 23
        R_TICKER = by + 24

        bar_w = max(10, bw - 14)

        def _vote(pct):
            if pct < 0.33:
                return c_bright('  CASPAR     ──  ANALYZING  ...')
            if pct < 0.50:
                return c_amber('  CASPAR     ──  PATTERN FOUND')
            return c_green('  CASPAR     ──  APPROVED')

        def _vote2(pct):
            if pct < 0.50:
                return c_bright('  BALTHASAR  ──  COMPUTING  ...')
            if pct < 0.75:
                return c_amber('  BALTHASAR  ──  CONVERGING')
            return c_green('  BALTHASAR  ──  APPROVED')

        def _vote3(pct):
            if pct < 0.72:
                return c_bright('  MELCHIOR   ──  DEEP SCAN  ...')
            if pct < 0.95:
                return c_amber('  MELCHIOR   ──  KEY MATCH')
            return c_green('  MELCHIOR   ──  APPROVED')

        hex_buf = [''] * 6
        last_sec = -1

        while True:
            key = term.inkey(timeout=0.12)
            if key and is_esc(key):
                sys.exit(0)

            now = time.time()
            elapsed = min(now - start_ts, total)
            pct = elapsed / total
            remain = max(0, total - elapsed)
            cur_sec = int(elapsed)
            if cur_sec == last_sec:
                continue
            last_sec = cur_sec

            pct_str = f'{pct * 100:5.1f}%'
            put(R_OVERALL_BAR, bx, c_red('│') + c_muted('  TOTAL  ') + _prog_bar(pct, bar_w, c_amber, c_dim) + c_muted('  ') + c_red('│'))
            mm, ss = divmod(int(remain), 60)
            eta = f'ETA  {mm:02d}:{ss:02d}'
            put(R_OVERALL_PCT, bx, c_red('│') + c_amber(f'  {pct_str}  complete     {eta}'.ljust(bw - 2)) + c_red('│'))

            phase_lbl = BRUTE_PHASES[-1][0]
            phase_pct = 1.0
            for lbl, p0, p1 in BRUTE_PHASES:
                if pct <= p1:
                    phase_lbl = lbl
                    phase_pct = max(0.0, min(1.0, (pct - p0) / max(0.001, p1 - p0)))
                    break
            put(R_PHASE_LBL, bx, c_red('│') + c_cyan(f'  {phase_lbl}'[:bw - 2].ljust(bw - 2)) + c_red('│'))
            put(R_PHASE_BAR, bx, c_red('│') + c_muted('  PHASE  ') + _prog_bar(phase_pct, bar_w, c_cyan, c_dim) + c_muted('  ') + c_red('│'))

            hex_buf = hex_buf[1:] + [_rand_hex(bw - 8)]
            for i, line in enumerate(hex_buf):
                col = c_dim if i < 4 else c_muted
                put(R_HEX_START + i, bx, c_red('│') + col(f'  {line}'[:bw - 2].ljust(bw - 2)) + c_red('│'))

            put(R_CASPAR, bx, c_red('│') + _vote(pct)[:bw - 2].ljust(bw - 2) + c_red('│'))
            put(R_BALTHASAR, bx, c_red('│') + _vote2(pct)[:bw - 2].ljust(bw - 2) + c_red('│'))
            put(R_MELCHIOR, bx, c_red('│') + _vote3(pct)[:bw - 2].ljust(bw - 2) + c_red('│'))

            tick_sym = '▊' if cur_sec % 2 == 0 else '▉'
            put(R_CLOCK, bx, c_red('│') + c_yellow(f'  {tick_sym}  TIME REMAINING   {mm:02d} min  {ss:02d} sec'.ljust(bw - 2)) + c_red('│'))

            tickers = [
                'SCANNING KEY SPACE ...',
                'TESTING PERMUTATIONS ...',
                'CROSS-REFERENCING PATTERN DB ...',
                'MAGI CONSENSUS IN PROGRESS ...',
                'DECRYPTION LAYER ACTIVE ...',
            ]
            put(R_TICKER, bx, c_red('│') + c_muted(f'  {tickers[cur_sec % len(tickers)]}'[:bw - 2].ljust(bw - 2)) + c_red('│'))

            if pct >= 1.0:
                put(R_CLOCK, bx, c_red('│') + c_green('  DECRYPTION COMPLETE  —  ACCESS GRANTED'.ljust(bw - 2)) + c_red('│'))
                time.sleep(2.0)
                return True

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 3 — FINAL SECRET PROMPT + GIF PAYLOAD
# ─────────────────────────────────────────────────────────────────────────────
def play_final_gif_payload():
    chafa = shutil.which('chafa')
    curl = shutil.which('curl')
    if not chafa or not curl:
        print(term.clear)
        print(c_bright('\n  Missing dependency. Install chafa and curl to render the terminal GIF.\n'))
        print(c_amber('  Ubuntu/Debian: sudo apt install chafa curl\n'))
        print(c_amber('  Arch: sudo pacman -S chafa curl\n'))
        print(c_amber('  macOS: brew install chafa curl\n'))
        print(c_green('  hehehehe\n'))
        return

    fd, gif_path = tempfile.mkstemp(prefix='nerv-final-', suffix='.gif')
    os.close(fd)
    try:
        subprocess.run(['curl', '-L', FINAL_GIF_URL, '-o', gif_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(term.clear)
        print(c_green('hehehehe\n'))
        width = max(40, term.width - 2)
        height = max(12, term.height - 4)
        subprocess.run([
            chafa,
            '--animate', 'on',
            '--clear',
            '--symbols', 'block+border+space',
            '--size', f'{width}x{height}',
            gif_path,
        ], check=False)
    finally:
        try:
            os.remove(gif_path)
        except OSError:
            pass


def draw_final_secret_prompt():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        bw = min(w, 72)
        bh = 12
        bx = (w - bw) // 2
        by = max(2, (h - bh) // 2)

        for row in range(h):
            put(row, 0, c_dred('░' * w))
        for row in range(bh):
            put(by + row, bx, term.on_black + ' ' * bw + term.normal)

        put(by, bx, c_red(box_top(bw)))
        put(by + 1, bx, c_red('│') + c_orange('  FINAL AUTHORIZATION LAYER'.ljust(bw - 2)) + c_red('│'))
        put(by + 2, bx, c_red(box_sep(bw)))
        put(by + 3, bx, c_red('│') + c_white('  Pilot synchronization accepted.'.ljust(bw - 2)) + c_red('│'))
        put(by + 4, bx, c_red('│') + c_muted('  A final secret message is available.'.ljust(bw - 2)) + c_red('│'))
        put(by + 5, bx, c_red(box_sep(bw)))
        put(by + 6, bx, c_red('│') + c_amber('  [ ENTER ] reveal final secret message'.ljust(bw - 2)) + c_red('│'))
        put(by + 7, bx, c_red('│') + c_muted('  [ ESC   ] abort'.ljust(bw - 2)) + c_red('│'))
        put(by + 8, bx, c_red(box_sep(bw)))
        put(by + 9, bx, c_red('│') + c_dim('  Waiting for final authorization...'.ljust(bw - 2)) + c_red('│'))
        put(by + 10, bx, c_red('│') + c_dim(''.ljust(bw - 2)) + c_red('│'))
        put(by + 11, bx, c_red(box_bot(bw)))

        while True:
            key = term.inkey(timeout=0.1)
            if not key:
                continue
            if is_esc(key):
                return False
            if is_enter(key):
                put(by + 9, bx, c_red('│') + c_green('  Launching final secret message...'.ljust(bw - 2)) + c_red('│'))
                put(by + 10, bx, c_red('│') + c_muted('  payload: terminal gif / text: hehehehe'.ljust(bw - 2)) + c_red('│'))
                time.sleep(1.0)
                break

    play_final_gif_payload()
    return True

# ─────────────────────────────────────────────────────────────────────────────
def main():
    try:
        draw_splash()
        draw_password_gate()
        draw_final_secret_prompt()
    except KeyboardInterrupt:
        pass
    finally:
        print(term.clear + term.normal)
        print(c_red('\n  [ NERV ]  Session terminated.\n'))

if __name__ == '__main__':
    main()
