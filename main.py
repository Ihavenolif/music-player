import modules.window as Window

from modules.song import Song
from modules.player import init_player

player = init_player()

Window.set_global_player_reference(player)

Window.TK.bind("<space>", lambda e:Window.toggle_pause())
Window.pause_label.bind("<Button-1>", lambda e:Window.toggle_pause())
Window.next_label.bind("<Button-1>", lambda e:Window.skip_song())

Window.start_loop()