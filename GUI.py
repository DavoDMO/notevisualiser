from Game import b, noteText
from tkinter import *
#import tkinter as tk
from aubioAlgo import get_current_note, current_pitch, pitch_o
import threading
from threading import Timer

root = Tk()

# def increment(var):
#     var.set(var.get() + 1)

# answer = tk.IntVar()
# tk.Label(root, textvariable=answer).pack()
# root.mainloop()

root.title("Test GUI mucka")

root.geometry('350x200')

#print(get_current_note)

# def printit():
#     threading.Timer(1.0, printit).start()
#     current=current_pitch.nameWithOctave
#     lbl = Label(root, textvariable=current_pitch)
#     lbl.grid()
#     root.mainloop()

#printit()

#for noteLoop in current_pitch:



while True:
    get_current_note()
    current=current_pitch.nameWithOctave
    lbl = Label(root, text=current)
    lbl.grid()
    root.mainloop()