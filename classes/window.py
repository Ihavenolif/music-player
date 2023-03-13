import tkinter as tk

TK = tk.Tk()

from classes.images import Images

class Window:
    # MIDDLE FRAME
    content_frame = tk.Frame(width=600, height=400, bg="#555")
    content_frame.pack(fill=tk.BOTH, expand=True)

    # MUSIC CONTROL BAR
    music_control_frame = tk.Frame(bg="#333", height=50)

    progress_bar_frame = tk.Frame(master=music_control_frame)

    previous_label = tk.Label(master=music_control_frame ,image=Images.previous)
    pause_label = tk.Label(master=music_control_frame ,image=Images.play)
    next_label = tk.Label(master=music_control_frame ,image=Images.next)

    previous_label.pack(side=tk.LEFT)
    pause_label.pack(side=tk.LEFT)
    next_label.pack(side=tk.LEFT)

    music_control_frame.pack(fill=tk.BOTH)

    def start_loop():
        TK.mainloop()