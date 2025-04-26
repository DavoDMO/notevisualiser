import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from aubioAlgo import *
import time
import threading
from music21 import pitch

# Creating GUI
root = tk.Tk()
root.title("Note Detector")
root.geometry('500x400')
root_width, root_height = 500, 400
root.minsize(root_width,root_height)
root.grid_columnconfigure(0, weight=1)

frame1=Frame(root)
frame1.grid(row=0,column=0)

frame2=Frame(root)
frame2.grid(row=1,column=0)

var = StringVar()
var.set("Current Note: ...")

var2 = StringVar()
var2.set("...")

var3 = StringVar()
var3.set("Type some text...")


# global variables
current = None # Shared variable
running = True # used to stop loop with button
targetNote = None
final_colour = "#00AFFF"
upordown_teller = ""

def get_current_note(): # Function from aubioAlgo.py
    global current
    global running
    global targetNote
    global final_colour
    global upordown_teller
    pitches = []
    confidences = []
    recent_pitches = []  # store last few good pitches
    max_recent_pitches = 5  # how many to keep for averaging
    current_pitch = music21.pitch.Pitch()
    last_note = None

    while running:
        data = stream.read(hop_s, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=aubio.float_type)  
        pitch = (pitch_o(samples)[0])
        confidence = pitch_o.get_confidence()
        
        if confidence > 0.9 and pitch > 0:
            recent_pitches.append(pitch)
            if len(recent_pitches) > max_recent_pitches:
                recent_pitches.pop(0)
            avg_pitch = sum(recent_pitches) / len(recent_pitches)

            current_pitch.frequency = avg_pitch
            last_note = current_pitch.nameWithOctave

        # update global "current" whether or not you have a good note
        current = last_note if last_note else None


        pitches += [pitch]
        confidences += [confidence]
        # current='Nan'
        if pitch>0:
            current_pitch.frequency = float(pitch)
            last_note = current_pitch.nameWithOctave
        
        current = last_note if last_note else last_note
        
        if targetNote:
            distance = ""
            diff_in_cents = (current_pitch.midi - targetNote.midi)*100
            # setting colours:
            # NOTES TO SELF:
                # Exact Match (blue) = 0 cents
                # Close (Light Red or Light Green (depending if sharp or flat)) = ±100 cents
                # Medium Far (Medium Red/Green) = ±200 cents
                # Very Far (Dark Red/Green) = ±300 cents
            
            tolerance_buffer = 1
            
            exactText = "Spot On"
            tooHighText = "Too High, Go A Bit Lower"
            tooLowText = "Too Low, Go A Bit Higher"
            
            if abs(diff_in_cents) <= tolerance_buffer:
                upordown_teller = exactText
            if diff_in_cents > 0:
                upordown_teller = tooHighText
            elif diff_in_cents < 0:
                upordown_teller = tooLowText
            else:
                upordown_teller = exactText

            # base colours:
            exactColour = "00AFFF" # blue
            tooHigh = "00FF00" # green
            tooLow = "FF0000" # red

            def hex_to_rgb(hex_color): # converting hex colours to RGB tuples
                hex_color = hex_color.lstrip('#')  # removes '#' if it exists
                return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            
            # converting base colours for blending setup
            exactColour_rgb = hex_to_rgb(exactColour)
            tooHigh_rgb = hex_to_rgb(tooHigh)
            tooLow_rgb = hex_to_rgb(tooLow)

            thresholds = [
                (0, "Exact match"),
                (100, "Close match"),
                (200, "Medium far"),
                (300, "Very far")
            ]
            
            absDiff = abs(diff_in_cents) # setting absolute value
            distance = "Very far" # setting default value

            for max_cents, label in thresholds: # for number and text (max_cents and label) set in thresholds
                if absDiff <= max_cents:
                    distance = label
                    break
            
            if diff_in_cents > 0:
                base_colour_rgb = tooHigh_rgb
            elif diff_in_cents < 0:
                base_colour_rgb = tooLow_rgb
            else:
                base_colour_rgb = exactColour_rgb

            # how much to blend towards blue
            t = min(absDiff / 300, 1.0) # calculating blend factor
            
            # blending setup:
            r= int((1 - t) * exactColour_rgb[0] + t * base_colour_rgb[0])
            g= int((1 - t) * exactColour_rgb[1] + t * base_colour_rgb[1])
            b= int((1 - t) * exactColour_rgb[2] + t * base_colour_rgb[2])

            final_colour = '#{:02x}{:02x}{:02x}'.format(r, g, b)


        else:  
            pass
        
        print("Note difference: ", diff_in_cents)



        # # Data to be written
        # dictionary = current
        
        # # Serializing json
        # json_object = json.dumps(dictionary, indent=0)

        # # Writing to sample.json
        # if current != "null":
        #     with open("sample.json", "w") as outfile:
        #         outfile.write(json_object)

        # if current == "null":
        #     with open("sample.json", "r") as openfile:
        #         json_object = json.load(openfile)
        #         print(f"Json file: {json_object}")




        print(f"Distance is: {distance}")

        print(pitch,'----',current,'----',current_pitch.microtone.cents,'----',str(current_time))
        

        #q.put({'Note': current, 'Cents': current_pitch.microtone.cents,'hz':pitch})

        time.sleep(0.25)
        #break
        #print(f"Current note: {current}")


 



