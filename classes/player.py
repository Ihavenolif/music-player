import pyaudio
import threading
import time
import tkinter as tk
import music_tag

from PIL import Image
from tkinter.filedialog import askopenfilename

from classes.song import Song
from classes.images import Images
from classes.window import Window, init_after_player



class Player:
    QUEUE:list[Song] = []
    PA = pyaudio.PyAudio()
    CHUNK = 512
    PLAYING = False
    song:Song = Song("", "", "", "", 0, "", image=Image.new("RGB", (1000,1000), (255,255,255)))

    def __init__(self) -> None:
        pass

    def play_song():
        stream = Player.PA.open(format=Player.PA.get_format_from_width(Player.song.seg.sample_width),
                              channels=Player.song.seg.channels,
                              rate=Player.song.seg.frame_rate,
                              output=True)
        
        while Player.song.progress <= Player.song.length:
            while not Player.PLAYING:
                time.sleep(0.1)
            stream.write(Player.song.chunked_file[Player.song.progress]._data)
            Player.song.progress += 1
            Window.progress_bar.step()
        
        stream.close()
        Player.song.finished_playing = True
        Player.load_song()

    def add_to_queue(song:Song):
        Player.QUEUE.append(song)

    def load_song():
        if Player.QUEUE == []: return
        Player.song = Player.QUEUE[0]
        Player.QUEUE.pop(0)
        Player.song.load()
        Window.progress_bar.configure(maximum=Player.song.length)

        thread = threading.Thread(target=Player.play_song)
        thread.start()

    def toggle_pause():
        if Player.PLAYING:
            Window.pause_label.configure(image=Images.play)
        else:
            Window.pause_label.configure(image=Images.pause)
            if not Player.song or Player.song.finished_playing:
                Player.load_song()
                
                

        Player.PLAYING = not Player.PLAYING
    
    def skip_song():
        Player.song.progress = Player.song.length

# INIT WINDOW

def open_file():
    filepath = askopenfilename(initialdir="~",filetypes=(("Audio file", "*.mp3 *.wav *.aac *.mp4 *.ogg"), ("","")))

    filetype = filepath.split(".")[-1]

    tags = music_tag.load_file(filepath)
    title = tags["tracktitle"]
    artist = tags["artist"]
    album = tags["album"]
    length_secs = float(str(tags["#length"])) * 60

    img = tags["artwork"]

    pil_img = img.first.thumbnail([512,512])

    Player.add_to_queue(Song(source=filetype, title=title, author=artist, album=album, length=length_secs, link=filepath, image=pil_img))

init_after_player(open_file)