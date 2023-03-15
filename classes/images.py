import os
import sys

from PIL import ImageTk, Image

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Images:
    previous = ImageTk.PhotoImage(Image.open(resource_path("previous.png")))
    pause = ImageTk.PhotoImage(Image.open(resource_path("pause.png")))
    next = ImageTk.PhotoImage(Image.open(resource_path("next.png")))
    play = ImageTk.PhotoImage(Image.open(resource_path("play.png")))