def update_gui():
    var.set("Current Note:")
    var2.set(str(current))
    label2.config(fg=final_colour)
    upDownVar.set(str(upordown_teller))
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
    global targetNote
    w2var = StringVar()
    if targetNote == None:
        w2var.set("No target note entered")
    else:
        w2var.set(f"Current target note: {targetNote.nameWithOctave}")
    new_window = Toplevel(root)
    new_window.title("Target Note Window")
    new_window.geometry("350x300")
    new_window_width, new_window_height = 350, 300
    new_window.minsize(new_window_height,new_window_width)
    new_window.grid_columnconfigure(0, weight=1)

    # text box stuff:
    def textSubmit():
        global targetNote # sets global variable to be accessed outside
        note_input = txt.get() # gets input from textbox

        try:
            targetNote = pitch.Pitch(note_input) # converts textbox input to pitch.Pitch so it can be compared
            w2var.set(str(f"Current target note: {targetNote.nameWithOctave}")) # displaying target note in current GUI
            w2TargetVar.set(targetNote.nameWithOctave) # displaying taret note in main GUI
        except Exception as e:
            w2var.set("Invalid note input") # error message for invalid input
            print("Error:", e) # printing error message

    def w2exit():
        new_window.destroy()

        # drop down menu for mouse-only users
    def mouse_only():
        def show():
            ddLbl.config(text=cb.get())
        # Dropdown options  
        a = ["A", "B", "C", "D", "E", "F", "G"]
        b = ["1", "2", "3", "4", "5", "6", "7"]
        c = ["Sharp", "Flat"]
        # Combobox
        #ddLabelFont = tkFont.Font(family="Ariel", size=10)
        #ddLabel = Label(new_window, text="Select note, sharp/flat, and octave for mouse-only users:", font=ddLabelFont)
        #ddLabel.grid(row=2,column=0,sticky="NW",pady=(35,0),padx=(30,0))
        cb = ttk.Combobox(new_window, values=a, width=10)
        cb.set("Letter")
        cb.grid(row=2,column=0,sticky="SW",pady=(60,0),padx=(2,0))
        cb2 = ttk.Combobox(new_window, values=b, width=10)
        cb2.set("Octave")
        cb2.grid(row=2,column=0,sticky="SW",pady=(60,0),padx=(110,0))
        cb3 = ttk.Combobox(new_window, values=c, width=10)
        cb3.set("Sharp/Flat")
        cb3.grid(row=2,column=0,sticky="SW",pady=(60,0),padx=(217,0))
        # Button to display selection  
        #ddButton = Button(new_window, text="Show Selection", command=show)
        #ddButton.grid(row=2,column=0,sticky="SW",pady=(80,0))
        # Label to show selected value  
        ddLbl = Label(new_window, text=" ")
        ddLbl.grid(row=2,column=0)

    txt = Entry(new_window, width=25, text=targetNote)
    txt.grid(row=1,column=0,sticky="NW")

    submit_btn = tk.Button(new_window, text="Submit", width=5, command=textSubmit)
    submit_btn.grid(row=2,column=0,sticky="NW",pady=(2,0),padx=(2,0))

    txtLabel = Label(new_window, textvariable=w2var, font='Ariel 17 bold', width=20)
    txtLabel.grid(row=0,column=0,sticky="NESW")

    exit_button = tk.Button(new_window, text="Exit", width=5, command=w2exit, activeforeground="white", fg="white", bg="#900029", activebackground="#b70034")
    exit_button.grid(row=3,column=0, sticky="E",pady=(180,0),padx=(0,3))

root.protocol('WM_DELETE_WINDOW', exit)



# print(f"Current note: {current}")
# get_current_note()

label = Label(textvariable=var, font='Ariel 17 bold')
label.grid(row=0,column=0,sticky='N',pady=(0,0))

label2 = Label(textvariable=var2, font='Ariel 17 bold')
#label2.grid(row=1,column=1,pady=(105,0),padx=(45,0))
label2.grid(row=1,column=0,sticky='',pady=(150,0))

upDownVar = StringVar()
upDownVar.set("...")
upDownLabel = Label(textvariable=upDownVar, font='Ariel 17 bold')
upDownLabel.grid(row=0,column=0,sticky='N',pady=(50,0))


# # text box stuff:
# txt = Entry(root, width=30)
# txt.grid(row=1,column=0)

# submit_btn = tk.Button(text="Submit", width=5, command=textSubmit)
# submit_btn.grid(row=1,column=0,sticky="W")

# txtLabel = Label(textvariable=var3, font='Ariel 17 bold')
# txtLabel.grid(row=1,column=0,sticky='N',pady=(0,0))




# new window button:
w2TargetVar = StringVar()
w2TargetVar.set(str(targetNote))

w2button = tk.Button(text="Add Target", width=10, command=open_new_window)
w2button.grid(row=0,column=0,sticky="W",pady=(3,0),padx=(3,0))

w2labelTarget = Label(textvariable=w2TargetVar, font='Ariel 17 bold', width=8, fg="blue")
w2labelTarget.grid(row=1,column=0,sticky="NW",pady=(0,100),padx=(0,0))




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