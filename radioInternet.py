from tkinter import *
import webbrowser
from time import gmtime, strftime
from datetime import datetime
import webbrowser
import radio

def openUrl():
    link = urlEntry.get()
    webbrowser.open_new(link)

def time(): 
    now = datetime.now()
    string = now.strftime("%H:%M:%S - %d/%m/%Y")
    timeLabel.config(text = string) 
    if isopentime():
        openUrl()
    timeLabel.after(1000, time) 

def gettimelist(Stime):
    listtime = [int(i) for i in Stime.split(':') if i.isdigit()]
    return listtime

def isopentime():
    timer = timerEntry.get()
    now = datetime.now()
    realtime = now.strftime("%H:%M:%S")

    if (gettimelist(timer)==gettimelist(realtime)):
        return True
    else: return False

root = Tk()

root.title("Open a link")

timeLabel = Label(root, text="")

linkLabel = Label(root, text="Link: ")
urlEntry = Entry(root, width=30, borderwidth=5)

setClockLabel = Label(root, text="Timer: ")
timerEntry = Entry(root, width=30, borderwidth=5)

#openButton = Button(root, text="Open", command = openUrl)

timeLabel.grid(row=0, column=0, columnspan=2)

linkLabel.grid(row=1, column=0)
urlEntry.grid(row=1, column=1)
setClockLabel.grid(row=2, column=0)
timerEntry.grid(row=2, column=1)
#openButton.grid(row=2, column=1)

time()

root.mainloop()
