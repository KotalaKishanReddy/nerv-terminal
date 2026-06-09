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

# ── Palette ──────────────────────────────────────────────────────────────────
def c_red(s):      return term.color_rgb(200, 20,  20)  + s + term.normal
def c_orange(s):   return term.color_rgb(255, 90,  0)   + s + term.normal
def c_amber(s):    return term.color_rgb(255, 165, 0)   + s + term.normal
def c_dark_red(s): return term.color_rgb(100, 0,   0)   + s + term.normal
def c_white(s):    return term.color_rgb(220, 210, 190) + s + term.normal
def c_dim(s):      return term.color_rgb(90,  80,  70)  + s + term.normal
def c_green(s):    return term.color_rgb(0,   200, 80)  + s + term.normal
def c_bright(s):   return term.color_rgb(255, 50,  50)  + s + term.normal

# ── Key helpers ───────────────────────────────────────────────────────────────
def is_space(k):  return (not k.is_sequence) and str(k) == ' '
def is_esc(k):    return k.is_sequence and k.name == 'KEY_ESCAPE'
def key_char(k):
    if not k.is_sequence and len(str(k)) == 1:
        return str(k).lower()
    return None

HEX_CHARS = "0123456789ABCDEF使徒覚醒"

def noise(w):
    return "".join(random.choice(HEX_CHARS) for _ in range(w))

# ── Shinji frames ─────────────────────────────────────────────────────────────
SHINJI = [
    [r"  .-----.",r" / o   o \\",r"|    △    |",r" \  ___  /",r"  '-----'"],
    [r"  .-----.",r" / -   - \\",r"|    △    |",r" \  ___  /",r"  '-----'"],
    [r"  .-----.",r" / _   _ \\",r"|    △    |",r" \  ___  /",r"  '-----'"],
    [r"  .-----.",r" /  o   o\\",r"|     △   |",r" \  ___  /",r"  '-----'"],
]
ANIM_SEQ = [0,0,0,0,1,0,0,0,2,0,0,0,0,3,0,0]

EVA = [
    r"    /\    ",
    r"   /  \   ",
    r"  / /\ \  ",
    r" /_/  \_\ ",
    r" | /██\ | ",
    r" |/ ██ \| ",
    r"    ██    ",
    r"   /  \   ",
]

# ── Box drawing helpers ───────────────────────────────────────────────────────
def box_top(w):    return "┌" + "─"*(w-2) + "┐"
def box_bot(w):    return "└" + "─"*(w-2) + "┘"
def box_mid(w):    return "├" + "─"*(w-2) + "┤"
def box_row(w, s): return "│" + s[:w-2].ljust(w-2) + "│"

def put(row, col, text, end=''):
    print(term.move(row, max(0, col)) + text, end=end, flush=True)

# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 1 — NERV SPLASH
# ─────────────────────────────────────────────────────────────────────────────
def draw_splash():
    fig   = Figlet(font='banner3')
    art   = fig.renderText('NERV').splitlines()
    # Trim empty lines
    art   = [l for l in art if l.strip()]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        NARROW = w < 50

        # Background noise
        for row in range(h):
            put(row, 0, c_dim(noise(w)[:w]))

        # Box
        bw = min(w - 2, 60) if not NARROW else w
        bh = h - 4
        bx = (w - bw) // 2
        by = 2

        for row in range(bh):
            put(by + row, bx, term.on_black + " " * bw + term.normal)

        put(by,          bx, c_red("█" * bw))
        put(by + bh - 1, bx, c_red("█" * bw))

        # Logo — scale down on narrow screens
        max_art_w = max(len(l) for l in art) if art else 1
        if NARROW and max_art_w > bw - 2:
            # Fallback: plain big text
            logo_lines = ["N E R V"]
        else:
            logo_lines = art

        lx = bx + max(0, (bw - max(len(l) for l in logo_lines)) // 2)
        ly = by + 2
        for i, line in enumerate(logo_lines[:bh - 8]):
            put(ly + i, lx, c_red(line[:bw]))

        # Subtitle
        sub = "GEHIRN ADVANCED RESEARCH" if not NARROW else "GEHIRN A.R."
        put(ly + len(logo_lines[:bh-8]) + 1, bx + (bw - len(sub)) // 2, c_amber(sub))

        # Info lines
        info = [
            ("CLASSIFICATION: TOP SECRET", c_white),
            ("MAGI v3.0  |  TOKYO-3 NETWORK", c_dim),
            ("⚠  UNAUTHORIZED ACCESS ⚠", c_dim),
        ]
        base = ly + len(logo_lines[:bh-8]) + 3
        for i, (txt, col) in enumerate(info):
            short = txt if len(txt) <= bw - 4 else txt[:bw-4]
            put(base + i, bx + 2, col(short))

        # Blink prompt
        prompt   = "[ SPACE ] START" if NARROW else "[ PRESS SPACE TO INITIALIZE PILOT INTERFACE ]"
        prompt_y = by + bh - 3
        prompt_x = bx + max(0, (bw - len(prompt)) // 2)
        stop_ev  = threading.Event()

        def blink():
            state = True
            while not stop_ev.is_set():
                txt = c_amber(prompt) if state else " " * len(prompt)
                put(prompt_y, prompt_x, txt)
                state = not state
                stop_ev.wait(0.55)

        t = threading.Thread(target=blink, daemon=True)
        t.start()

        while True:
            key = term.inkey(timeout=0.05)
            if not key:
                continue
            if is_space(key):
                stop_ev.set(); t.join(0.7)
                while term.inkey(timeout=0): pass
                break
            if is_esc(key):
                stop_ev.set(); sys.exit(0)


# ─────────────────────────────────────────────────────────────────────────────
# SCREEN 2 — PILOT INTERFACE  (wide ≥ 60 cols: 3-panel | narrow: stacked)
# ─────────────────────────────────────────────────────────────────────────────
PILOT_DATA = [
    ("PILOT",       "IKARI, SHINJI"),
    ("UNIT",        "EVA-01"),
    ("SYNC",        "41.3%"),
    ("A.T.FIELD",   "ACTIVE"),
    ("STATUS",      "STANDBY"),
    ("THREAT",      "ANGEL CL.4"),
]
MENU = [
    ("A", "ACTIVATE EVA"),
    ("S", "SYNC UPLINK"),
    ("D", "TACTICAL"),
    ("M", "MAGI QUERY"),
    ("Q", "EXIT"),
]
MENU_MSGS = {
    'a': ">> ACTIVATING EVA... STANDBY",
    's': ">> INITIATING SYNC UPLINK...",
    'd': ">> LOADING TACTICAL DISPLAY...",
    'm': ">> QUERYING MAGI SYSTEM...",
}


def draw_wide(h, w, frame, feedback, fb_until):
    """3-panel layout for wide terminals (≥60 cols)."""
    LW = 14    # left panel width
    RW = 14    # right panel width
    CW = w - LW - RW - 2
    PH = min(h - 4, 24)
    PY = (h - PH) // 2

    now = time.time()

    # ── Noise rows ──
    put(0,     0, c_dim(noise(w)[:w]))
    put(h - 1, 0, c_dim(noise(w)[:w]))

    # ── Left: EVA silhouette ──
    put(PY,     0, c_red(box_top(LW)))
    put(PY + 1, 0, c_red(box_row(LW, c_orange(" EVA-01"))))
    put(PY + 2, 0, c_red(box_mid(LW)))
    for i, line in enumerate(EVA[:PH - 6]):
        put(PY + 3 + i, 0, c_red("│") + c_amber(line[:LW-2].ljust(LW-2)) + c_red("│"))
    for j in range(len(EVA), PH - 6):
        put(PY + 3 + j, 0, c_red(box_row(LW, "")))
    put(PY + PH - 3, 0, c_red(box_mid(LW)))
    put(PY + PH - 2, 0, c_red("│") + c_green(" SYNC:41%" [:LW-2].ljust(LW-2)) + c_red("│"))
    put(PY + PH - 1, 0, c_red(box_bot(LW)))

    # ── Right: Shinji ──
    rx = w - RW
    sh = SHINJI[frame]
    put(PY,     rx, c_red(box_top(RW)))
    put(PY + 1, rx, c_red(box_row(RW, c_orange(" PILOT"))))
    put(PY + 2, rx, c_red(box_mid(RW)))
    for i, line in enumerate(sh[:PH - 6]):
        put(PY + 3 + i, rx, c_red("│") + c_white(line[:RW-2].ljust(RW-2)) + c_red("│"))
    for j in range(len(sh), PH - 6):
        put(PY + 3 + j, rx, c_red(box_row(RW, "")))
    put(PY + PH - 3, rx, c_red(box_mid(RW)))
    put(PY + PH - 2, rx, c_red(box_row(RW, c_amber("[CAM-01]"))))
    put(PY + PH - 1, rx, c_red(box_bot(RW)))

    # ── Center ──
    cx = LW + 1
    put(PY,     cx, c_red(box_top(CW)))
    put(PY + 1, cx, c_red(box_row(CW, c_orange(" NERV // PILOT INTERFACE v2.0"))))
    put(PY + 2, cx, c_red(box_mid(CW)))

    for i, (k, v) in enumerate(PILOT_DATA):
        row = f" {k:<10}: {v}"
        col = c_amber if i % 2 == 0 else c_white
        put(PY + 3 + i, cx, c_red("│") + col(row[:CW-2].ljust(CW-2)) + c_red("│"))

    sep = PY + 3 + len(PILOT_DATA)
    put(sep, cx, c_red(box_mid(CW)))
    put(sep + 1, cx, c_red(box_row(CW, c_orange(" COMMANDS:"))))
    for j, (key, label) in enumerate(MENU):
        put(sep + 2 + j, cx, c_red(box_row(CW, c_white(f"  [{key}] {label}"))))

    used = sep + 2 + len(MENU)
    fb   = feedback[0] if now < fb_until[0] else ""
    put(used, cx, c_red(box_row(CW, c_bright(fb) if fb else "")))
    used += 1

    bot = PY + PH - 1
    for row in range(used, bot):
        put(row, cx, c_red(box_row(CW, "")))
    put(bot, cx, c_red(box_bot(CW)))

    # Ticker
    tick = "▐▌" if int(now * 2) % 2 == 0 else "░░"
    bar  = f" MAGI ONLINE {tick}  |  THREAT: NONE  |  T+{int(now)%9999:04d}s "
    put(h - 2, 0, c_amber(bar[:w].ljust(w)))


def draw_narrow(h, w, frame, feedback, fb_until):
    """Single-column stacked layout for narrow terminals (phones)."""
    now = time.time()
    sh  = SHINJI[frame]

    # ── Header ──
    title = "NERV // PILOT INTERFACE"[:w]
    put(0, (w - len(title)) // 2, c_red(title))
    put(1, 0, c_red("─" * w))

    row = 2

    # ── Pilot data (compact 2-col) ──
    for k, v in PILOT_DATA:
        line = f"{k}:{v}"[:w].ljust(w)
        put(row, 0, c_amber(line))
        row += 1

    put(row, 0, c_dark_red("─" * w)); row += 1

    # ── Shinji (small, right-aligned) ──
    max_sh_w = max(len(l) for l in sh)
    sx = max(0, w - max_sh_w - 1)
    for i, line in enumerate(sh):
        if row + i >= h - 6:
            break
        put(row + i, sx, c_white(line[:w - sx]))
    row += len(sh) + 1

    put(row, 0, c_dark_red("─" * w)); row += 1

    # ── Menu ──
    for key, label in MENU:
        if row >= h - 3:
            break
        put(row, 0, c_white(f"[{key}] {label}"[:w]))
        row += 1

    # ── Feedback ──
    fb = feedback[0] if now < fb_until[0] else ""
    put(h - 3, 0, c_bright(fb[:w].ljust(w)))

    # ── Ticker ──
    put(h - 2, 0, c_dim("─" * w))
    tick = "▐▌" if int(now * 2) % 2 == 0 else "░░"
    bar  = f"{tick} T+{int(now)%9999:04d}s"
    put(h - 1, 0, c_amber(bar[:w].ljust(w)))


def draw_pilot_interface():
    anim_step = 0
    last_anim = time.time()
    feedback  = [""]
    fb_until  = [0.0]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)

        while True:
            h, w   = term.height, term.width
            now    = time.time()
            NARROW = w < 60

            if now - last_anim > 0.18:
                anim_step = (anim_step + 1) % len(ANIM_SEQ)
                last_anim = now
            frame = ANIM_SEQ[anim_step]

            if NARROW:
                draw_narrow(h, w, frame, feedback, fb_until)
            else:
                draw_wide(h, w, frame, feedback, fb_until)

            key = term.inkey(timeout=0.05)
            if not key:
                continue
            ch = key_char(key)

            if ch == 'q' or is_esc(key):
                break
            elif ch in MENU_MSGS:
                feedback[0] = MENU_MSGS[ch]
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
        print(c_red("\n  [NERV] Session terminated.\n"))

if __name__ == "__main__":
    main()
