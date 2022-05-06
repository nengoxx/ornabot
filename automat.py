import time
from random import randint
import pyautogui
import keyboard

import config
import func

state = 0
statetime = 0
'''
0-world
1-mob select
2-unknown
3-battle mob
4-continue to world
'''
refillTime=0
foughtSinceRefill = 0

useItems=0
timeSinceItem = 0

zoomout=0

refill_button = [0,0]
cancel_button = [0,0]
battle_button = [0,0]
spell_button = [0,0]
continue_button = [0,0]

def checkState(threaded=False):
    global statetime
    global state
    global refillTime
    global foughtSinceRefill
    global timeSinceItem
    global useItems
    
    global refill_button 
    global cancel_button 
    global battle_button
    global spell_button
    global continue_button
    # refill_button = [0,0]
    # cancel_button = [0,0]
    # battle_button = [0,0]
    # spell_button = [0,0]
    # continue_button = [0,0]
    
    if (statetime==0):
        statetime=time.time()
    
    if (time.time() - statetime > 300 and func.botting):
        func.relaunchApp()
        state = 2
        statetime = time.time()
        return
    
    if ((time.time() - statetime > 15 and state == 3) or (time.time() - statetime > 10 and state!=3) or foughtSinceRefill > 20 ):
        if (refillTime != 1):
            refillTime = 1
            statetime = time.time()
            
    if((config.useCoins or config.useExpPot) and (time.time() - timeSinceItem > 3600)):
        useItems=1
    
    battle_button = func.findButton(func.i_battle)
    if (battle_button[0] > 0): #mob select
        if (state != 1 and state != 5): #battle button still visible when on low hp
            state = 1
            statetime = time.time()
        return   
    cancel_button = func.findButton(func.i_cancel)
    refill_button = func.findButton(func.i_refill)
    if (cancel_button[0] < 0 and refill_button[0] > 0): #refill button still visible when on low hp on state 1                         #world
        if (state != 0):
            state = 0
            statetime = time.time()
        return
    if (refill_button[0] < 0 and battle_button[0] < 0 and cancel_button[0] > 0): #codex or other non desirable state(find cancel button)
        if (state != 2):
            state = 2
            statetime = time.time()
        return
    spell_button = func.findButton(func.i_spell1)
    if (spell_button[0] > 0 and refill_button[0] < 0 and cancel_button[0] < 0):
        if (state != 3):
            state = 3
            statetime = time.time()
        return
    continue_button = func.findButton(func.i_continue)
    if (continue_button[0] > 0 and refill_button[0] < 0 and cancel_button[0] < 0):
        if (state != 4):
            state = 4
            statetime = time.time()
        return
    #pyautogui.sleep(randint(1000, 2000)/1000)
    

def findMob(t=1):
    global state
    if (state != 0 or (not func.botting)):
        return
    global refill_button 
    global cancel_button 
    global battle_button 
    start = time.time()
    #checkState()
    while (state==0 and (time.time()-start) < t):
        randMobCoords = func.randCoords(func.mobCoords,func.mobWH) #get and click random coords for mobs to fight
        pyautogui.moveTo(x=randMobCoords[0],y=randMobCoords[1],duration=0.1)
        if (state != 0):
            return
        func.checkClick(randMobCoords)
        #pyautogui.sleep(randint(500, 1000)/1000)
        #checkState()
        
            
            
        
def fightMob(t=1):
    global state
    if (state != 3 or (not func.botting)):
        return
    global spell_button
    global continue_button
    start = time.time()
    #checkState()
    while (state==3 and (time.time()-start) < t):
        if (spell_button[0]>30):
            spellcoords=func.randCoords(spell_button)
            pyautogui.moveTo(x=spellcoords[0],y=spellcoords[1],duration=0.3)
            if (state != 3):
                return
            func.checkClick(spellcoords)
        #pyautogui.sleep(randint(800, 1500)/1000)
        #checkState()
        
