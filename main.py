import wave
import sys
import pyaudio
import time
import threading
import numpy

import tkinter as tk
from PIL import ImageTk, Image
from classes.song import Song

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

# INIT
WINDOW = tk.Tk()
PA = pyaudio.PyAudio()
CHUNK = 512
PLAYING = False
QUEUE:list[Song] = []

# IMAGE LOADING
previous_image = ImageTk.PhotoImage(Image.open("images/previous.png"))
pause_image = ImageTk.PhotoImage(Image.open("images/pause.png"))
play_image = ImageTk.PhotoImage(Image.open("images/play.png"))
next_image = ImageTk.PhotoImage(Image.open("images/next.png"))

# MIDDLE FRAME
content_frame = tk.Frame(width=600, height=400, bg="#555")
content_frame.pack(fill=tk.BOTH, expand=True)

# MUSIC CONTROL BAR
music_control_frame = tk.Frame(bg="#333", height=50)

progress_bar_frame = tk.Frame(master=music_control_frame)

previous_label = tk.Label(master=music_control_frame ,image=previous_image)
pause_label = tk.Label(master=music_control_frame ,image=play_image)
next_label = tk.Label(master=music_control_frame ,image=next_image)

previous_label.pack(side=tk.LEFT)
pause_label.pack(side=tk.LEFT)
next_label.pack(side=tk.LEFT)

music_control_frame.pack(fill=tk.BOTH)

def audio_datalist_set_volume(datalist, volume):
    """ Change value of list of audio chunks """
    sound_level = (volume / 100.)

    for i in range(len(datalist)):
        chunk = numpy.fromstring(datalist[i], numpy.int16)

        chunk = chunk * sound_level

        datalist[i] = chunk.astype(numpy.int16)
    
    return datalist

def toggle_pause():
    global PLAYING
    if PLAYING:
        pause_label.configure(image=play_image)
    else:
        pause_label.configure(image=pause_image)
    PLAYING = not PLAYING
    print(f"Playing: {PLAYING}")

def play_song():
    with wave.open(sys.argv[1], 'rb') as wf:
        stream = PA.open(format=PA.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        while len(data := wf.readframes(CHUNK)):
            while not PLAYING:
                time.sleep(0.1)
            stream.write(audio_datalist_set_volume(data, 50))

        stream.close()

thread = threading.Thread(target=play_song)
thread.start()

pause_label.bind("<Button-1>", lambda e:toggle_pause())

WINDOW.mainloop()