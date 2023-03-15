from pydub import AudioSegment
from pydub.utils import make_chunks
from PIL import Image as PILImg

class Song:
    source:str
    title:str
    author:str
    album:str
    length:int
    length_secs:int
    image:PILImg
    link:str
    seg:AudioSegment
    chunked_file:list[AudioSegment]
    progress:int
    finished_playing:bool = True

    def load(self):
        if self.source in ("wav", "mp3", "aac", "mp4", "ogg"):
            self.seg = AudioSegment.from_file(file=self.link, format=self.source)
        elif self.source == "spotify":
            #spotify implementation
            pass
        elif self.source == "youtube":
            #youtube implementation
            pass

        self.chunked_file = make_chunks(self.seg, 100)
        self.length = len(self.chunked_file)
        self.finished_playing = False
        self.progress = 0

    def __init__(self, source:str, title:str, author:str, album:str, length:int, link:str, image:PILImg) -> None:
        self.source = source
        self.title = title
        self.author = author
        self.album = album
        self.length_secs = length
        self.link = link
        self.image = image