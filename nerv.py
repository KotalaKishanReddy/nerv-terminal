#!/usr/bin/env python3
"""
NERV Terminal — Neon Genesis Evangelion themed terminal launcher
Usage: python nerv.py

Dependencies: blessed, pyfiglet
  pip install -r requirements.txt
"""

import sys
import time
import random
import threading
from blessed import Terminal
from pyfiglet import Figlet

term = Terminal()

# ─── EVA Color Palette ───────────────────────────────────────────────────────
def orange(s):    return term.color_rgb(255, 90, 0)    + s + term.normal
def red(s):       return term.color_rgb(200, 20, 20)   + s + term.normal
def amber(s):     return term.color_rgb(255, 165, 0)   + s + term.normal
def dark_red(s):  return term.color_rgb(120, 0, 0)     + s + term.normal
def white(s):     return term.color_rgb(220, 210, 190) + s + term.normal
def dim_white(s): return term.color_rgb(120, 110, 100) + s + term.normal
def bright_red(s):return term.color_rgb(255, 50, 50)   + s + term.normal
def green(s):     return term.color_rgb(0, 200, 80)    + s + term.normal

# ─── Key helpers ─────────────────────────────────────────────────────────────
def is_space(key):
    """Reliable spacebar detection across terminals."""
    return (not key.is_sequence) and str(key) == ' '

def is_escape(key):
    return key.is_sequence and key.name == 'KEY_ESCAPE'

def key_char(key):
    """Return lowercase char only for plain (non-sequence) keystrokes."""
    if not key.is_sequence and len(str(key)) == 1:
        return str(key).lower()
    return None

# ─── Scanline / Background noise ─────────────────────────────────────────────
HEX_CHARS = "0123456789ABCDEF神使徒覚醒警戒"

def random_hex_line(width):
    return "".join(random.choice(HEX_CHARS) for _ in range(width))

# ─── Shinji ASCII art frames (right-side panel, animated) ────────────────────
SHINJI_FRAMES = [
    # Frame 0 — neutral
    [
        r"   .-----.",
        r"  /  o o  \\",
        r" |    △    |",
        r"  \  ___  /",
        r"   '-----'",
        r"   |NERV |",
        r"   | uni |",
        r"  /|     |\\",
        r" / |     | \\",
        r"   | LEG |",
        r"   |_____|",
    ],
    # Frame 1 — slight tilt
    [
        r"   .-----.",
        r"  /  - -  \\",
        r" |    △    |",
        r"  \  ___  /",
        r"   '-----'",
        r"   |NERV |",
        r"   | uni |",
        r"  /|     |\\",
        r" / |     | \\",
        r"   | LEG |",
        r"   |_____|",
    ],
    # Frame 2 — blink
    [
        r"   .-----.",
        r"  /  _ _  \\",
        r" |    △    |",
        r"  \  ___  /",
        r"   '-----'",
        r"   |NERV |",
        r"   | uni |",
        r"  /|     |\\",
        r" / |     | \\",
        r"   | LEG |",
        r"   |_____|",
    ],
    # Frame 3 — look right
    [
        r"   .-----.",
        r"  /   o o \\",
        r" |     △   |",
        r"  \  ___  /",
        r"   '-----'",
        r"   |NERV |",
        r"   | uni |",
        r"  /|     |\\",
        r" / |     | \\",
        r"   | LEG |",
        r"   |_____|",
    ],
]

# EVA Unit-01 silhouette (left panel)
EVA_SILHOUETTE = [
    r"      /\      ",
    r"     /  \     ",
    r"    / /\ \    ",
    r"   / /  \ \   ",
    r"  /_/ /\ \_\  ",
    r"  |  /  \  |  ",
    r"  | / ██ \ |  ",
    r"  |/  ██  \|  ",
    r"  |   ██   |  ",
    r"  |  /  \  |  ",
    r" /| /    \ |\ ",
    r"/_|/      \|_\\",
]


