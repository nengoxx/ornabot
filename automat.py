import time
import func
from random import randint
import pyautogui

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
    
    if ((time.time() - statetime > 20 and state == 3) or foughtSinceRefill > 20 or time.time() - statetime > 10):
        if (refillTime != 1):
            refillTime = 1
            statetime = time.time()
    
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
    spell_button = func.findButton(func.i_spell)
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
    if (state != 0):
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
    if (state != 3):
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
    else:
        state = 2
    state = 0
    
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