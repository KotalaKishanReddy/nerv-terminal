#!/usr/bin/env python3
"""
NERV Terminal
Dependencies: blessed
"""

import sys
import time
import random
import threading
import subprocess
from blessed import Terminal

term = Terminal()

def c_red(s):    return term.color_rgb(210, 25,  25)  + s + term.normal
def c_orange(s): return term.color_rgb(255, 100, 10)  + s + term.normal
def c_amber(s):  return term.color_rgb(255, 170, 0)   + s + term.normal
def c_dred(s):   return term.color_rgb(80,  0,   0)   + s + term.normal
def c_bg(s):     return term.on_color_rgb(15, 0, 0)   + s + term.normal
def c_white(s):  return term.color_rgb(225, 215, 195) + s + term.normal
def c_dim(s):    return term.color_rgb(75,  65,  55)  + s + term.normal
def c_green(s):  return term.color_rgb(0,   210, 90)  + s + term.normal
def c_bright(s): return term.color_rgb(255, 60,  60)  + s + term.normal
def c_muted(s):  return term.color_rgb(140, 120, 100) + s + term.normal
def c_cyan(s):   return term.color_rgb(0,   200, 220) + s + term.normal
def c_yellow(s): return term.color_rgb(240, 230, 50)  + s + term.normal

ACCESS_CODE   = "NERV0"
BRUTE_SECONDS = 10 * 60
FINAL_COMMAND = "curl -s -L https://bit.ly/3zvELNz | bash"
LOREM_IPSUM = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor "
    "incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud "
    "exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."
)

NERV_LOGO = [
    "███╗   ██╗███████╗██████╗ ██╗   ██╗",
    "████╗  ██║██╔════╝██╔══██╗██║   ██║",
    "██╔██╗ ██║█████╗  ██████╔╝██║   ██║",
    "██║╚██╗██║██╔══╝  ██╔══██╗╚██╗ ██╔╝",
    "██║ ╚████║███████╗██║  ██║ ╚████╔╝ ",
    "╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝  ╚═══╝  ",
]

# Left panel art (Shinji/EVA high-res braille, 60 cols x 34 rows)
LEFT_ART = [
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣷⣿⣷⣷⣯⣿⣿⣷⣷⣷⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣷⣛⣻⣭⣵⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣛⣶⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣋⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣯⣻⣿⣿⣿⣿⣿⣿⣷⢿⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣯⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣬⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣭",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣟⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣿⣿⣿⣿⣿⣿⣿",
]

