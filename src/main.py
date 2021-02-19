from tensorflowfunction import *
from bluetoothcommunication import *
from tkinter import *
import pyttsx3

rootWindow = Tk()
rootWindow.title("Safe eye")


robotVoice = pyttsx3.init()

for _ in range(10):
    robotVoice.say("hello guys")
    robotVoice.runAndWait()




rootWindow.mainloop()