def flee(hold = 5000):
    global state
    if (refillTime == 1 and state==3):
        fleecoords=func.findImage(func.i_flee,click=False)
        if (fleecoords[0]>30):
            pyautogui.moveTo(x=fleecoords[0],y=fleecoords[1],duration=0.5)
            pyautogui.mouseDown()
            pyautogui.sleep(randint(2000, hold)/1000)
            pyautogui.mouseUp()
        if(state==3):#if it fails, try to take down the mob
            fightMob()
            func.findImage(func.i_spell2)
            
    

def refill(hold=3000):
    global state
    global foughtSinceRefill
    global refillTime
    if (refillTime == 1 and state ==0):
        # func.findImage(func.i_cancel)
        # pyautogui.sleep(randint(1000, 2000)/1000)
        refillcoords=func.findImage(func.i_refill,click=False)
        if (refillcoords[0]>30):
            pyautogui.moveTo(x=refillcoords[0],y=refillcoords[1],duration=0.5)
            pyautogui.mouseDown()
            pyautogui.sleep(randint(2000, hold)/1000)
            pyautogui.mouseUp()
            foughtSinceRefill = 0
            refillTime = 0
    # else:
    #     state = 2
    # state = 0
    
def use_Items(): #torch+coins
    global state
    global timeSinceItem
    global useItems
    if (useItems == 1 and (config.useCoins or config.useExpPot) and state ==0):
        refillcoords=func.findImage(func.i_refill,click=False)
        if (refillcoords[0]>30):
            pyautogui.moveTo(x=refillcoords[0],y=refillcoords[1],duration=0.5)
            if (state != 0):
                return
            func.checkClick(refillcoords)
            pyautogui.sleep(randint(2000, 3000)/1000)
            # if (config.useExpPot):
            #     pyautogui.scroll(-5)
                #TODO
            if (state != 0 and state!=2):#TODO new state
                return
            # pyautogui.scroll(-20)
            # keyboard.press('down_arrow')
            # pyautogui.keyDown("down")
            # kb.press(Key.down)
            # pyautogui.sleep(randint(4000, 5000))
            # kb.release(Key.down)
            # pyautogui.keyUp("down")
            # keyboard.release('down_arrow')
            func.swipe('up')
            func.swipe('up')
            pyautogui.sleep(randint(700, 1000)/1000)
            func.findImage(func.i_torch)
            if (config.useCoins):
                pyautogui.sleep(randint(700, 1000)/1000)
                func.findImage(func.i_coin1)
                pyautogui.sleep(randint(700, 1000)/1000)
                func.findImage(func.i_coin2)
            timeSinceItem = time.time()
            useItems = 0
            returnToWorld()
    return
    
def returnToWorld():
    global state
    match state:
        case 0:#world
            func.findImage(func.i_cancel)
            pyautogui.sleep(randint(1000, 2000)/1000)
        case 1:#entering battle
            func.findImage(func.i_cancel)
            pyautogui.sleep(randint(1000, 2000)/1000)
        case 2:#wrong state
            func.findImage(func.i_cancel)
            pyautogui.sleep(randint(1000, 2000)/1000)
        case 3:#battle
            flee()
        case 4:#continue
            func.findImage(func.i_continue)
            pyautogui.sleep(randint(1000, 2000)/1000)
        case _:
            func.findImage(func.i_cancel)
            pyautogui.sleep(randint(1000, 2000)/1000)
            
def zoomOut():
    global zoomout
    if (zoomout == 0):
        zoomout = 1
        return
    if(state==0):
        #pyautogui doesn't work for sending special keys to scrcpy
        pyautogui.moveTo(x=func.mobCoords[0],y=func.mobCoords[1],duration=0.5)
        keyboard.press('ctrl')
        pyautogui.dragTo(func.mobCoords[0]+func.mobWH[0]/2, func.mobCoords[1]+func.mobWH[1]/2, 0.5, button='left')
        keyboard.release('ctrl')
        zoomout=0