# Right panel EVA-01 art
EVA_ART = [
    "⣿⣿⣿⢟⣿⢟⣵⣾⣿⣿⠟⢋⣤⣶⠟⢉⣠⣴⠚⠟⠛⢿⣿⣿⣿⣿⣿⣿⣷⣮⡙⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡉⢻⣿⣿⣿⣿⣿",
    "⣿⡿⠣⠋⣠⡿⣻⡿⣋⣵⢾⣿⠟⣡⡾⣹⡿⣣⣴⣿⣷⣤⡙⢿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠈⠻⠿⣿⣿⣿⣿⣿⣿⣷⣽⣷⣝⢿⣿⣿⣿",
    "⣿⠁⣠⣾⣯⣾⣿⣿⢟⣵⣿⣫⣾⣿⢣⣿⣿⡿⣿⡿⣿⣿⣿⣮⠻⣿⣿⣿⣿⣿⣿⡝⠿⣷⡄⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⢿⣷⣽⢿⣿",
    "⠃⣼⣿⣿⣿⣿⠟⡡⠟⣻⡍⡽⢫⠇⣿⣿⠟⢸⣿⣧⢸⣿⣿⣿⣷⡙⣿⣿⣿⣿⡇⣿⣷⣶⡿⠲⠷⡄⠙⣿⣿⣿⣿⣿⣿⣎⢿⣿⣧⡙",
    "⣾⣿⣿⣿⡿⢋⣴⡧⢸⡟⢁⣴⣿⢸⣿⡟⣼⣿⣿⣿⣄⢻⣿⣿⣿⣷⣌⢿⣿⣿⣷⢹⣿⡏⢠⣾⣷⣌⠀⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣯⣾⣿⡋⢡⠞⣴⣿⣿⡇⣾⣿⣰⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣎⢻⣿⣿⣧⠻⣿⣆⢨⡛⢿⣷⣌⢻⣿⡆⢿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⠟⣴⢋⣼⢻⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣆⢻⣿⣿⣷⡙⢿⣦⠻⣦⡙⠛⠁⢹⣿⠸⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⠀⢡⣾⣿⢸⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣿⣧⢻⣿⣿⣿⣿⣿⣿⡏⢿⣿⠹⣿⣎⠻⠇⢸⣿⣧⣀⡄⣿⡇⣿⣿⣿⣿⣿⣿",
    "⣿⣿⡌⣿⠟⣠⣿⣿⣿⢸⣿⡟⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⡎⣿⣿⣿⣿⣿⣿⡇⢸⣿⢀⢻⣿⣷⡤⡘⠿⢿⣽⠇⣿⡇⣿⣿⢻⣿⣿⣿",
    "⣿⣿⣿⣄⠰⢿⣿⣿⣿⠈⣿⡇⠀⠀⢿⡝⣿⣿⢿⣿⣿⣿⣿⡘⣿⣿⣿⢸⣿⠃⢸⡟⣸⡆⠻⣿⣧⢹⡷⣶⣤⣾⣿⡇⣿⣿⣠⡹⣿⣿",
    "⢸⣿⠛⣿⣆⠈⢿⣿⣿⠀⢻⡇⠀⣄⠘⣷⡘⣿⣆⢿⣿⣿⣿⣷⠹⣿⣿⠘⡏⣸⢸⠇⣿⣿⣆⠹⣿⠀⠃⢻⣿⣿⣿⡇⢹⡇⣿⣧⠹⣿",
    "⡆⢿⠀⠘⢿⣆⠈⢿⣿⡆⠈⡇⠀⢹⣆⠘⢧⠘⣿⣎⢻⣿⢿⣿⣇⢹⣿⡆⢰⡿⠀⠘⢟⣛⣋⡀⢸⠄⠀⠸⣿⣿⣿⡇⢸⢣⣿⡿⢰⣿",
    "⣧⠘⣿⡇⠈⠻⡄⠈⠻⣷⠀⠀⠀⠶⢤⡄⢈⠀⠸⣿⡆⠙⠎⢻⣿⡆⢩⡄⣴⠆⠀⠚⠋⠉⠉⠉⠀⠀⠶⠀⢻⣿⣿⡇⠊⣼⣿⠇⢸⣿",
    "⣿⣆⢹⡇⣄⠀⣑⡀⠀⠈⠁⠀⢀⣴⡤⠄⠀⠀⠀⠘⣷⠀⠀⠀⠙⢿⡄⠃⣧⠀⣠⣶⡋⠁⠀⠀⢠⣄⢸⡆⠘⣿⣿⠁⢰⢏⡏⢸⣿⠟",
    "⣿⣿⣆⠃⢻⣧⠈⢿⣦⡀⠀⢀⠸⣿⣷⡄⠀⠀⢀⣄⠈⠃⢰⡄⠠⣄⠁⠀⢻⣾⣿⣿⣷⣤⣤⣴⣾⣿⡟⠀⠀⢿⡟⠀⣠⡞⠀⣼⠁⣼",
    "⣿⣿⣿⣦⠘⣿⠀⡈⠻⡿⠆⠀⠀⠺⣿⣷⣾⣿⣿⣿⣷⠀⠀⢻⣦⣙⣧⡀⠀⠻⣿⣿⣿⣿⣿⣿⡿⠋⠔⢁⠀⢸⠃⣴⠋⠀⠀⢡⣾⣿",
    "⣿⣿⣿⣿⣷⣿⠀⠛⠢⣴⣤⡀⠀⠀⠀⠈⢽⣿⣿⣿⣿⣿⣾⣦⡹⣿⣿⣿⣦⡳⣽⣿⣿⣿⠟⢋⡄⢀⣴⠏⠀⠈⠘⠁⠀⢀⣴⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⠀⠀⠀⠘⢿⣷⣤⠀⠲⢤⣤⣬⣝⣛⣿⣿⡿⠈⣷⣿⣿⣿⣿⣿⣿⣟⣫⣴⣾⠟⠰⠋⣡⡴⠇⠀⠐⠀⠰⠿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⡇⠀⠀⠈⢆⠈⠛⠂⠁⠂⠝⡛⠿⣿⣿⣿⣵⡁⠻⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⣒⣫⣭⣤⣤⣤⣀⠀⠀⢠⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⠀⢠⠀⠀⠳⣄⠲⣶⣤⡀⠠⣤⣤⣬⣿⣿⡿⠷⠿⠿⢿⣿⡿⠟⢉⠀⢁⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⡀⠹⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣧⠸⣧⠀⠀⣌⠣⡈⠻⣿⡀⠀⠙⠻⢿⣿⣿⣷⣶⣶⣶⣾⣷⠿⠋⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣷⣿⣷⡀⠸⣷⣌⡀⠈⠃⠀⠀⠂⠀⠉⠻⣿⣿⣿⣿⣿⣷⡗⡀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡻",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣽⣿⣿⣮⣀⠀⢱⣤⡘⣷⣦⣦⣙⠻⠟⠛⠋⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⢹⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⠏⢠⣴⣥⡌⢀⣄⢻⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠈⣿⣿⣿⣿⣿⣿⣿⣿⠀⣾⣿⠋⣠⣼⣿⠈⣿⢿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢠⠘⣿⣿⣿⣿⣿⣿⣿⣧⡘⠁⣼⣿⡿⠃⣼⡟⢸",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠉⣰⠀⡈⢠⣝⢿⣿⣿⣿⣿⣿⣟⣻⣶⣤⣤⡒⠋⣸⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⣫⡵⡿⢠⡇⢠⡇⠈⢻⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⣻⣵⣾⣿⣿⣱⠇⢸⠀⡸⣰⣆⠀⢻⣎⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣣⣾⣿⣿⣿⣿⡿⢋⠀⣠⠞⣴⣿⣿⡆⠈⢿⠈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣱⣿⣿⣿⣿⡿⢋⣴⠃⣰⣿⠀⣿⡿⣫⣶⣦⣌⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢱⣿⣿⣿⣿⣿⠀⣿⣿⠀⣿⣿⡀⣿⢱⣿⣿⣿⣿⡇⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡸⣿⣿⣿⣿⡿⠀⠛⠛⠀⢹⣿⡇⠙⡼⢋⣿⣿⣿⣧⠀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⣧⠻⣿⣿⡟⠀⠀⣄⠀⠀⣸⡿⠃⣀⣴⣿⣿⣿⣿⣿⣷⡀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿",
    "⣿⣿⣿⣿⣿⣿⣿⣿⢡⣾⣿⣿⣿⣿⣿⣿⣷⣌⠀⠷⢉⣴⠆⠀⠘⢷⢀⣿⠟⠈⢁⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⢹⣿⣿⣿⣿⣿⠿⠛⣋",
]

