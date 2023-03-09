class Song():
    def __init__(self, source:str, title:str, author:str, album:str, length:int) -> None:
        self.source = source
        self.title = title
        self.author = author
        self.album = album
        self.length = int