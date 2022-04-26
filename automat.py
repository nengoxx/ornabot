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

refill_button = [0,0]
cancel_button = [0,0]
battle_button = [0,0]
spell_button = [0,0]
continue_button = [0,0]

def checkState():
    global statetime
    global state
    global refill_button 
    global cancel_button 
    global battle_button
    global spell_button
    global continue_button
    refill_button = [0,0]
    cancel_button = [0,0]
    battle_button = [0,0]
    spell_button = [0,0]
    continue_button = [0,0]
    
    
    battle_button = func.findButton(func.i_battle)
    if (battle_button[0] > 0): #mob select
        state = 1
        statetime = time.time()
        return   
    refill_button = func.findButton(func.i_refill)
    if (refill_button[0] > 0):                          #world
        state = 0
        statetime = time.time()
        return
    cancel_button = func.findButton(func.i_cancel)
    if (refill_button[0] < 0 and battle_button[0] < 0 and cancel_button[0] > 0): #codex or other non desirable state(find cancel button)
        state = 2
        statetime = time.time()
        return
    spell_button = func.findButton(func.i_spell)
    if (spell_button[0] > 0):
        state = 3
        statetime = time.time()
        return
    continue_button = func.findButton(func.i_continue)
    if (continue_button[0] > 0):
        state = 4
        statetime = time.time()
        return
    pyautogui.sleep(randint(1000, 2000)/1000)
    

def findMob(t=5):
    global state
    global refill_button 
    global cancel_button 
    global battle_button 
    start = time.time()
    checkState()
    while ((state==0) and ((time.time()-start) < t)):
        randMobCoords = func.randCoords(func.mobCoords,func.mobWH) #get and click random coords for mobs to fight
        pyautogui.moveTo(x=randMobCoords[0],y=randMobCoords[1],duration=0.1)
        func.checkClick(randMobCoords)
        #pyautogui.sleep(randint(500, 1000)/1000)
        checkState()
        if (state != 0):
            return
            
            
        
def fightMob(t=20):
    global state
    global spell_button
    global continue_button
    start = time.time()
    checkState()
    while ((state==3) and ((time.time()-start) < t)):
        spellcoords=func.randCoords(spell_button)
        pyautogui.moveTo(x=spellcoords[0],y=spellcoords[1],duration=0.5)
        func.checkClick(spellcoords)
        #pyautogui.sleep(randint(800, 1500)/1000)
        checkState()
        if (state != 3):
            return


def refill(hold=3000):
    global state
    if (state==0):
        refillcoords=func.randCoords(refill_button)
        pyautogui.moveTo(x=refillcoords[0],y=refillcoords[1],duration=0.5)
        pyautogui.mouseDown()
        pyautogui.sleep(randint(2000, hold)/1000)
        pyautogui.mouseUp()
    else:
        state = 2