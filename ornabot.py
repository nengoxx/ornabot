from random import randint
import threading
from time import sleep
import pyautogui
import keyboard
import tkinter
from win32gui import *
import win32com.client
from func import *
import func
from automat import *
import automat
import telegram_bot
import config

#
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
#pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0

# botting = False
# windowName = "Nexus 5"
# windowSize = [424,759]



# def toggleBot(kb_event_info):
#     get_window_rect()
#     global botting
#     botting = not botting
#     showText()


# def showText():
#     global botting
#     global label
#     label = tkinter.Label(text='autoF', font=(None, '12', 'bold'), fg='white', bg='black')
#     if ((botting == True) & get_active_window()):
#         label.master.overrideredirect(True)
#         label.master.geometry("+10+10")
#         label.master.lift()
#         label.master.wm_attributes("-topmost", True)
#         label.master.wm_attributes("-disabled", True)
#         label.master.wm_attributes("-transparentcolor", "black")
#         label.pack()
#         label.update()
#     else:
#         label.master.destroy()


# def get_active_window():
#     return (GetWindowText(GetForegroundWindow()) == config.windowName)

# def set_active_window():
#     hwnd = FindWindow("SDL_app",config.windowName)
#     if (hwnd !=0):
#         win32com.client.Dispatch("WScript.Shell").SendKeys('%')
#         SetForegroundWindow(hwnd)

# def get_window_rect():
#     if (get_active_window()):
#         MoveWindow(GetForegroundWindow(),0,0,config.windowSize[0],config.windowSize[1],False)
#         rect = GetWindowRect(GetForegroundWindow())
#         x = rect[0]
#         y = rect[1]
#         w = rect[2]
#         h = rect[3]
#         func.windowRect = [x,y,w,h]
        
def stateThreading():
    while True:
        automat.checkState(True)

def main():
    global botting
    global state
    stateThread = 0
    if __name__== "__main__" :
        keyboard.on_press_key('º',toggleBot)
        while True:
            if(not get_active_window()):
                set_active_window()
            while (get_active_window()):
                if botting:
                    if (stateThread < 1 ):
                        x = threading.Thread(target=stateThreading, daemon=True)
                        x.start()
                        stateThread += 1
                    
                    if (automat.refillTime==1):
                        returnToWorld()
                        refill()
                        
                    match automat.state:
                        case 0:#world
                            findMob()
                        case 1:#entering battle
                            findImage(func.i_battle)
                            pyautogui.sleep(randint(1000, 2000)/1000)
                        case 2:#wrong state
                            #findImage(func.i_battle,searchtime=1)
                            if (automat.state == 2): #sometimes itdoesnt recognize the battle button fast enough in state 1
                                returnToWorld()
                        case 3:#combat
                            fightMob()
                        case 4:#continue
                            findImage(func.i_continue)
                            pyautogui.sleep(randint(1000, 2000)/1000)
                            automat.foughtSinceRefill += 1
                        case _:
                            returnToWorld()
                    

if __name__ == '__main__':
    # telegram_bot.setupTelegram()
    main()