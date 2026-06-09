#!/usr/bin/env python3
"""NERV Terminal — Neon Genesis Evangelion TUI"""

import sys, time, random, threading
import blessed

term = blessed.Terminal()

# ── Palette ─────────────────────────────────────────────────────────────────────────────────
def c(r,g,b):      return term.color_rgb(r,g,b)
def bg(r,g,b):     return term.on_color_rgb(r,g,b)

RED    = c(210, 20,  20)
BRTRED = c(255, 60,  60)
DKRED  = c(100,  5,   5)
ORANGE = c(255,130,   0)
AMBER  = c(240,170,   0)
YELL   = c(255,220,  80)
GREEN  = c(  0,210,  70)
DKGRN  = c(  0,100,  30)
CYAN   = c(  0,200,220)
DKCYAN = c(  0, 80, 90)
WHITE  = c(210,210,210)
LGRAY  = c(140,140,140)
MGRAY  = c( 70, 70, 70)
DGRAY  = c( 25, 25, 25)
BG_RED = bg(18,  0,  0)
RST    = term.normal
BOLD   = term.bold
DIM    = term.dim

ANGEL_ART = """⡇⡇⡷⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⢿⢿⡿⡿⡿⡿⡇⡇⡇⡇⡇⡿⠙⠉⠨⠠⢤⣴⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠛⠋⡁⢠⠤⠤⢒⢖⠦⡲⢤⡀⢌⠉⠃⠈⡈⢤⢤⢤⢤⢤⢤⢤⡀⠉⠂⠎⢏⡳⢤⢙⠋⠙⠓⠋⡿⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠛⠉⢠⢔⢎⡳⢣⢝⠎⠧⠙⡁⢡⢌⢤⢨⠁′⡃⢛⢌⢤⢲⢤⢤⢡⠒⠁⠎⢏⡳⢤⢙⠋⢸⠑⡿⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠋⡁⢴⢪⡳⠙⢶⣘⠇⠃⢠⢔⢲⢹⢲⢹⢜⢢⢏⠀⢠⢽⣘⢎⡳⢹⢦⢝⢼⢩⣓⠦⢨⠁⢯⢱⢦⢨⠉⠙⡿⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⠟⠛⢠⢴⢚⢏⠓⠦⣍⠞⠁⢤⢲⢹⢱⢎⢳⢥⢳⢱⢣⢝⠠⢏⢼⢱⢣⢎⢧⢝⢦⢝⡲⢕⢎⢲⣍⠓⢧⣈⠁
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠋⠁⢴⢫⡵⢪⡵⢚⠌⠁⢤⢎⢳⢜⠧⡳⣍⢹⢫⣓⢹⢱⢭⢣⢝⠠⢏⢼⢱⢣⢎⢧⢝⢦⢝⡲⢕⢎⢲⣍⠓⢧⣈⠁⠛⡿⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠋⢠⠞⢸⢹⡃⢛⢴⠋⢒⢏⢳⢲⢹⡲⢥⢳⢪⢳⢮⣡⠝⠠⢋⢞⢳⠦⢜⢳⢸⠠⢛⢼⢱⢣⢎⢧⢝⢦⢝⡲⢕⢎⢲⣍⠓⢧⣈⠁⠛⡿⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠃⠀⢠⢴⡳⢫⢼⢣⢳⢬⢳⢮⢥⢳⡴⢫⢜⡱⢥⢳⢪⢵⢮⢹⠁⢸⢣⠀⢠⢽⣘⢎⡳⢜⢝⢲⢭⢎⢧⢝⡶⢛⢸⢲⠦⢜⢳⢸⠠⢛⢼⢱⢣⢢⠔⡈⢫⢝⢴⢚⢣⢜⢢⠟⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇
⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡿⠃⠀⢠⢞⢱⢣⡳⢣⢬⢃⢳⢥⢳⢪⢵⢺⢲⢫⢳⢬⢵⢲⢹⢳⢮⢳⠠⢜⡲⢑⢳⢆⢵⢬⢳⢪⢕⢾⢳⢮⢳⠦⢜⢳⢸⠠⢛⢼⢱⢣⢢⠔⡈⢫⢝⢴⢚⢣⢜⢢⠟⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇⡇""".strip().split("\n")

ART_LINES = ANGEL_ART
_blink_on = True
_running  = True
_scroll_off = 0

