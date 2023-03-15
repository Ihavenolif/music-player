from PIL import Image

from classes.window import Window
from classes.song import Song
from classes.player import Player

Player.QUEUE.append(Song(source="mp3", title="kokot", author="kokotos", album="albumos", length=330, link="shortened_lorna.mp3", image=Image.new("RGB", (1000,1000), (255,255,255))))
Player.QUEUE.append(Song(source="wav", title="kokot", author="kokotos", album="albumos", length=330, link="temp.wav", image=Image.new("RGB", (1000,1000), (255,255,255))))

Window.pause_label.bind("<Button-1>", lambda e:Player.toggle_pause())
Window.next_label.bind("<Button-1>", lambda e:Player.skip_song())

Window.start_loop()