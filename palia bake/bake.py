#from pyautogui import *
import pyautogui
import time
import keyboard
import random
#import win32api, win32con
from ctypes import *

#pyautogui.displayMousePosition()
#60,125,71




def click(x,y):
    pyautogui.click(x,y)

def onscreen(bild,gs=True,c=0.9):
    if pyautogui.locateOnScreen(f"bilder/{bild}.png", grayscale=True, confidence=c) != None:
        return True
    else:
        return False

def pixel(x,y):
    pic=pyautogui.screenshot(region=(x,y,1,1))
    r,g,b=pic.getpixel((0,0))
    return r,g,b

def bake():
    print("bake")
    pyautogui.keyDown("e")
    time.sleep(1)
    pyautogui.keyUp("e")
    
def make():
    print("make")
    click(1230, 980)
    time.sleep(11)
    pyautogui.keyDown("e")
    time.sleep(1)
    pyautogui.keyUp("e")
    



while keyboard.is_pressed("q") == False:
    #print(pixel(1800,880))
    #time.sleep(0.1)
    print("check")
    if onscreen("bake") or onscreen("bake2") or onscreen("bake3") or onscreen("bake4"):
        bake()
    if onscreen("make"):
        make()

    