def blink_thread():
    global _blink_on
    while _running:
        _blink_on = not _blink_on
        time.sleep(0.5)

def scroll_thread():
    global _scroll_off
    while _running:
        _scroll_off = (_scroll_off + 1) % max(1, len(ART_LINES))
        time.sleep(0.06)

def cprint(row, col, text, flush=False):
    print(term.move_xy(col, row) + text, end="", flush=flush)

def fill_row(row, ch="─", col=None, width=None):
    w = width or term.width
    c2 = col or ""
    print(term.move_xy(0, row) + c2 + ch * w + RST, end="")

def nerv_header(row):
    W = term.width
    fill_row(row, "▀", RED, W)
    title = " ▌ NERV ▐ 特務機関ネルフ ▌ TACTICAL COMMAND INTERFACE "
    ts = time.strftime('%H:%M:%S')
    pad = " " * max(0, W - len(title) - len(ts) - 2)
    cprint(row, 0, BOLD + AMBER + title + pad + RED + ts + " " + RST)
    fill_row(row+1, "▄", DKRED, W)

def nerv_footer(row):
    W = term.width
    fill_row(row, "─", DKRED, W)
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    alerts = ["AT-FIELD:NOMINAL","ANGEL-THREAT:NONE","LCL:100%","SYNC:41.3%","MAGI:ONLINE"]
    tick = " ◈ ".join(alerts)
    tick = (tick * 4)[:W-20]
    cprint(row+1, 0, DKRED + "■" + CYAN + tick + LGRAY + f" [{now}]" + RST)

NERV_BLOCK = [
" ███╗   ██╗███████╗██████╗ ██╗   ██╗",
" ████╗  ██║██╔════╝██╔══██╗██║   ██║",
" ██╔██╗ ██║█████╗  ██████╔╝██║   ██║",
" ██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝",
" ██║ ╚████║███████╗██║  ██║ ╚████╔╝ ",
" ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝ ",
]

def draw_splash():
    W, H = term.width, term.height
    print(term.clear, end="")
    art_flat = "".join(ART_LINES)
    art_chars = [ch for ch in art_flat if ch not in (' ', '\n')]
    for r in range(2, H-3):
        row_str = ""
        for _ in range(W):
            if random.random() < 0.08 and art_chars:
                row_str += DKRED + random.choice(art_chars[:200])
            else:
                row_str += DGRAY + "\u00b7"
        cprint(r, 0, row_str + RST)
    nerv_header(0)
    nerv_footer(H-3)
    logo_w = max(len(l) for l in NERV_BLOCK) + 6
    logo_h = len(NERV_BLOCK) + 8
    lx = (W - logo_w) // 2
    ly = (H - logo_h) // 2
    cprint(ly,   lx, RED + "◄" + AMBER + "━"*(logo_w-2) + RED + "►" + RST)
    cprint(ly+1, lx, RED + "▌" + DKRED + "  NERV  MAGI SYSTEM v3.0  TOKYO-3  " + RED + "▌" + RST)
    cprint(ly+2, lx, RED + "◄" + DKRED + "─"*(logo_w-2) + RED + "►" + RST)
    for i, line in enumerate(NERV_BLOCK):
        pad = (logo_w - len(line) - 2) // 2
        cprint(ly+3+i, lx, RED+"▌"+BOLD+BRTRED+" "*pad+line+" "*pad+RST+RED+"▌"+RST)
    cprint(ly+3+len(NERV_BLOCK),   lx, RED+"◄"+DKRED+"─"*(logo_w-2)+RED+"►"+RST)
    cprint(ly+3+len(NERV_BLOCK)+1, lx, RED+"▌"+CYAN+" ◈ GEHIRN PROJECT  ◈  CLASSIFIED LEVEL AAA  ◈ "+RED+"▌"+RST)
    cprint(ly+3+len(NERV_BLOCK)+2, lx, RED+"◄"+AMBER+"━"*(logo_w-2)+RED+"►"+RST)
    return ly + logo_h + 1

