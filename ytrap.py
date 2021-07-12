import pyautogui
import ark
import json
import time
import cv2
import numpy as np
import screen


crystal_template = cv2.imread("templates/gacha_crystal.png", cv2.IMREAD_GRAYSCALE)
gen2suit_template = cv2.imread("templates/gen2suit.png", cv2.IMREAD_GRAYSCALE)
deposit_all_template = cv2.imread("templates/deposit_all.png", cv2.IMREAD_COLOR)
added_template = cv2.imread("templates/added_template.png", cv2.IMREAD_GRAYSCALE)

lower_cyan = np.array([90,255,255])
upper_cyan = np.array([110,255,255])

hsv = cv2.cvtColor(deposit_all_template, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_cyan, upper_cyan)
masked_template = cv2.bitwise_and(deposit_all_template, deposit_all_template, mask= mask)
deposit_all_gray_template = cv2.cvtColor(masked_template, cv2.COLOR_BGR2GRAY)


beds = {}


lapCounter = 0

ark.setParams(1.45, 1.45, 10)
statusText = ""

def setStatusText(txt):
    global statusText
    statusText = txt

def setBeds(b):
    beds = b;

def canDeposit():
    roi = screen.getScreen()    
    screen_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(screen_hsv, lower_cyan, upper_cyan)
    masked_screen = cv2.bitwise_and(roi, roi, mask= mask)
    gray_screen = cv2.cvtColor(masked_screen, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_screen, deposit_all_gray_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 14000000):
        return True
    return False


def checkWeWearingSuit():
    roi = screen.getScreen()[150:440,740:1170]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, gen2suit_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(max_val)
    if(max_val > 1000000):
        return True
    return False


def checkWeHoldingSuit():
    roi = screen.getScreen()[230:330,110:680]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, gen2suit_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    print(max_val)
    if(max_val > 1000000):
        return True
    return False

def checkWeGotRowOfCrystals():
    roi = screen.getScreen()[323:423,111:213]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if(max_val > 5500000):
        return True
    return False

def checkWeGotCrystals():
    roi = screen.getScreen()[230:330,120:210]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray_roi, crystal_template, cv2.TM_CCOEFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if(max_val > 5500000):
        return True
    return False

def waitForAddedGraphic():
    counter = 0
    while(counter < 10):
        roi = screen.getScreen()[1030:1070, 37:142]
        gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(gray_roi, added_template, cv2.TM_CCOEFF)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if(max_val > 3000000):
            return True

        time.sleep(0.1)
        counter += 1
    return False


def dropGen2Suit(popcorn = False):
    pyautogui.press('i')
    time.sleep(2.0)
    while(ark.inventoryIsOpen() == False):
        pyautogui.press('i')
        ark.sleep(2.0)
    
    while(checkWeWearingSuit()):
        pyautogui.moveTo(800, 200)
        pyautogui.dragTo(450, 275, 0.2)

        pyautogui.moveTo(800, 300)
        pyautogui.dragTo(450, 275, 0.2)

        pyautogui.moveTo(800, 400)
        pyautogui.dragTo(450, 275, 0.2)

        pyautogui.moveTo(1100, 200)
        pyautogui.dragTo(450, 275, 0.2)

        pyautogui.moveTo(1100, 400)
        pyautogui.dragTo(450, 275, 0.2)
        pyautogui.moveTo(800, 200)

        ark.sleep(2.0)

    
    if(popcorn):
        ark.searchMyStacks("fed")
        pyautogui.moveTo(165, 280)
        pyautogui.click()
        while(checkWeHoldingSuit()):
            pyautogui.press('o')
    else:
        ark.dropItems("fed")
        ark.dropItems("")

    ark.closeInventory()


def loadGacha():
    if(beds["aberrationMode"] == False):
        for i in range(6):
            if(ark.openInventory() == True):
                break
        if(ark.inventoryIsOpen() == False):
            return
        
        ark.searchStructureStacks("pellet")
        ark.tTransferFrom(7)
        ark.closeInventory()

    if(beds["turnDirection"] == 360):
        ark.step('right', 1.0)
        ark.harvestCropStack("trap")
        pyautogui.press('c')

        ark.step('right', 1.0)
        ark.harvestCropStack("trap")
        pyautogui.press('c')

        ark.step('right', 1.0)
        ark.harvestCropStack("trap")
        pyautogui.press('c')

        ark.step('right', 1.0)

    else:
        if(beds["turnDirection"] == "left"):
            ark.step('left', 1.0)
        else:
            ark.step('right', 1.0)
    
        ark.harvestCropStack("trap")
        pyautogui.press('c')
        if(beds["turnDirection"] == "left"):
            ark.step('left', 1.0)
        else:
            ark.step('right', 1.0)
    
        ark.lookDown()
        ark.step('up', 0.1)
        ark.harvestCropStack("trap")
        pyautogui.press('c')
        if(beds["turnDirection"] == "left"):
            ark.step('right', 2.0)
        else:
            ark.step('left', 2.0)
    
    ark.lookUp()
    ark.lookDown()

    for i in range(30):
        if(ark.openInventory() == True):
            ark.transferAll("trap")
            ark.transferAll()
            ark.dropItems("")
            ark.closeInventory()
            return
        else:
            ark.sleep(2)

    
