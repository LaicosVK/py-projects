import cv2
import numpy as np
from PIL import ImageGrab
from win32 import win32gui


# detect windows
windows_list = []
toplist = []
def enum_win(hwnd, result):
    win_text = win32gui.GetWindowText(hwnd)
    windows_list.append((hwnd, win_text))
win32gui.EnumWindows(enum_win, toplist)

# find game
game_hwnd = 0
for (hwnd, win_text) in windows_list:
    if "TETR.IO" in win_text:
        game_hwnd = hwnd       


while True:
    position = win32gui.GetWindowRect(game_hwnd)

    
    # screenshot
    screenshot = ImageGrab.grab(position)
