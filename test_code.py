from tkinter import *
from tkinter.ttk import *

# Create the main window
master = Tk()
master.geometry("300x200")  # Set window size
master.title("Main Window")
var = StringVar()
var.set("Test label")

# Function to open a new window
def open_new_window():
    new_window = Toplevel(master)  # Create a new window
    new_window.title("New Window")
    new_window.geometry("250x150")  

    label = Label(new_window,textvariable=var, text="This is a new window").pack(pady=20)
    Button(new_window, text="Submit", command=submit).pack(pady=10)

    def submit():
        var.set("Button been pressed broski")

# Create a label and a button to open the new window
Label(master, text="This is the main window").pack(pady=10)
Button(master, text="Open New Window", command=open_new_window).pack(pady=10)

# Run the Tkinter event loop
master.mainloop()