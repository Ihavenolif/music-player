import tkinter as tk
from PIL import ImageTk, Image

window = tk.Tk()
#window.geometry("700x500")

pause_image = ImageTk.PhotoImage(Image.open("pepeJAM.png"))

music_control = tk.Frame()
pause = tk.Label(image=pause_image)
pause.pack()

greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()

window.mainloop()