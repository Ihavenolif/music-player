import wave
import sys
import pyaudio
import time
import threading
import numpy

import tkinter as tk

from classes.window import Window
from classes.song import Song
from classes.player import Player
from classes.images import Images

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

player = Player()

def audio_datalist_set_volume(datalist, volume):
    """ Change value of list of audio chunks """
    sound_level = (volume / 100.)

    for i in range(len(datalist)):
        chunk = numpy.fromstring(datalist[i], numpy.int16)

        chunk = chunk * sound_level

        datalist[i] = chunk.astype(numpy.int16)
    
    return datalist

def play_song():
    with wave.open(sys.argv[1], 'rb') as wf:
        stream = player.PA.open(format=player.PA.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        while len(data := wf.readframes(player.CHUNK)):
            while not player.PLAYING:
                time.sleep(0.1)
            stream.write(data)

        stream.close()

thread = threading.Thread(target=play_song)
thread.start()

Window.pause_label.bind("<Button-1>", lambda e:player.toggle_pause())

Window.start_loop()