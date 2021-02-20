# Importing all the needed packages
from tensorflowfunction import *
from bluetoothcommunication import *
from tkinter import *
from tkinter.font import *
from pyttsx3 import *
from threading import * 
import sys

# config all the tkinter window 
rootWindow = Tk()
rootWindow.iconphoto(False, PhotoImage(file = "src/pics/eye.png"))
rootWindow.title("Safe eye")
rootWindow.geometry("500x500")
rootWindow.resizable(False, False)
rootWindow.config(bg = "#a7c5eb")
# initializing the tts
robotVoice = init()
buttonFont = Font(weight = "bold",size = 38)

def welcome():
    robotVoice.say("Safe eye started")
    robotVoice.runAndWait()
welcomeThread = Thread(target=welcome).start()



startBu = Button(rootWindow, text = "Start using camera", bg = "#709fb0", fg = "white", font = buttonFont)
startBu.grid(row = 0, column = 0)
rootWindow.mainloop()
sys.exit()