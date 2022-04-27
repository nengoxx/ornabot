from random import random
from libs.imagesearch.imagesearch import *


images_dir = "./images/"
ssize = "720"

i_battle = images_dir + 'battle_'+ ssize +'.PNG'
i_spell = images_dir + 'spell_'+ ssize +'.PNG'
i_continue = images_dir + 'continue_'+ ssize +'.PNG'
i_cancel = images_dir + 'cancel_'+ ssize +'.PNG'
i_refill = images_dir + 'refill_'+ ssize +'.PNG'

coordOffset = [30,10] # offset for the button coordinates x,y
windowRect = [0,0,0,0]

mobCoords=[70,240] #from x1 10 to x2 400; from y1 190 to y2 590
mobWH = [295,285]

lastClick = [0,0]

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
        pyautogui.moveTo(x=randcoords[0],y=randcoords[1],duration=0.5)
        #pyautogui.click(x=randcoords[0],y=randcoords[1],button='left')
        checkClick(randcoords)
    return

def findImage(i, timesample = 300, searchtime = 5, click = True):
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
    randcoords = randCoords(pos)
    if (pos[0] > 0 and click):
        pyautogui.moveTo(x=randcoords[0],y=randcoords[1],duration=0.5)
        #pyautogui.click(x=randcoords[0],y=randcoords[1],button='left')
        checkClick(randcoords,i)
    return randcoords
    
def checkClick(c,i=0):
    global lastClick
    if (i != 0 and lastClick != c): #recheck image just before clicking in case the animations are slow
        pos = imagesearcharea(i, windowRect[0],windowRect[1],windowRect[2],windowRect[3])
        if (pos[0] > 0):
            checkClick(c)
    elif (i==0 and lastClick != c and c[0] > 0): #no image provided only check coordinates 
        pyautogui.click(x=c[0],y=c[1],button='left')
        lastClick = c
        


'''
Randomization
'''
def r_old(num, rand):
    return num + rand*random.random()

def r(num1, num2):
    return random.randint(num1, num2)

def randCoords_old(coords, offset = coordOffset):  # random mouse clicking
    #[x1, y1, w, h] = coords
    [x1, y1] = coords
    w, h = 30, 30
    #offset as percentage of the size
    xoffset = (w *(offset[0]/100))/2
    yoffset = (h *(offset[1]/100))/2
    x1 = x1 + xoffset
    x2 = w - xoffset*2
    y1 = y1 + yoffset
    y2 = h - yoffset*2
    #log("Coords Between x: (" + str(x1)+' '+str(x1+x2)+'), offset: '+str(xoffset))
    #log("Coords Between y: (" + str(y1) + ' ' + str(y1+y2)+'), offset: '+str(yoffset))
    #auxx = r(x1 + xoffset, w - xoffset*2)
    #auxy = r(y1 + yoffset, h - yoffset*2)
    auxx = r(x1,x2)
    auxy = r(y1,y2)
    return [auxx, auxy]

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