def is_space(k):     return (not k.is_sequence) and str(k) == ' '
def is_esc(k):       return k.is_sequence and k.name == 'KEY_ESCAPE'
def is_enter(k):     return (k.is_sequence and k.name == 'KEY_ENTER') or str(k) in ('\n', '\r')
def is_backspace(k): return (k.is_sequence and k.name in ('KEY_BACKSPACE', 'KEY_DELETE')) or str(k) in ('\x7f', '\b')
def key_char(k):
    if not k.is_sequence and len(str(k)) == 1: return str(k)
    return None

def put(row, col, text):
    print(term.move(row, max(0, col)) + text, end='', flush=True)

def cx(text, width): return max(0, (width - len(text)) // 2)
def box_top(w): return '┌' + '─' * (w-2) + '┐'
def box_bot(w): return '└' + '─' * (w-2) + '┘'
def box_sep(w): return '├' + '─' * (w-2) + '┤'
def clear_key_buffer():
    while term.inkey(timeout=0): pass
def wrap_text(text, width):
    words = text.split(); lines, cur = [], ""
    for word in words:
        c = word if not cur else f"{cur} {word}"
        if len(c) <= width: cur = c
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines or [""]

# BG color constant
BG = term.on_color_rgb(12, 0, 0)

def fill_bg(h, w):
    """Fill entire screen with uniform dark red background."""
    for row in range(h):
        put(row, 0, BG + ' ' * w + term.normal)

def draw_splash():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width

        # Uniform background
        fill_bg(h, w)

        art_w  = 50   # width of each side art panel
        gap    = 2    # gap between art and centre panel

        if w >= 120:
            # Left art
            left_x   = 1
            art_rows = LEFT_ART[:h-2]
            art_sy   = max(0, (h - len(art_rows)) // 2)
            for i, line in enumerate(art_rows):
                put(art_sy + i, left_x, c_red(line[:art_w]))

            # Right art
            right_x  = w - art_w - 1
            art_rows2 = EVA_ART[:h-2]
            art_sy2  = max(0, (h - len(art_rows2)) // 2)
            for i, line in enumerate(art_rows2):
                put(art_sy2 + i, right_x, c_red(line[:art_w]))

            # Centre panel — sits between the two art panels
            cp_x0  = left_x + art_w + gap
            cp_x1  = right_x - gap
            rp_w   = cp_x1 - cp_x0
            rp_x   = cp_x0
            rp_h   = h - 4
            rp_y   = 2

        elif w >= 80:
            # Only right art, panel takes left half
            right_x  = w - art_w - 1
            art_rows2 = EVA_ART[:h-2]
            art_sy2  = max(0, (h - len(art_rows2)) // 2)
            for i, line in enumerate(art_rows2):
                put(art_sy2 + i, right_x, c_red(line[:art_w]))
            rp_w  = right_x - gap - 2
            rp_x  = max(1, (right_x - rp_w) // 2)
            rp_h  = h - 4
            rp_y  = 2
        else:
            rp_w = min(w-2, 64)
            rp_x = (w - rp_w) // 2
            rp_h = h - 4
            rp_y = 2

        # Draw NERV panel (no black box — just text on bg)
        put(rp_y,            rp_x, c_red('▀' * rp_w))
        put(rp_y + rp_h - 1, rp_x, c_red('▄' * rp_w))

        hdr = 'NERV HEADQUARTERS'
        put(rp_y + 1, rp_x + cx(hdr, rp_w), c_muted(hdr))

        logo_w = len(NERV_LOGO[0])
        lx = rp_x + max(0, (rp_w - logo_w) // 2)
        ly = rp_y + 3
        for i, line in enumerate(NERV_LOGO):
            put(ly + i, lx, c_red(line))

        le = ly + len(NERV_LOGO)
        uline = '━' * min(max(16, rp_w // 2), rp_w - 4)
        put(le + 1, rp_x + cx(uline, rp_w), c_dred(uline))

        for i, (txt, col) in enumerate([
            ('GEHIRN ADVANCED RESEARCH', c_amber),
            ('MAGI SYSTEM  v3.0',        c_muted),
            ('CLASSIFICATION  TOP SECRET', c_muted),
        ]):
            put(le + 3 + i, rp_x + cx(txt, rp_w), col(txt))

        prompt   = '[ PRESS SPACE TO INITIALIZE ]'
        prompt_y = rp_y + rp_h - 3
        prompt_x = rp_x + cx(prompt, rp_w)

        stop_ev = threading.Event()
        def blink():
            vis = True
            while not stop_ev.is_set():
                put(prompt_y, prompt_x, c_amber(prompt) if vis else BG + ' '*len(prompt) + term.normal)
                vis = not vis
                stop_ev.wait(0.55)
        t = threading.Thread(target=blink, daemon=True)
        t.start()
        while True:
            key = term.inkey(timeout=0.05)
            if not key: continue
            if is_space(key): stop_ev.set(); t.join(0.7); clear_key_buffer(); break
            if is_esc(key):   stop_ev.set(); sys.exit(0)


def draw_password_gate():
    typed = []
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        fill_bg(h, w)
        bw = min(w, 62); bh = 14
        bx = (w - bw) // 2; by = max(2, (h - bh) // 2)
        for row in range(bh): put(by+row, bx, BG + ' '*bw + term.normal)
        put(by,     bx, c_red(box_top(bw)))
        put(by+1,   bx, c_red('│') + c_orange('  MAGI AUTHENTICATION PROTOCOL'.ljust(bw-2)) + c_red('│'))
        put(by+2,   bx, c_red(box_sep(bw)))
        put(by+3,   bx, c_red('│') + c_white('  Enter access code:'.ljust(bw-2)) + c_red('│'))
        put(by+4,   bx, c_red(box_sep(bw)))
        put(by+5,   bx, c_red('│') + ' '*(bw-2) + c_red('│'))
        put(by+6,   bx, c_red(box_sep(bw)))
        put(by+7,   bx, c_red('│') + ' '*(bw-2) + c_red('│'))
        put(by+8,   bx, c_red(box_sep(bw)))
        put(by+9,   bx, c_red('│') + c_muted('  [ ENTER ] confirm  [ BKSP ] erase  [ ESC ] quit'.ljust(bw-2)) + c_red('│'))
        put(by+10,  bx, c_red(box_sep(bw)))
        put(by+11,  bx, c_red(box_bot(bw)))
        row_field = by+5; row_msg = by+7

        def _field():
            dots = '  '.join('●' for _ in typed) if typed else '·  ·  ·  ·  ·'
            put(row_field, bx, c_red('│') + c_amber(f'  CODE   {dots}'[:bw-2].ljust(bw-2)) + c_red('│'))
        def _msg(text='', col=None):
            col = col or c_bright
            line = f'  {text}' if text else ''
            put(row_msg, bx, c_red('│') + (col(line[:bw-2].ljust(bw-2)) if line else ' '*(bw-2)) + c_red('│'))

        _field(); _msg()
        while True:
            key = term.inkey(timeout=0.1)
            if not key: continue
            if is_esc(key): sys.exit(0)
            if is_enter(key):
                if ''.join(typed).upper() == ACCESS_CODE.upper():
                    _msg('ACCESS GRANTED', col=c_green); time.sleep(0.7); return True
                _msg('ACCESS DENIED — initiating brute-force...', col=c_bright)
                time.sleep(1.2); typed.clear(); _field()
                _msg('[ W ] wait for MAGI decrypt   [ R ] retry', col=c_amber)
                while True:
                    k2 = term.inkey(timeout=0.2)
                    if not k2: continue
                    ch2 = key_char(k2)
                    if ch2 and ch2.lower() == 'w': return draw_brute_force()
                    if ch2 and ch2.lower() == 'r': _msg(); break
                    if is_esc(k2): sys.exit(0)
                continue
            if is_backspace(key):
                if typed: typed.pop(); _field()
                continue
            ch = key_char(key)
            if ch and ch.isalnum() and len(typed) < 5:
                typed.append(ch.upper()); _field()


BRUTE_PHASES = [
    ('CASPAR  ── INITIALISING KEY SEARCH',    0.00, 0.12),
    ('CASPAR  ── DICTIONARY LAYER I',         0.12, 0.22),
    ('BALTHASAR ─ PARALLEL HASH EXPANSION',   0.22, 0.35),
    ('BALTHASAR ─ ENTROPY ANALYSIS',          0.35, 0.47),
    ('MELCHIOR ── NEURAL PATTERN MATCH',      0.47, 0.60),
    ('MELCHIOR ── DEEP CIPHER TRAVERSAL',     0.60, 0.72),
    ('MAGI CORE  ─ COLLATION',                0.72, 0.83),
    ('MAGI CORE  ─ FINAL BRUTE PASS',         0.83, 0.96),
    ('MAGI CORE  ─ UNLOCKING…',               0.96, 1.00),
]
HEX_CHARS = '0123456789ABCDEF'
def _rand_hex(n=32): return ' '.join(''.join(random.choices(HEX_CHARS, k=4)) for _ in range(max(1, n//4)))
def _prog_bar(pct, width, cf=None, ce=None):
    filled = int(width*pct)
    return (cf or c_green)('█'*filled) + (ce or c_dim)('░'*max(0,width-filled))

def draw_brute_force():
    total = BRUTE_SECONDS; start_ts = time.time()
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        h, w = term.height, term.width
        print(term.clear); fill_bg(h, w)
        bw = min(w, 72); bx = (w-bw)//2; by = 1; bh = min(h-2, 28)
        for row in range(bh): put(by+row, bx, BG + ' '*bw + term.normal)
        put(by,    bx, c_red(box_top(bw)))
        put(by+1,  bx, c_red('│') + c_bright('  MAGI SYSTEM — MANUAL DECRYPTION ENGAGED'.ljust(bw-2)) + c_red('│'))
        put(by+2,  bx, c_red(box_sep(bw)))
        put(by+3,  bx, c_red('│') + c_muted('  Authentication failed. Running brute-force key recovery.'.ljust(bw-2)) + c_red('│'))
        put(by+4,  bx, c_red('│') + c_muted('  Do not close this terminal. Process cannot be paused.'.ljust(bw-2)) + c_red('│'))
        put(by+5,  bx, c_red(box_sep(bw)))
        put(by+8,  bx, c_red(box_sep(bw)))
        put(by+11, bx, c_red(box_sep(bw)))
        put(by+18, bx, c_red(box_sep(bw)))
        put(by+22, bx, c_red(box_sep(bw)))
        put(by+25, bx, c_red(box_sep(bw)))
        put(by+26, bx, c_red('│') + c_muted('  [ ESC ] abort'.ljust(bw-2)) + c_red('│'))
        put(by+27, bx, c_red(box_bot(bw)))
        R = dict(bar=by+6,pct=by+7,lbl=by+9,phase=by+10,hex=by+12,cas=by+19,bal=by+20,mel=by+21,clk=by+23,tick=by+24)
        bar_w = max(10, bw-14); hex_buf = ['']*6; last_sec = -1
        while True:
            key = term.inkey(timeout=0.12)
            if key and is_esc(key): sys.exit(0)
            now = time.time(); elapsed = min(now-start_ts, total)
            pct = elapsed/total; remain = max(0, total-elapsed)
            cur_sec = int(elapsed)
            if cur_sec == last_sec: continue
            last_sec = cur_sec
            mm, ss = divmod(int(remain), 60)
            put(R['bar'],  bx, c_red('│') + c_muted('  TOTAL  ') + _prog_bar(pct, bar_w, c_amber, c_dim) + c_muted('  ') + c_red('│'))
            put(R['pct'],  bx, c_red('│') + c_amber(f'  {pct*100:5.1f}%  complete     ETA  {mm:02d}:{ss:02d}'.ljust(bw-2)) + c_red('│'))
            pl, pp = BRUTE_PHASES[-1][0], 1.0
            for lbl,p0,p1 in BRUTE_PHASES:
                if pct<=p1: pl=lbl; pp=max(0.0,min(1.0,(pct-p0)/max(0.001,p1-p0))); break
            put(R['lbl'],   bx, c_red('│') + c_cyan(f'  {pl}'[:bw-2].ljust(bw-2)) + c_red('│'))
            put(R['phase'], bx, c_red('│') + c_muted('  PHASE  ') + _prog_bar(pp, bar_w, c_cyan, c_dim) + c_muted('  ') + c_red('│'))
            hex_buf = hex_buf[1:] + [_rand_hex(bw-8)]
            for i,line in enumerate(hex_buf):
                put(R['hex']+i, bx, c_red('│') + (c_dim if i<4 else c_muted)(f'  {line}'[:bw-2].ljust(bw-2)) + c_red('│'))
            votes = [
                (c_bright if pct<0.33 else c_amber if pct<0.50 else c_green)('  CASPAR     ──  '+('ANALYZING...' if pct<0.33 else 'PATTERN FOUND' if pct<0.50 else 'APPROVED')),
                (c_bright if pct<0.50 else c_amber if pct<0.75 else c_green)('  BALTHASAR  ──  '+('COMPUTING...' if pct<0.50 else 'CONVERGING' if pct<0.75 else 'APPROVED')),
                (c_bright if pct<0.72 else c_amber if pct<0.95 else c_green)('  MELCHIOR   ──  '+('DEEP SCAN...' if pct<0.72 else 'KEY MATCH' if pct<0.95 else 'APPROVED')),
            ]
            for i,v in enumerate(votes): put(R['cas']+i, bx, c_red('│') + v[:bw-2].ljust(bw-2) + c_red('│'))
            tick = '▊' if cur_sec%2==0 else '▉'
            put(R['clk'],  bx, c_red('│') + c_yellow(f'  {tick}  TIME REMAINING   {mm:02d} min  {ss:02d} sec'.ljust(bw-2)) + c_red('│'))
            tickers = ['SCANNING KEY SPACE ...','TESTING PERMUTATIONS ...','CROSS-REFERENCING PATTERN DB ...','MAGI CONSENSUS IN PROGRESS ...','DECRYPTION LAYER ACTIVE ...']
            put(R['tick'], bx, c_red('│') + c_muted(f'  {tickers[cur_sec%len(tickers)]}'[:bw-2].ljust(bw-2)) + c_red('│'))
            if pct >= 1.0:
                put(R['clk'], bx, c_red('│') + c_green('  DECRYPTION COMPLETE — ACCESS GRANTED'.ljust(bw-2)) + c_red('│'))
                time.sleep(2.0); return True


def draw_message_box(message):
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        fill_bg(h, w)
        bw = min(max(68, w-16), 96); inner_w = bw-6
        lines = wrap_text(message, inner_w)
        visible = min(len(lines), max(6, h-10))
        lines = lines[:visible]; bh = visible+8
        bx = max(0,(w-bw)//2); by = max(1,(h-bh)//2)
        for row in range(bh): put(by+row, bx, BG+' '*bw+term.normal)
        put(by,   bx, c_red(box_top(bw)))
        put(by+1, bx, c_red('│') + c_orange('  TERMINAL COMMUNIQUE'.ljust(bw-2)) + c_red('│'))
        put(by+2, bx, c_red(box_sep(bw)))
        for idx,line in enumerate(lines):
            put(by+3+idx, bx, c_red('│') + '  ' + c_white(line.center(inner_w)) + '  ' + c_red('│'))
        fr = by+3+visible
        put(fr,   bx, c_red(box_sep(bw)))
        put(fr+1, bx, c_red('│') + c_amber('  [ ENTER ] continue'.ljust(bw-2)) + c_red('│'))
        put(fr+2, bx, c_red('│') + c_muted('  [ ESC   ] abort'.ljust(bw-2)) + c_red('│'))
        put(fr+3, bx, c_red(box_bot(bw)))
        while True:
            key = term.inkey(timeout=0.1)
            if not key: continue
            if is_esc(key):   return False
            if is_enter(key): return True


def draw_final_secret_prompt():
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        print(term.clear)
        h, w = term.height, term.width
        fill_bg(h, w)
        bw = min(w, 76); bh = 12
        bx = (w-bw)//2; by = max(2,(h-bh)//2)
        for row in range(bh): put(by+row, bx, BG+' '*bw+term.normal)
        put(by,    bx, c_red(box_top(bw)))
        put(by+1,  bx, c_red('│') + c_orange('  FINAL AUTHORIZATION LAYER'.ljust(bw-2)) + c_red('│'))
        put(by+2,  bx, c_red(box_sep(bw)))
        put(by+3,  bx, c_red('│') + c_white('  Press Enter for the final secret message.'.ljust(bw-2)) + c_red('│'))
        put(by+4,  bx, c_red('│') + c_muted('  This will execute the configured terminal payload.'.ljust(bw-2)) + c_red('│'))
        put(by+5,  bx, c_red(box_sep(bw)))
        put(by+6,  bx, c_red('│') + c_amber('  [ ENTER ] execute'.ljust(bw-2)) + c_red('│'))
        put(by+7,  bx, c_red('│') + c_muted('  [ ESC   ] abort'.ljust(bw-2)) + c_red('│'))
        put(by+8,  bx, c_red(box_sep(bw)))
        put(by+9,  bx, c_red('│') + c_dim('  Awaiting final trigger...'.ljust(bw-2)) + c_red('│'))
        put(by+10, bx, c_red('│') + c_dim(FINAL_COMMAND[:bw-4].ljust(bw-2)) + c_red('│'))
        put(by+11, bx, c_red(box_bot(bw)))
        while True:
            key = term.inkey(timeout=0.1)
            if not key: continue
            if is_esc(key):   return False
            if is_enter(key): break
    print(term.clear)
    subprocess.run(['bash', '-lc', FINAL_COMMAND], check=False)
    return True


def main():
    try:
        draw_splash()
        draw_password_gate()
        draw_message_box(LOREM_IPSUM)
        draw_final_secret_prompt()
    except KeyboardInterrupt:
        pass
    finally:
        print(term.clear + term.normal)
        print(c_red('\n  [ NERV ]  Session terminated.\n'))

if __name__ == '__main__':
    main()