def update_splash_prompt(prompt_row):
    W = term.width
    prompt = "▌▌  PRESS  SPACE  TO  INITIALIZE  PILOT  INTERFACE  ▌▌"
    col = (W - len(prompt)) // 2
    vis = AMBER + BOLD if _blink_on else DKRED + DIM
    cprint(prompt_row, col, vis + prompt + RST, flush=True)
    hexline = "  ".join(f"{random.randint(0,0xFFFF):04X}" for _ in range(8))
    cprint(prompt_row+2, (W-len(hexline))//2, DKGRN + hexline + RST, flush=True)

ART_COLOR_MAP = [RED, DKRED, BRTRED, ORANGE, AMBER]

def art_line_color(i):
    return ART_COLOR_MAP[i % len(ART_COLOR_MAP)]

def draw_pilot():
    W, H = term.width, term.height
    print(term.clear, end="")
    nerv_header(0)
    nerv_footer(H-3)
    art_col_w = min(55, W // 2)
    ax = W - art_col_w
    cprint(2, ax, RED+"◄"+AMBER+"━"*(art_col_w-2)+RED+"►"+RST)
    cprint(3, ax, RED+"▌"+CYAN+(" EVANGELION — ANGEL PATTERN DETECTED ").center(art_col_w-2)+RED+"▌"+RST)
    cprint(4, ax, RED+"◄"+DKRED+"─"*(art_col_w-2)+RED+"►"+RST)
    art_rows = H - 10
    for i in range(art_rows):
        idx = (_scroll_off + i) % len(ART_LINES)
        line = ART_LINES[idx]
        visible = line[:art_col_w-2]
        pad = max(0, art_col_w-2-len(visible))
        col = art_line_color(i)
        cprint(5+i, ax, RED+"▌"+ col + visible + " "*pad + RED+"▌"+RST)
    lx = 0
    lw = ax - 2
    cprint(2, lx, RED+"◄"+AMBER+"━"*(lw-2)+RED+"►"+RST)
    cprint(3, lx, RED+"▌"+CYAN+(" NERV PILOT COMMAND INTERFACE ").center(lw-2)+RED+"▌"+RST)
    cprint(4, lx, RED+"◄"+DKRED+"─"*(lw-2)+RED+"►"+RST)
    sync = 41.3
    bar_w = 20
    filled = int(bar_w * sync / 100)
    bar = GREEN + "█" * filled + DKGRN + "░" * (bar_w - filled) + RST
    pilot_info = [
        (AMBER+BOLD+" PILOT: IKARI SHINJI "+RST,""),
        (CYAN+" DESIGNATION: "+WHITE+"THIRD CHILD"+RST,""),
        (CYAN+" UNIT: "+WHITE+"EVA-01"+RST,""),
        (CYAN+" SYNC RATIO: "+f"{sync:.1f}%  "+bar,""),
        (CYAN+" LCL STATUS: "+GREEN+"NOMINAL"+RST,""),
        (CYAN+" AT-FIELD: "+AMBER+"ACTIVE"+RST,""),
        ("",""),
        (RED+" ◈ TACTICAL MENU ◈"+RST,""),
        (DKRED+"─"*(lw-4),""),
        (WHITE+" [A] "+CYAN+"ACTIVATE EVA"+RST,""),
        (WHITE+" [S] "+CYAN+"MAGI QUERY"+RST,""),
        (WHITE+" [D] "+CYAN+"ANGEL RADAR"+RST,""),
        (WHITE+" [M] "+CYAN+"MISSION LOG"+RST,""),
        (WHITE+" [Q] "+RED+"TERMINATE SESSION"+RST,""),
    ]
    for i, (line, _) in enumerate(pilot_info):
        cprint(5+i, lx+2, line)

def main():
    global _running
    _running = True
    bt = threading.Thread(target=blink_thread, daemon=True)
    st = threading.Thread(target=scroll_thread, daemon=True)
    bt.start()
    st.start()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        screen = "splash"
        prompt_row = draw_splash()
        last_redraw = time.time()
        while True:
            now = time.time()
            key = term.inkey(timeout=0.08)
            if screen == "splash":
                if str(key) == " ":
                    screen = "pilot"
                    draw_pilot()
                    last_redraw = now
                elif now - last_redraw > 0.5:
                    update_splash_prompt(prompt_row)
                    nerv_header(0)
                    nerv_footer(term.height-3)
                    last_redraw = now
            elif screen == "pilot":
                if key.lower() == "q" or key.name == "KEY_ESCAPE":
                    break
                elif now - last_redraw > 0.08:
                    draw_pilot()
                    last_redraw = now
    _running = False
    print(term.clear + term.move_xy(0,0))

if __name__ == "__main__":
    main()