def pickupWithFSpam():
    pyautogui.press('c')
    ark.lookDown()
    ark.step('s', 1.5)
    for i in range(6):
        pyautogui.press('f')
        ark.sleep(0.2)
        ark.step('w', 0.1)
    ark.step('w', 1.0)

    pyautogui.press('f')
        
def pickupWithWhip():
    pyautogui.press('c')
    ark.lookUp()
    if(ark.openInventory()):
        ark.takeAll("broken")
        ark.searchStructureStacks("whip")
        pyautogui.moveTo(1295, 283);
        pyautogui.dragTo(690, 1050, 0.5, button='left')
        waitForAddedGraphic()
        ark.closeInventory()

        ark.lookDown()
        ark.step('right', 2.0)
        pyautogui.press('1')
        ark.sleep(1.0)
        pyautogui.click()
        ark.sleep(1.0)
        pyautogui.click()
        ark.sleep(1.0)
        pyautogui.press('1')
        ark.step('left', 2.0)
        ark.lookDown()
    else:
        ark.lookDown()
        pyautogui.press('c')
        pickupWithFSpam()

    

def whipCrystals():
    for i in range(beds["crystalBeds"]):
        setStatusText("Picking up crystals")
        ark.bedSpawn(beds["crystalBedPrefix"] + str(i).zfill(2), beds["bedX"], beds["bedY"])
        openTribeLog()

        if(beds["pickupMethod"] == "whip"):
            pickupWithWhip()
        else:
            pickupWithFSpam()

        pyautogui.press('i')
        ark.sleep(2.0)

        
        ark.searchMyStacks("gacha")
        pyautogui.moveTo(167, 280, 0.1)
        pyautogui.click()
        ark.sleep(1.0)
    
        count = 0
        while(checkWeGotRowOfCrystals()):
            for i in range(6):
                pyautogui.moveTo(167+(i*95), 280, 0.1)
                pyautogui.click()
                pyautogui.press('e')
    
            ark.sleep(0.8)
            count += 6
    
        pyautogui.moveTo(165, 280)
        pyautogui.click()
        while(checkWeGotCrystals()):
            pyautogui.press('e')
            ark.sleep(0.2)
            count += 1
            if(count > 300):
                break
        ark.closeInventory()
    
        pyautogui.press('c')
        ark.step('up', 0.9)
    
        while(canDeposit() == False):
            ark.step('w', 0.4)
            ark.sleep(0.2)
            
        for i in range(8):
            pyautogui.press('e')
            ark.sleep(0.2)
            while(ark.getBedScreenCoords() != None):
                pyautogui.press('esc')
                ark.sleep(2.0)
    
        ark.step('up', 0.7)
        for i in range(6):
            pyautogui.press('e')
            ark.sleep(0.2)
            while(ark.getBedScreenCoords() != None):
                pyautogui.press('esc')
                ark.sleep(2.0)
    
        ark.lookUp()
        if(ark.openInventory()):
            time.sleep(0.5)
            pyautogui.moveTo(690, 1050)
            pyautogui.click()
            pyautogui.press('t')
            time.sleep(0.5)

            ark.transferAll("whip")
            for item in beds["keepItems"]:
                ark.transferAll(item)
            ark.dropItems("")
            ark.closeInventory()
        ark.lookDown()
        if(beds["dropGen2Suits"]):
            dropGen2Suit(False)
        ark.step('s', 0.4)
        ark.accessBed()
    
def openTribeLog():
    if(beds["openTribeLog"]):
        pyautogui.press('l')
        ark.sleep(6)
        ark.closeTribeLog()
            
def getStatus():
    return statusText
    
def stop():
    ark.terminate(True)

def start(b):
    global beds
    global lapCounter
    beds = b
    ark.terminate(False)
    setStatusText("Starting. F2 to stop. Alt tab back into the game NOW.")
    try:
        ark.sleep(8)
        start = time.time()
        while(True):
            for i in range(beds["seedBeds"]):
                duration = time.time() - start
                if(duration > beds["crystalInterval"]):
                    start = time.time()
                    whipCrystals()
                    lapCounter += 1
                    if(lapCounter > beds["suicideFrequency"]):
                        setStatusText("Suiciding . . .")
                        lapCounter = 0
                        suicideBed = beds["suicideBed"]
                        ark.bedSpawn(suicideBed, beds["bedX"], beds["bedY"])
                        if(beds["dropGen2Suits"]):
                            dropGen2Suit(False)
                        ark.sleep(20)

                setStatusText("Seeding at gachaseed" + str(i).zfill(2))

                ark.bedSpawn(beds["seedBedPrefix"] + str(i).zfill(2), beds["bedX"], beds["bedY"])
                openTribeLog()
                loadGacha()
                if(beds["dropGen2Suits"]):
                    dropGen2Suit(True)
                ark.lookDown()
                ark.step('s', 0.3)
                ark.accessBed()
    except:
        print("Bot thread terminated.")
