from random import randint
from time import sleep
import pyautogui
import keyboard
import tkinter
from win32gui import *
import win32com.client
from automat import findMob
from func import *
import func
from automat import *
import automat

#
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
#pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0

botting = False
BarSpam = False
windowName = "Nexus 5"
windowSize = [424,759]



def toggleBot(kb_event_info):
    get_window_rect()
    global botting
    botting = not botting
    showText()


def showText():
    global botting
    global label
    label = tkinter.Label(text='autoF', font=(None, '12', 'bold'), fg='white', bg='black')
    if ((botting == True) & get_active_window()):
        label.master.overrideredirect(True)
        label.master.geometry("+10+10")
        label.master.lift()
        label.master.wm_attributes("-topmost", True)
        label.master.wm_attributes("-disabled", True)
        label.master.wm_attributes("-transparentcolor", "black")
        label.pack()
        label.update()
    else:
        label.master.destroy()


def get_active_window():
    return (GetWindowText(GetForegroundWindow()) == windowName)

def set_active_window():
    hwnd = FindWindow("SDL_app",windowName)
    if (hwnd !=0):
        win32com.client.Dispatch("WScript.Shell").SendKeys('%')
        SetForegroundWindow(hwnd)

def get_window_rect():
    if (get_active_window()):
        MoveWindow(GetForegroundWindow(),0,0,windowSize[0],windowSize[1],False)
        rect = GetWindowRect(GetForegroundWindow())
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        func.windowRect = [x,y,w,h]
        

def main():
    global botting
    global state
    if __name__== "__main__" :
        keyboard.on_press_key('º',toggleBot)
        while True:
            set_active_window()
            while (get_active_window()):
                if botting:
                    # match automat.state:
                    #     case 0:
                    #         findMob()
                    #     case 1:
                    #         findImage(func.i_battle)
                    #         pyautogui.sleep(randint(1000, 2000)/1000)
                    #     case 2:
                    #         findImage(i_cancel)
                    #         pyautogui.sleep(randint(1000, 2000)/1000)
                    #     case 3:
                    #         fightMob()
                    #     case 4:
                    #         findImage(func.i_continue)
                    #         pyautogui.sleep(randint(1000, 2000)/1000)
                    #     case _:
                    #         findImage(i_cancel)
                    #         pyautogui.sleep(randint(1000, 2000)/1000)
                    # automat.checkState()
                    
                    if (automat.state==5):
                        automat.refill()
                    elif (automat.state == 2):
                        findImage(func.i_battle)
                        findImage(i_cancel)
                        pyautogui.sleep(randint(1000, 2000)/1000)
                    elif (automat.state == 0):
                        findMob()
                    elif (automat.state == 3):
                        fightMob()
                    elif (automat.state == 4):
                        findImage(func.i_continue)
                        pyautogui.sleep(randint(1000, 2000)/1000)
                        automat.foughtSinceRefill += 1
                    elif (automat.state == 1):
                        findImage(func.i_battle)
                        pyautogui.sleep(randint(1000, 2000)/1000)
                    automat.checkState()


main()
#