from random import randint
from time import sleep
import pyautogui
import keyboard
import tkinter
from win32gui import GetWindowText, GetForegroundWindow
import time

#
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False
pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0

botting = False
BarSpam = False
windowName = "Genshin Impact"


def toggleBot(kb_event_info):
    global botting
    botting = not botting
    showText()


def showText():
    global botting
    global label
    label = tkinter.Label(text='autoF', font=(None, '12', 'bold'), fg='white', bg='black')
    if ((botting == True) & get_active_window()):
        label.master.overrideredirect(True)
        #label.master.geometry("+5+5")
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


def main():
    global botting
    if __name__== "__main__" :
        keyboard.on_press_key('º',toggleBot)
        while True:
            while (get_active_window()):
                if botting:
                    pyautogui.press("f")
                    pyautogui.sleep(randint(10, 400)/1000)
                    #time.sleep(randint(10, 400)/1000)


main()
#