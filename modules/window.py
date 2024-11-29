import tkinter as tk
import music_tag
import signal

from tkinter import ttk
from tkinter.filedialog import askopenfilename

TK = tk.Tk()

import modules.images as Images
from modules.song import Song
from modules.player import Player

player:Player = None

def debug_print_queue():
    player.queue.debug_print()

def debug_print_active_song():
    song = player.active_song
    print(f"Player:\nPaused: {player.paused}, Song: {player.active_song}\nActive song:\nName: {song.title}, Progress: {song.progress}, Length: {song.length}")

def kokot():
    print("kokot")

def toggle_pause():
    pause_status = player.toggle_pause()
    if pause_status:
        pause_label.configure(image=Images.play)
    else:
        pause_label.configure(image=Images.pause)

def open_file():
    filepath = askopenfilename(initialdir="~",filetypes=(("Audio file", "*.mp3 *.wav *.aac *.mp4 *.ogg"), ("","")))

    filetype = filepath.split(".")[-1]

    tags = music_tag.load_file(filepath)
    title = str(tags["tracktitle"])
    artist = str(tags["artist"])
    album = str(tags["album"])
    length_secs = float(str(tags["#length"]))

    player.queue.add(Song(source=filetype, title=title, author=artist, album=album, length=length_secs, link=filepath))

def skip_song():
    player.skip_song()
    # update UI with new song


# MENU BAR
menu_bar = tk.Menu(master=TK)

filemenu = tk.Menu(master=menu_bar, tearoff=0)
filemenu.add_command(label="Open file", command=open_file)
menu_bar.add_cascade(label="File", menu=filemenu)

debugmenu = tk.Menu(master=menu_bar, tearoff=0)
debugmenu.add_command(label="Print Queue", command=debug_print_queue)
debugmenu.add_command(label="Print Active Song", command=debug_print_active_song)
menu_bar.add_cascade(label="Debug", menu=debugmenu)

# MIDDLE FRAME
content_frame = tk.Frame(width=600, height=400, bg="#555")
content_frame.pack(fill=tk.BOTH, expand=True)

# MUSIC CONTROL BAR
music_control_frame = tk.Frame(bg="#333", height=60)

progress_bar_val = tk.IntVar()
progress_bar = ttk.Progressbar(master=music_control_frame, orient="horizontal", mode="determinate", maximum=1, variable=progress_bar_val)

previous_label = tk.Label(master=music_control_frame ,image=Images.previous)
pause_label = tk.Label(master=music_control_frame ,image=Images.play)
next_label = tk.Label(master=music_control_frame ,image=Images.next)

volume_bar = tk.Scale(master=music_control_frame, orient=tk.HORIZONTAL)

progress_bar.pack(fill=tk.X)

previous_label.pack(side=tk.LEFT)
pause_label.pack(side=tk.LEFT)
next_label.pack(side=tk.LEFT)
volume_bar.pack(side=tk.RIGHT)

music_control_frame.pack(fill=tk.BOTH)

def set_global_player_reference(x:Player):
    global player
    player = x
    player.progress_bar = progress_bar
    player.progress_bar_val = progress_bar_val
    player.volume_bar = volume_bar

def kill_program():
    print("Stopping playback")
    player.stop_sig = True
    print("Closing window")
    TK.destroy()
    print("Exiting with code 0")
    exit(0)

def sigint_handler(sig = None, frame = None):
    kill_program()



def start_loop():
    TK.config(menu=menu_bar)
    TK.protocol("WM_DELETE_WINDOW", kill_program)
    signal.signal(signal.SIGINT, sigint_handler)
    TK.mainloop()

