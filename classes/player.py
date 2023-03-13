import pyaudio
from classes.song import Song
from classes.images import Images
from classes.window import Window

class Player:
    QUEUE:list[Song] = []
    PA = pyaudio.PyAudio()
    CHUNK = 512
    PLAYING = False

    def __init__(self) -> None:
        pass

    def load_song(song:Song):
        
        pass

    def toggle_pause(self):
        if self.PLAYING:
            Window.pause_label.configure(image=Images.play)
        else:
            Window.pause_label.configure(image=Images.pause)

        self.PLAYING = not self.PLAYING