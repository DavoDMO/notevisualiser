import sys
import aubio
from aubio import pitch
import queue
import music21
import pyaudio
import numpy as np
from tkinter import *
import time
# Open stream.
# PyAudio object.
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32,
                channels=1, rate=48000, input=True,
                input_device_index=3, frames_per_buffer=512)

root = Tk()
root.geometry('1000x1000')

q = queue.Queue()  
current_pitch = music21.pitch.Pitch()

filename = 'piano.wav'
samplerate = 48000


win_s = 512 
hop_s = 512 

tolerance = 0.8

pitch_o = pitch("default",win_s,hop_s,samplerate)
#pitch_o.set_unit("")
pitch_o.set_tolerance(tolerance)


# total number of frames read
total_frames = 0
def get_current_note():
    pitches = []
    confidences = []
    current_pitch = music21.pitch.Pitch()
    output = ""

    while True:
        data = stream.read(hop_s, exception_on_overflow=False)
        samples = np.fromstring(data,dtype=aubio.float_type)  
        pitch = (pitch_o(samples)[0])
        #pitch = int(round(pitch))
        confidence = pitch_o.get_confidence()
        #if confidence < 0.8: pitch = 0.
        pitches += [pitch]
        confidences += [confidence]
        current='Nan'
        if pitch>0:
            current_pitch.frequency = float(pitch)
            current=current_pitch.nameWithOctave
            output=pitch,'----',current,'----',current_pitch.microtone.cents
            print(output)

        q.put({'Note': current, 'Cents': current_pitch.microtone.cents,'hz':pitch})
        
        # lbl = Label(root, text=(output))
        # lbl.grid()
        # root.mainloop()

        with open('notes.txt', 'w') as file:
            while True:
                file.write(str((output)))

if __name__ == '__main__':
    get_current_note()
    
