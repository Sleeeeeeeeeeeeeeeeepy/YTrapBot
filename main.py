import json
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from pynput.keyboard import Key, Listener
import ytrap
import threading
from tkinter import ttk
from ttkthemes import ThemedTk


with open('settings.json') as json_file:
    data = json.load(json_file)

r = ThemedTk(theme="arc")

r.title('Gacha Bot')
ytrap.setStatusText("Ready. Press F1 to start.")

def updateStatus():
    statusLabel['text'] = ytrap.getStatus()
    r.after(100, updateStatus)

def onKeyPress(key):
    if(key == Key.f1):
        saveJson()
        print(getThisLocation())
        x = threading.Thread(target=ytrap.start, args=([getThisLocation()]), daemon=True)
        x.start()
    if(key == Key.f2):
        ytrap.stop()
        ytrap.setStatusText("Ready. Press F1 to start.")


def onKeyRelease(key):
    pass
    
listener = Listener(on_press=onKeyPress, on_release=onKeyRelease)
listener.start()

def getThisLocation():
    for i in data["locations"]:
        if(i["name"] == locationVariable.get()):
            return i


def saveJson():
    file = open("settings.json", "w")
    file.write(json.dumps(data, indent=4, sort_keys=True))
    file.close()

fillingUI = False
def fillUI():
    global fillingUI
    location = locationVariable.get()
    for i in data["locations"]:
        if(i["name"] == location):
            fillingUI = True
            if(i["aberrationMode"] == True):
                mapVariable.set("Aberration")
            elif(i["dropGen2Suits"] == True):
                mapVariable.set("Gen2")
            else:
                mapVariable.set("Other")

            if(i["turnDirection"] == "left"):
                cropVariable.set("Left")
            else:
                cropVariable.set("Right")

            defaultXEntry.delete(0, tk.END)
            defaultXEntry.insert(0, str(i["bedX"]))

            defaultYEntry.delete(0, tk.END)
            defaultYEntry.insert(0, str(i["bedY"]))

            crystalBedsEntry.delete(0, tk.END)
            crystalBedsEntry.insert(0, str(i["crystalBeds"]))

            seedBedsEntry.delete(0, tk.END)
            seedBedsEntry.insert(0, str(i["seedBeds"]))

            pickupIntervalEntry.delete(0, tk.END)
            pickupIntervalEntry.insert(0, str(i["crystalInterval"]))
            
            suicideFrequencyEntry.delete(0, tk.END)
            suicideFrequencyEntry.insert(0, str(i["suicideFrequency"]))

            suicideBedEntry.delete(0, tk.END)
            suicideBedEntry.insert(0, str(i["suicideBed"]))

            gachaItems = ", ".join(i["keepItems"])
            gachaItemsEntry.delete(0, tk.END)
            gachaItemsEntry.insert(0, gachaItems)
            fillingUI = False


def locationChanged(*args):
    fillUI()

def reloadLocations():
    # Reset var and delete all old options
    locationVariable.set('')
    locationMenu['menu'].delete(0, 'end')

    # Insert list of new options (tk._setit hooks them up to var)
    for location in data["locations"]:
        locationMenu['menu'].add_command(label=location["name"], command=tk._setit(locationVariable, location["name"]))
    if(len(data["locations"]) > 0):
        locationVariable.set(data["locations"][0]["name"])
        

def addLocation():
    answer = tk.simpledialog.askstring("Input", "What do you want to call this gacha location?",
            parent=r)
    if answer is not None and answer != "":
        data["locations"].append({ 
            "name": answer,
            "bedX": 0,
            "bedY": 0,
            "crystalBeds": 1,
            "seedBeds": 12,
            "crystalInterval": 500,
            "dropGen2Suits": False,
            "aberrationMode": False,
            "keepItems": ["fab", "riot", "pump"],
            "suicideBed": "suicide bed",
            "suicideFrequency": 3,
            "turnDirection": "left"
        })
        reloadLocations()
    else:
        tk.messagebox.showinfo( "No location name", "You must enter a name for your gacha tower.")

def deleteLocation():
    if(len(data["locations"]) > 0):
        count = 0
        for i in data["locations"]:
            if(i["name"] == locationVariable.get()):
                del data["locations"][count]
                break
            count += 1
        reloadLocations()
    else:
        tk.messagebox.showinfo("No locations", "There are no locations to delete.")


def onMapChange(*args):
    loc = getThisLocation()
    if(mapVariable.get() == "Aberration"):
        loc["aberrationMode"] = True
        loc["dropGen2Suits"] = False
    if(mapVariable.get() == "Gen2"):
        loc["aberrationMode"] = False
        loc["dropGen2Suits"] = True
    if(mapVariable.get() == "Other"):
        loc["aberrationMode"] = False
        loc["dropGen2Suits"] = False
    saveJson()

def onCropDirectionChange(*args):
    loc = getThisLocation()
    if(cropVariable.get() == "Left"):
        loc["turnDirection"] = "left"
    else:
        loc["turnDirection"] = "right"
    saveJson()    

