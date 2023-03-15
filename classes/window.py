import tkinter as tk

from tkinter import ttk
from tkinter.filedialog import askopenfilename

TK = tk.Tk()

from classes.images import Images
from classes.song import Song


class Window:
    # MENU BAR
    

    # MIDDLE FRAME
    content_frame = tk.Frame(width=600, height=400, bg="#555")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # MUSIC CONTROL BAR
    music_control_frame = tk.Frame(bg="#333", height=60)

    progress_bar = ttk.Progressbar(master=music_control_frame, orient="horizontal", mode="determinate", maximum=1)

    previous_label = tk.Label(master=music_control_frame ,image=Images.previous)
    pause_label = tk.Label(master=music_control_frame ,image=Images.play)
    next_label = tk.Label(master=music_control_frame ,image=Images.next)
    
    progress_bar.pack(fill=tk.X)

    previous_label.pack(side=tk.LEFT)
    pause_label.pack(side=tk.LEFT)
    next_label.pack(side=tk.LEFT)

    music_control_frame.pack(fill=tk.BOTH)

    def start_loop():
        TK.config(menu=Window.menu_bar)
        TK.mainloop()

def init_after_player(open_file):
    Window.menu_bar = tk.Menu(master=TK)
    Window.filemenu = tk.Menu(master=Window.menu_bar, tearoff=0)
    Window.filemenu.add_command(label="Open file", command=open_file)
    Window.menu_bar.add_cascade(label="File", menu=Window.filemenu)