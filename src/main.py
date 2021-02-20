from tensorflowfunction import *
from bluetoothcommunication import *
from tkinter import *
import pyttsx3
from threading import * 
import sys

rootWindow = Tk()
rootWindow.iconphoto(False, PhotoImage(file = "src/pics/eye.png"))
rootWindow.title("Safe eye")
rootWindow.geometry("500x500")

robotVoice = pyttsx3.init()


def welcome():
    robotVoice.say("Safe eye started")
    robotVoice.runAndWait()

welcomeThread = Thread(target=welcome).start()

startButton = Button(rootWindow, text = "Start using camera").pack()




rootWindow.mainloop()
sys.exit()