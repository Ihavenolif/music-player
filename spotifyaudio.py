import pyaudio
import wave

from pydub import AudioSegment
from librespot.core import Session
from librespot.metadata import TrackId
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

SPOTIFY_CHUNK_SIZE = 50000
PLAYER_CHUNK_SIZE = 1024
SESSION: Session = Session.Builder().stored_file().create()

p = pyaudio.PyAudio()

track_id = TrackId.from_uri("spotify:track:6NAmbftWAovcMCnJzDCFsU")
spotify_stream = SESSION.content_feeder().load(track_id, VorbisOnlyAudioQuality(AudioQuality.HIGH), False, None)
total_size = spotify_stream.input_stream.size
downloaded = 0

def convert_audio_format(filename):
    """ Converts raw audio into playable mp3 or ogg vorbis """
    #print("###   CONVERTING TO " + MUSIC_FORMAT.upper() + "   ###")
    raw_audio = AudioSegment.from_file(filename, format="ogg",
                                       frame_rate=44100, channels=2, sample_width=2)
    bitrate = "160k"
    raw_audio.export("temp.mp3", format="mp3", bitrate=bitrate)

    raw_audio = AudioSegment.from_file("temp.mp3", format="mp3",
                                       frame_rate=44100, channels=2, sample_width=2)
    bitrate = "160k"
    raw_audio.export("temp.wav", format="wav", bitrate=bitrate)

def download_track():
                    total_size = spotify_stream.input_stream.size
                    downloaded = 0
                    _SPOTIFY_CHUNK_SIZE = SPOTIFY_CHUNK_SIZE
                    fail = 0
                    with open("temp.wav", 'wb') as file:
                        while downloaded <= total_size:
                            data = spotify_stream.input_stream.stream().read(_SPOTIFY_CHUNK_SIZE)

                            downloaded += len(data)
                            file.write(data)
                            #print(f"[{total_size}][{_SPOTIFY_CHUNK_SIZE}] [{len(data)}] [{total_size - downloaded}] [{downloaded}]")
                            if (total_size - downloaded) < _SPOTIFY_CHUNK_SIZE:
                                _SPOTIFY_CHUNK_SIZE = total_size - downloaded
                            if len(data) == 0 : 
                                fail += 1                                
                            if fail > 30:
                                break

download_track()   
convert_audio_format("temp.wav")
        
print("file download complete")

with wave.open("temp.wav", 'rb') as wf:
    # Open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Play samples from the wave file (3)
    while len(data := wf.readframes(PLAYER_CHUNK_SIZE)):  # Requires Python 3.8+ for :=
        stream.write(data)

    # Close stream (4)
    stream.close()

    # Release PortAudio system resources (5)
    p.terminate()