import pyaudio
import threading
import time
from classes.song import Song
from classes.images import Images
from classes.window import Window

class Player:
    QUEUE:list[Song] = []
    PA = pyaudio.PyAudio()
    CHUNK = 512
    PLAYING = False
    song:Song = Song("", "", "", "", 0, "")

    def __init__(self) -> None:
        pass

    def play_song(self):
        stream = self.PA.open(format=self.PA.get_format_from_width(self.song.seg.sample_width),
                              channels=self.song.seg.channels,
                              rate=self.song.seg.frame_rate,
                              output=True)
        
        while self.song.progress < self.song.length:
            while not self.PLAYING:
                time.sleep(0.1)
            stream.write(self.song.chunked_file[self.song.progress]._data)
            self.song.progress += 1
        
        stream.close()
        self.song.finished_playing = True

    def toggle_pause(self):
        if self.PLAYING:
            Window.pause_label.configure(image=Images.play)
        else:
            Window.pause_label.configure(image=Images.pause)
            if not self.song or self.song.finished_playing:
                if self.QUEUE == []: return
                self.song = self.QUEUE[0]
                self.QUEUE.pop(0)
                self.song.load()
                
                thread = threading.Thread(target=self.play_song)
                thread.start()

        self.PLAYING = not self.PLAYING