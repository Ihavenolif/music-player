from PIL import ImageTk, Image

class Images:
    previous = ImageTk.PhotoImage(Image.open("images/previous.png"))
    pause = ImageTk.PhotoImage(Image.open("images/pause.png"))
    next = ImageTk.PhotoImage(Image.open("images/next.png"))
    play = ImageTk.PhotoImage(Image.open("images/play.png"))