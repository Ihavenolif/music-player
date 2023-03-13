from pydub import AudioSegment
from pydub.utils import make_chunks
import pyaudio

soundfile:AudioSegment = AudioSegment.from_file(file="temp.wav", format="wav")

chunked_file = make_chunks(soundfile, 100)

p = pyaudio.PyAudio()

stream = p.open(format=p.get_format_from_width(soundfile.sample_width),
                    channels=soundfile.channels,
                    rate=soundfile.frame_rate,
                    output=True)

for i in range(len(chunked_file)):
    try:
        print(f"Progress: {i}/{len(chunked_file)} ({(i/len(chunked_file))*100})")
    except: pass
    stream.write(chunked_file[i]._data)