# ─── Screen 1: NERV Splash ────────────────────────────────────────────────────
def draw_splash():
    fig = Figlet(font='banner3')
    nerv_art = fig.renderText('NERV').splitlines()

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width

        # Draw scanline background
        for row in range(h):
            noise = dim_white(random_hex_line(w)[:w])
            print(term.move(row, 0) + noise, end='', flush=True)

        # Black center box
        box_h, box_w = h - 6, min(w - 4, 80)
        box_x = (w - box_w) // 2
        box_y = 2

        for row in range(box_h):
            print(term.move(box_y + row, box_x) + term.on_black + " " * box_w + term.normal, end='', flush=True)

        # Box borders
        border_line = "█" * box_w
        print(term.move(box_y,             box_x) + red(border_line), end='', flush=True)
        print(term.move(box_y + box_h - 1, box_x) + red(border_line), end='', flush=True)

        # NERV ASCII logo
        art_start_y = box_y + 2
        art_start_x = box_x + (box_w - max(len(l) for l in nerv_art)) // 2
        for i, line in enumerate(nerv_art[:8]):
            print(term.move(art_start_y + i, max(0, art_start_x)) + red(line[:box_w]), end='', flush=True)

        # Subtitle
        subtitle = "GEHIRN ADVANCED RESEARCH"
        print(term.move(art_start_y + 9, box_x + (box_w - len(subtitle)) // 2)
              + amber(subtitle), end='', flush=True)

        # Divider
        divider = "─" * (box_w - 4)
        print(term.move(art_start_y + 11, box_x + 2) + dark_red(divider), end='', flush=True)

        # Classification info
        lines_info = [
            white("  CLASSIFICATION: TOP SECRET // NERV EYES ONLY"),
            dim_white("  MAGI SYSTEM v3.0  |  TOKYO-3 TACTICAL NETWORK"),
            dim_white("  \u26a0  UNAUTHORIZED ACCESS WILL BE PROSECUTED  \u26a0"),
        ]
        for i, line in enumerate(lines_info):
            print(term.move(art_start_y + 13 + i, box_x + 2) + line, end='', flush=True)

        # Blinking SPACE prompt
        prompt   = "[ PRESS SPACE TO INITIALIZE PILOT INTERFACE ]"
        prompt_y = box_y + box_h - 4
        prompt_x = box_x + (box_w - len(prompt)) // 2

        stop_blink = threading.Event()

        def blink_loop():
            state = True
            while not stop_blink.is_set():
                txt = amber(prompt) if state else " " * len(prompt)
                print(term.move(prompt_y, prompt_x) + txt, end='', flush=True)
                state = not state
                stop_blink.wait(timeout=0.55)

        t = threading.Thread(target=blink_loop, daemon=True)
        t.start()

        # ── Key loop: wait for SPACE ──────────────────────────────────────
        while True:
            key = term.inkey(timeout=0.05)
            if not key:
                continue
            if is_space(key):
                stop_blink.set()
                t.join(timeout=0.7)
                # Drain any queued input before transitioning
                while term.inkey(timeout=0):
                    pass
                break
            if is_escape(key):
                stop_blink.set()
                sys.exit(0)


# ─── Screen 2: Pilot Interface ────────────────────────────────────────────────
def draw_pilot_interface():
    frame_idx   = 0
    anim_frames = [0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0]
    anim_step   = 0
    last_anim   = time.time()

    pilot_data = [
        ("PILOT",        "IKARI, SHINJI"),
        ("UNIT",         "EVA-01 [PURPLE]"),
        ("SYNC RATIO",   "41.3%"),
        ("A.T. FIELD",   "ACTIVE"),
        ("STATUS",       "STANDBY"),
        ("THREAT LEVEL", "ANGEL — CLASS 4"),
    ]

    menu_items = [
        "[ A ]  ACTIVATE EVA UNIT",
        "[ S ]  SYNC UPLINK",
        "[ D ]  TACTICAL DISPLAY",
        "[ M ]  MAGI QUERY",
        "[ Q ]  ABORT / EXIT",
    ]

    # Feedback message shown in the center panel
    feedback      = [""]
    feedback_until = [0.0]

    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)

        while True:
            h, w = term.height, term.width
            now  = time.time()

            # ── Animation frame advance ───────────────────────────────────
            if now - last_anim > 0.18:
                anim_step = (anim_step + 1) % len(anim_frames)
                frame_idx = anim_frames[anim_step]
                last_anim = now

            # ── Background noise strips ───────────────────────────────────
            for row in [0, h - 1]:
                print(term.move(row, 0) + dim_white(random_hex_line(w)[:w]), end='', flush=True)

            # ── Left panel: EVA silhouette ────────────────────────────────
            panel_l_w = 18
            panel_h   = min(h - 2, 22)
            panel_y   = (h - panel_h) // 2

            print(term.move(panel_y,     0) + red("┌" + "─" * (panel_l_w - 2) + "┐"), end='', flush=True)
            print(term.move(panel_y + 1, 0) + red("│") + orange(" EVA-01 STATUS ") + red("│"), end='', flush=True)
            print(term.move(panel_y + 2, 0) + red("├" + "─" * (panel_l_w - 2) + "┤"), end='', flush=True)

            for i, line in enumerate(EVA_SILHOUETTE[:panel_h - 7]):
                padded = line.ljust(panel_l_w - 2)[:panel_l_w - 2]
                print(term.move(panel_y + 3 + i, 0) + red("│") + amber(padded) + red("│"), end='', flush=True)
            for j in range(len(EVA_SILHOUETTE), panel_h - 7):
                print(term.move(panel_y + 3 + j, 0) + red("│" + " " * (panel_l_w - 2) + "│"), end='', flush=True)

            print(term.move(panel_y + panel_h - 4, 0) + red("├" + "─" * (panel_l_w - 2) + "┤"), end='', flush=True)
            sync = "SYNC: 41.3%"
            print(term.move(panel_y + panel_h - 3, 0) + red("│") + green(f" {sync:<{panel_l_w-3}}") + red("│"), end='', flush=True)
            print(term.move(panel_y + panel_h - 2, 0) + red("│") + bright_red(f" ██████░░░░{' ' * (panel_l_w - 13)}") + red("│"), end='', flush=True)
            print(term.move(panel_y + panel_h - 1, 0) + red("└" + "─" * (panel_l_w - 2) + "┘"), end='', flush=True)

            # ── Right panel: Animated Shinji ──────────────────────────────
            panel_r_w = 18
            panel_r_x = w - panel_r_w
            shinji    = SHINJI_FRAMES[frame_idx]

            print(term.move(panel_y,     panel_r_x) + red("┌" + "─" * (panel_r_w - 2) + "┐"), end='', flush=True)
            print(term.move(panel_y + 1, panel_r_x) + red("│") + orange("  PILOT FEED   ") + red("│"), end='', flush=True)
            print(term.move(panel_y + 2, panel_r_x) + red("├" + "─" * (panel_r_w - 2) + "┤"), end='', flush=True)

            for i, line in enumerate(shinji[:panel_h - 6]):
                padded = line.ljust(panel_r_w - 2)[:panel_r_w - 2]
                print(term.move(panel_y + 3 + i, panel_r_x) + red("│") + white(padded) + red("│"), end='', flush=True)
            for j in range(len(shinji), panel_h - 6):
                print(term.move(panel_y + 3 + j, panel_r_x) + red("│" + " " * (panel_r_w - 2) + "│"), end='', flush=True)

            print(term.move(panel_y + panel_h - 3, panel_r_x) + red("├" + "─" * (panel_r_w - 2) + "┤"), end='', flush=True)
            cam_label = " [CAM 01-LIVE] "
            print(term.move(panel_y + panel_h - 2, panel_r_x) + red("│") + amber(cam_label[:panel_r_w-2].ljust(panel_r_w-2)) + red("│"), end='', flush=True)
            print(term.move(panel_y + panel_h - 1, panel_r_x) + red("└" + "─" * (panel_r_w - 2) + "┘"), end='', flush=True)

            # ── Center panel ──────────────────────────────────────────────
            cx    = panel_l_w + 1
            cw    = w - panel_l_w - panel_r_w - 2
            cy    = panel_y
            title = "NERV // PILOT INTERFACE v2.0"

            print(term.move(cy,     cx) + red("┌" + "─" * (cw - 2) + "┐"), end='', flush=True)
            print(term.move(cy + 1, cx) + red("│") + orange(f" {title:<{cw-3}}") + red("│"), end='', flush=True)
            print(term.move(cy + 2, cx) + red("├" + "─" * (cw - 2) + "┤"), end='', flush=True)

            for i, (k, v) in enumerate(pilot_data):
                row_str = f" {k:<14}: {v}"
                row_str = row_str[:cw - 2].ljust(cw - 2)
                color   = amber if i % 2 == 0 else white
                print(term.move(cy + 3 + i, cx) + red("│") + color(row_str) + red("│"), end='', flush=True)

            print(term.move(cy + 3 + len(pilot_data), cx) + red("├" + "─" * (cw - 2) + "┤"), end='', flush=True)

            menu_y     = cy + 4 + len(pilot_data)
            menu_title = " COMMAND INTERFACE:"
            print(term.move(menu_y, cx) + red("│") + orange(menu_title.ljust(cw - 2)) + red("│"), end='', flush=True)

            for j, item in enumerate(menu_items):
                item_str = f"  {item}".ljust(cw - 2)[:cw - 2]
                print(term.move(menu_y + 1 + j, cx) + red("│") + white(item_str) + red("│"), end='', flush=True)

            used = menu_y + 1 + len(menu_items)
            bot  = panel_y + panel_h - 1

            # Feedback row
            fb_text = feedback[0] if now < feedback_until[0] else ""
            fb_str  = fb_text[:cw - 2].ljust(cw - 2)
            fb_color = bright_red if fb_text else lambda s: s
            if used < bot:
                print(term.move(used, cx) + red("│") + fb_color(fb_str) + red("│"), end='', flush=True)
                used += 1

            for row in range(used, bot):
                print(term.move(row, cx) + red("│") + " " * (cw - 2) + red("│"), end='', flush=True)

            print(term.move(bot, cx) + red("└" + "─" * (cw - 2) + "┘"), end='', flush=True)

            # Bottom ticker
            tick   = "▐▌" if int(now * 2) % 2 == 0 else "░░"
            status = f" MAGI ONLINE {tick}  |  ANGEL ALERT: NONE  |  T+{int(now) % 9999:04d}s "
            print(term.move(h - 2, 0) + amber(status[:w].ljust(w)), end='', flush=True)

            # ── Key handling ──────────────────────────────────────────────
            key = term.inkey(timeout=0.05)
            if not key:
                continue

            ch = key_char(key)  # None for sequences, lowercase char for plain keys

            if ch == 'q' or is_escape(key):
                break
            elif ch in ('a', 's', 'd', 'm'):
                msgs = {
                    'a': "  >> ACTIVATING EVA UNIT... STANDBY",
                    's': "  >> INITIATING SYNC UPLINK...",
                    'd': "  >> LOADING TACTICAL DISPLAY...",
                    'm': "  >> QUERYING MAGI SYSTEM...",
                }
                feedback[0]       = msgs[ch]
                feedback_until[0] = now + 2.0


# ─── Entry point ─────────────────────────────────────────────────────────────
def main():
    try:
        draw_splash()
        draw_pilot_interface()
    except KeyboardInterrupt:
        pass
    finally:
        print(term.clear + term.normal)
        print(term.color_rgb(200, 20, 20) + "\n  [NERV] Session terminated.\n" + term.normal)

if __name__ == "__main__":
    main()
