# from tkinter import *
# from tkinter import ttk

# mw=Tk()
# mw.title('Window')
# mw_width, mw_height = 400, 300
# mw.minsize(mw_width,mw_height)
# mw.grid_columnconfigure(0, weight=1)

# frame1=Frame(mw)
# frame1.grid(row=0,column=0)

# main_label=ttk.Label(frame1,text='My label')
# main_label.grid(row=0,column=0,sticky='WE',pady=(75,0))

# mw.mainloop()

import tkinter as tk
from tkinter import *

window = tk.Tk()

window.title("Note Detector")
#window.geometry('500x400')
#window_width, window_height = 400, 300
window.minsize(width = 500, height = 400)
window.grid_columnconfigure(0, weight=1)

label = tk.Label(text="Label 1", font='Ariel 17 bold')
label.grid(row=0,column=1,sticky="W")

label2 = tk.Label(text="L2", font='Ariel 17 bold')
label2.grid(row=1,column=1,sticky="")

button1 = tk.Button(text="B1", width=5)
button2 = tk.Button(text="B2", width=5)
button3 = tk.Button(text="B3", width=5)
button1.grid(column=2, row=5, sticky="W")
button2.grid(column=3, row=5, sticky="S")
button3.grid(column=4, row=5, sticky="E")
window.mainloop()