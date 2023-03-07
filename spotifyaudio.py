import pyaudio
import wave

from librespot.core import Session
from librespot.metadata import TrackId
from librespot.audio.decoders import AudioQuality, VorbisOnlyAudioQuality

CHUNK = 50000
SESSION: Session = Session.Builder().stored_file().create()

p = pyaudio.PyAudio()

track_id = TrackId.from_uri("spotify:track:6NAmbftWAovcMCnJzDCFsU")
spotify_stream = SESSION.content_feeder().load(track_id, VorbisOnlyAudioQuality(AudioQuality.HIGH), False, None)
total_size = spotify_stream.input_stream.size
downloaded = 0

with open("./temp.wav", "wb") as file:
    _CHUNK = CHUNK
    while downloaded < total_size:
        data = spotify_stream.input_stream.stream().read(_CHUNK)

        downloaded += len(data)
        file.write(data)

        if (total_size - downloaded) < _CHUNK:
            _CHUNK = total_size - downloaded
        
print("file download complete")

with wave.open("temp.wav", 'rb') as wf:
    # Open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # Play samples from the wave file (3)
    while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
        stream.write(data)

    # Close stream (4)
    stream.close()

    # Release PortAudio system resources (5)
    p.terminate()