def onEntryChanged(*args):
    if(fillingUI == False):
        loc = getThisLocation()
        loc["bedX"] = int(defaultXEntry.get())
        loc["bedY"] = int(defaultYEntry.get())
        loc["crystalBeds"] = int(crystalBedsEntry.get())
        loc["seedBeds"] = int(seedBedsEntry.get())
        loc["crystalInterval"] = int(pickupIntervalEntry.get())
        loc["keepItems"] = gachaItemsEntry.get().split(", ") 
        loc["suicideBed"] = suicideBedEntry.get()
        loc["suicideFrequency"] = int(suicideFrequencyEntry.get())
        saveJson()


frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)
label = ttk.Label(frame, text="Plant Y Gacha Bot")
label.config(font=("Courier", 22))
label.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)
locationVariable = tk.StringVar(frame)
locationVariable.set("Spider Cave") # default value

label = ttk.Label(frame, text="Location")
label.pack(side=tk.LEFT)
locationMenu = ttk.OptionMenu(frame, locationVariable, "")
locationMenu.pack(side=tk.LEFT)

reloadLocations()

button = ttk.Button(frame, text='Delete', command = deleteLocation)
button.pack(side=tk.RIGHT)
button = ttk.Button(frame, text="Add", command = addLocation)
button.pack(side=tk.RIGHT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)
mapVariable = tk.StringVar(frame)
mapVariable.set("Other") # default value

label = ttk.Label(frame, text="Map")
label.pack(side=tk.LEFT)
mapMenu = ttk.OptionMenu(frame, mapVariable, "", "Other", "Aberration", "Gen2")
mapMenu.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Bed pixel coords")
label.pack(side=tk.LEFT)

label = ttk.Label(frame, text="X")
label.pack(side=tk.LEFT)

defaultXSv = tk.StringVar()
defaultXEntry = ttk.Entry(frame, textvariable=defaultXSv)
defaultXEntry.pack(side=tk.LEFT)

label = ttk.Label(frame, text="Y")
label.pack(side=tk.LEFT)

defaultYSv = tk.StringVar()
defaultYEntry = ttk.Entry(frame, textvariable=defaultYSv)
defaultYEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Crystal beds")
label.pack(side=tk.LEFT)

crystalBedsSv = tk.StringVar()
crystalBedsEntry = ttk.Entry(frame, textvariable=crystalBedsSv)
crystalBedsEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Seed beds")
label.pack(side=tk.LEFT)

seedBedsSv = tk.StringVar()
seedBedsEntry = ttk.Entry(frame, textvariable=seedBedsSv)
seedBedsEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Crystal pickup interval")
label.pack(side=tk.LEFT)

pickupIntervalSv = tk.StringVar()
pickupIntervalEntry = ttk.Entry(frame, textvariable=pickupIntervalSv)
pickupIntervalEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Suicide frequency")
label.pack(side=tk.LEFT)

suicideFrequencySv = tk.StringVar()
suicideFrequencyEntry = ttk.Entry(frame, textvariable=suicideFrequencySv)
suicideFrequencyEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Suicide bed name")
label.pack(side=tk.LEFT)

suicideBedSv = tk.StringVar()
suicideBedEntry = ttk.Entry(frame, textvariable=suicideBedSv)
suicideBedEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)

label = ttk.Label(frame, text="Gacha items to keep (separate by comma)")
label.pack(side=tk.LEFT)

gachaItemsSv = tk.StringVar()
gachaItemsEntry = ttk.Entry(frame, textvariable=gachaItemsSv)
gachaItemsEntry.pack(side=tk.LEFT)

frame = ttk.Frame(r)
frame.pack(fill=tk.X, expand=True)
cropVariable = tk.StringVar(frame)
cropVariable.set("Left") # default value

label = ttk.Label(frame, text="Crop harvest turn direction")
label.pack(side=tk.LEFT)
cropMenu = ttk.OptionMenu(frame, cropVariable, "", "Left", "Right")
cropMenu.pack(side=tk.LEFT)


frame = ttk.Frame(r).pack(fill=tk.X, expand=True)
statusLabel = ttk.Label(frame, text="Press F1 to start the bot")
statusLabel.pack(side=tk.LEFT, fill=tk.X, expand=True)

fillUI()

locationVariable.trace("w", locationChanged)
mapVariable.trace("w", onMapChange)
cropVariable.trace("w", onCropDirectionChange)

defaultXSv.trace_add("write", onEntryChanged)
defaultYSv.trace_add("write", onEntryChanged)
crystalBedsSv.trace_add("write", onEntryChanged)
seedBedsSv.trace_add("write", onEntryChanged)
pickupIntervalSv.trace_add("write", onEntryChanged)
suicideFrequencySv.trace_add("write", onEntryChanged)
suicideBedSv.trace_add("write", onEntryChanged)
gachaItemsSv.trace_add("write", onEntryChanged)

updateStatus()
r.mainloop()
