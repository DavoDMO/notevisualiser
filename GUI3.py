import tkinter as tk
from tkinter import *
from aubioAlgo import *
import time
import threading
import json

# Creating GUI
root = tk.Tk()
root.title("Note Detector")
root.geometry('500x400')
root_width, root_height = 500, 400
root.minsize(root_width,root_height)
root.grid_columnconfigure(0, weight=1)

#frame1=Frame(root)
#frame1.grid(row=0,column=0)

frame2=Frame(root)
frame2.grid(row=1,column=0)

var = StringVar()
var.set("Current Note: ...")

var2 = StringVar()
var2.set("...")

var3 = StringVar()
var3.set("Type some text...")



current = None # Shared variable
running = True # used to stop loop with button

def get_current_note(): # Function from aubioAlgo.py
    global current
    global running
    pitches = []
    confidences = []
    current_pitch = music21.pitch.Pitch()
    last_note = None

    while running:
        data = stream.read(hop_s, exception_on_overflow=False)
        samples = np.fromstring(data,dtype=aubio.float_type)  
        pitch = (pitch_o(samples)[0])
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.


        pitches += [pitch]
        confidences += [confidence]
        # current='Nan'
        if pitch>0:
            current_pitch.frequency = float(pitch)
            # current=current_pitch.nameWithOctave
            last_note = current_pitch.nameWithOctave
        
        current = last_note if last_note else last_note



        # Data to be written
        dictionary = current
        
        # Serializing json
        json_object = json.dumps(dictionary, indent=0)

        # Writing to sample.json
        if current != "null":
            with open("sample.json", "w") as outfile:
                outfile.write(json_object)

        if current == "null":
            with open("sample.json", "r") as openfile:
                json_object = json.load(openfile)
                print(f"Json file: {json_object}")




            
        print(pitch,'----',current,'----',current_pitch.microtone.cents,'----',str(current_time))

        #q.put({'Note': current, 'Cents': current_pitch.microtone.cents,'hz':pitch})

        time.sleep(0.25)
        #break
        #print(f"Current note: {current}")


 



def update_gui():
    var.set("Current Note:")
    var2.set(str(current))
    root.after(500, update_gui)

def start_note_thread():
    global running
    running = True
    note_thread = threading.Thread(target=get_current_note)
    note_thread.daemon = True  # thread closes when main program exits
    note_thread.start()

def stop():
    global running
    running = False

def exit():
    global running
    running = False
    root.destroy()





# second window (w2) stuff:
def open_new_window():
    w2var = StringVar()
    w2var.set("No current target note")

    new_window = Toplevel(root)
    new_window.title("Target Note Window")
    new_window.geometry("300x300")

    # text box stuff:
    def textSubmit():
        input = txt.get()
        w2var.set(str(input))

    txt = Entry(new_window, width=30)
    txt.grid(row=1,column=0)

    submit_btn = tk.Button(new_window, text="Submit", width=5, command=textSubmit)
    submit_btn.grid(row=2,column=0,sticky="W")

    txtLabel = Label(new_window, textvariable=w2var, font='Ariel 17 bold')
    txtLabel.grid(row=0,column=0,sticky='N',pady=(0,0))



root.protocol('WM_DELETE_WINDOW', exit)


# print(f"Current note: {current}")
# get_current_note()



label = Label(textvariable=var, font='Ariel 17 bold')
label.grid(row=0,column=0,sticky='N',pady=(0,0))

label2 = Label(textvariable=var2, font='Ariel 17 bold')
#label2.grid(row=1,column=1,pady=(105,0),padx=(45,0))
label2.grid(row=1,column=0,sticky='',pady=(150,0))




# # text box stuff:
# txt = Entry(root, width=30)
# txt.grid(row=1,column=0)

# submit_btn = tk.Button(text="Submit", width=5, command=textSubmit)
# submit_btn.grid(row=1,column=0,sticky="W")

# txtLabel = Label(textvariable=var3, font='Ariel 17 bold')
# txtLabel.grid(row=1,column=0,sticky='N',pady=(0,0))




# new window button:
w2button = tk.Button(text="Open new window", width=5, command=open_new_window)
w2button.grid(row=2,column=0,sticky="N")




# start, stop and exit buttons:
start_button = tk.Button(text="Start", width=5, command=start_note_thread, activeforeground="black", fg="black", bg="#00b720", activebackground="#00df27")
start_button.grid(column=0, row=2, sticky="W",pady=(150,0),padx=(4,0))

stop_button = tk.Button(text="Stop", width=5, command=stop, activeforeground="black", fg="black", bg="#00beb2", activebackground="#00d1c4")
stop_button.grid(column=0, row=2, sticky="",pady=(150,0),padx=(0,0))

exit_button = tk.Button(text="Exit", width=5, command=exit, activeforeground="white", fg="white", bg="#900029", activebackground="#b70034")
exit_button.grid(column=0, row=2, sticky="E",pady=(150,0),padx=(0,5))


#stop_button = tk.Button(root, text="Stop", command=stop, activeforeground="black", fg="black", bg="#00beb2", activebackground="#00d1c4")
#stop_button.grid(row=5,column=1,pady=(230,0),padx=(15,0))

#exit_button = tk.Button(root, text="Exit", command=exit, activeforeground="white", fg="white", bg="#900029", activebackground="#b70034")
#exit_button.grid(row=5,column=2,pady=(230,0),padx=(24,0))


update_gui()

root.mainloop()

get_current_note()

# button = Button(root, text="Count", command=get_current_note)
# button.pack()

# root.mainloop()



# def clicked():
#     lbl.configure(text = "Button got clicked")

# lbl = Label(root, text = "Current Detected Note:")
# lbl.grid()

# btn = Button(root, text = "Close Window" ,
#              fg = "red", command=root.destroy)
# btn.grid(column=0, row=6)

#root.mainloop()