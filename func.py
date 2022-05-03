from random import random
import tkinter
from win32gui import *
import win32com.client

from libs.imagesearch.imagesearch import *
import config

botting = False
windowName = "Nexus 5"
windowSize = [424,759]

images_dir = "./images/"
ssize = "720"

i_battle = images_dir + 'battle_'+ ssize +'.PNG'
i_spell = images_dir + 'spell_'+ ssize +'.PNG'
i_spell2 = images_dir + 'spell2_'+ ssize +'.PNG'
i_continue = images_dir + 'continue_'+ ssize +'.PNG'
i_cancel = images_dir + 'cancel_'+ ssize +'.PNG'
i_refill = images_dir + 'refill_'+ ssize +'.PNG'
i_flee = images_dir + 'flee_'+ ssize +'.PNG'

coordOffset = [10,30] # offset for the button coordinates x,y
windowRect = [0,0,0,0]

mobCoords=[70,240] #from x1 10 to x2 400; from y1 190 to y2 590
mobWH = [295,285]

lastClick = [0,0]

'''
Image & mouse
'''
def clickCoords(c):
    if (c[0]>0):
        randcoords = randCoords(c)
        pyautogui.click(x=randcoords[0],y=randcoords[1],button='left')
    return

def holdClick():
    return

def findButton(i):
    global windowRect
    if (windowRect[3] == 0): #not initialized
        bCoords = imagesearch(i)
    else:
        bCoords = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
    return bCoords

def findClickButton(i):
    global windowRect
    if (windowRect[3] == 0): #not initialized
        bCoords = imagesearch(i,0.5)
    else:
        bCoords = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
    if (bCoords[0] > 1 ): # coords not -1,-1 or 0,0
        randcoords = randCoords(bCoords)
        pyautogui.moveTo(x=randcoords[0],y=randcoords[1],duration=0.3)
        #pyautogui.click(x=randcoords[0],y=randcoords[1],button='left')
        checkClick(randcoords)
    return

def findImage(i, timesample = 100, searchtime = 5, click = True):
    global windowRect
    start = time.time()
    if (windowRect[3] == 0): #not initialized
        pos = imagesearch(i)
        while (pos[0] == -1 and (time.time()-start) > searchtime):
            time.sleep(timesample)
            pos = imagesearch(i)
    else:
        pos = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
        while (pos[0] == -1 and (time.time()-start) > searchtime):
            time.sleep(timesample)
            pos = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
    randcoords = [0,0]
    if (pos[0] > 0):
        randcoords = randCoords(pos)
        if  (click):
            pyautogui.moveTo(x=randcoords[0],y=randcoords[1],duration=0.3)
            #pyautogui.click(x=randcoords[0],y=randcoords[1],button='left')
            checkClick(randcoords,i)
    return randcoords
    
def checkClick(c,i=0):
    global lastClick
    if (i != 0 and lastClick != c): #recheck image just before clicking in case the animations are slow
        pos = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
        if (pos[0] > 30):
            checkClick(c)
    elif (i==0 and lastClick != c and c[0] > 30): #no image provided only check coordinates 
        pyautogui.click(x=c[0],y=c[1],button='left')
        lastClick = c
        


'''
Randomization
'''
def r(num1, num2):
    return random.randint(num1, num2)

def randCoords(coords, offset = coordOffset):  # random mouse clicking
    [x1, y1] = coords
    w, h = offset
    x1 = x1
    x2 = w + x1
    y1 = y1
    y2 = h + y1
    auxx = r(x1,x2)
    auxy = r(y1,y2)
    return [auxx, auxy]

'''
Window
'''
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
    global windowRect
    if (get_active_window()):
        MoveWindow(GetForegroundWindow(),0,0,windowSize[0],windowSize[1],False)
        rect = GetWindowRect(GetForegroundWindow())
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]
        windowRect = [x,y,w,h]