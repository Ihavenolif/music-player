import platform
import pasimple
import time
import threading
import audioop

from tkinter import ttk
import tkinter as tk

from modules.song import Song

class SongQueue():
    __list:list[Song] = []
    def add(self, song:Song) -> None:
        self.__list.append(song)

    def next(self) -> Song:
        return self.__list.pop(0)
    
    def len(self) -> int:
        return len(self.__list)
    
    def debug_print(self) -> None:
        print("Queue:")
        for x in self.__list:
            x.debug_print()
    
    def is_empty(self) -> bool:
        return self.len() == 0

class Player:
    queue = SongQueue()
    
    paused:bool = True
    active_song:Song = None

    progress_bar:ttk.Progressbar
    progress_bar_val:tk.IntVar
    volume_bar:tk.Scale

    stop_sig = False

    def toggle_pause(self) -> bool:
        self.paused = not self.paused
        return self.paused
    
    def skip_song(self) -> bool:
        if not self.active_song or self.active_song.finished_playing:
            self.load_next()
            return
        self.active_song.progress = self.active_song.length
        return True
    
    def start_playback(self) -> None:
        pass

    def play_song(self) -> None:
        pass

    def player_loop(self) -> None:
        pass

    def load_next(self) -> None:
        if self.queue.is_empty():
            return
        self.active_song = self.queue.next()
        self.active_song.load()
        self.progress_bar.configure(maximum=self.active_song.length)
        self.progress_bar_val.set(0)

    def __init__(self) -> None:
        self.active_song = Song("wav", "Let It Die", "Three Days Grace", "albumph", 300, "./temp.wav")
        self.active_song.load()
        self.player_thread = threading.Thread(target=self.player_loop)
        self.player_thread.start()

class LinuxPlayer(Player):
    def play_song(self) -> None:
        format = pasimple.width2format(self.active_song.seg.sample_width)
        channels = self.active_song.seg.channels
        sample_rate = self.active_song.seg.frame_rate
        bps = channels * sample_rate * self.active_song.seg.sample_width

        stream = pasimple.PaSimple(pasimple.PA_STREAM_PLAYBACK, format, channels, sample_rate, app_name="OSPlayer", stream_name="OSPlayer", maxlength=bps//10, minreq=bps//10, prebuf=bps//10, tlength=bps//10)

        

        while self.active_song.progress <= self.active_song.length:
            while self.paused:
                time.sleep(0.1)

            stream.write(self.active_song.chunked_file[self.active_song.progress]._data)
            self.active_song.progress += 1
            self.progress_bar.step()

        stream.close()
        self.active_song.finished_playing = True
        self.load_next()


    def player_loop(self) -> None:
        format = pasimple.width2format(self.active_song.seg.sample_width)
        channels = self.active_song.seg.channels
        sample_rate = self.active_song.seg.frame_rate
        bps = channels * sample_rate * self.active_song.seg.sample_width

        pastream = pasimple.PaSimple(pasimple.PA_STREAM_PLAYBACK, format, channels, sample_rate, app_name="OSPlayer", stream_name="OSPlayer", maxlength=bps//10, minreq=bps//10, prebuf=bps//10, tlength=bps//10)

        while not self.stop_sig:
            if not self.active_song or self.active_song.finished_playing:
                time.sleep(0.1)
                continue
            
            try:
                while self.active_song.progress < self.active_song.length:
                    if self.stop_sig:
                        break

                    while self.paused:
                        if self.stop_sig:
                            break

                        time.sleep(0.1)
                    
                    data = self.active_song.chunked_file[self.active_song.progress]._data
                    data = audioop.mul(data, self.active_song.seg.sample_width, self.volume_bar.get()/100)
                    pastream.write(data)
                    
                    self.active_song.progress += 1
                    self.progress_bar.step()
            except:
                pass
            self.active_song.finished_playing = True
            self.load_next()

        pastream.close()


    def start_playback(self) -> None:
        if not self.active_song: return
        format = pasimple.width2format(self.active_song.seg.sample_width)
        channels = self.active_song.seg.channels
        sample_rate = self.active_song.seg.frame_rate
        bps = channels * sample_rate * self.active_song.seg.sample_width

        stream = pasimple.PaSimple(pasimple.PA_STREAM_PLAYBACK, format, channels, sample_rate, app_name="OSPlayer", stream_name="OSPlayer", maxlength=bps//10, minreq=bps//10, prebuf=bps//10, tlength=bps//10)

        #pul = pulsectl.Pulse()
        #pul.client_list
        #pul.get_source_by_name()

        while True:
            while not self.active_song.finished_playing:
                if self.stop_sig: return
                if not self.paused:
                    stream.write(self.active_song.chunked_file[self.active_song.progress]._data)
                    self.active_song.progress += 1
                    self.progress_bar.step()
                else:
                    time.sleep(0.1)
            stream.drain()
            if not self.queue.is_empty():
                self.load_next()
        

class WindowsPlayer(Player):
    pass

def init_player() -> Player:
    if platform.system() == "Windows":
        return WindowsPlayer()
    elif platform.system() == "Linux":
        return LinuxPlayer()
    else:
        print("Unsupported platform.")
        exit(1)