import wave
import sys

import pyaudio

CHUNK = 1024

if len(sys.argv) < 2:
    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
    sys.exit(-1)

with wave.open(sys.argv[1], 'rb') as wf:
    # Instantiate PyAudio and initialize PortAudio system resources (1)
    p = pyaudio.PyAudio()
    print(p.get_default_output_device_info())

    print(f"Sample width: {wf.getsampwidth()}\nChannels: {wf.getnchannels()}\nRate: {wf.getframerate()}")
    

    # Open stream (2)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    chunked_file = []

    # Play samples from the wave file (3)
    while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
        chunked_file.append(data)

    for i in range(len(chunked_file)):
        try:
            print(f"Progress: {i}/{len(chunked_file)} ({(i/len(chunked_file))*100})")
        except: pass
        stream.write(chunked_file[i])

    # Close stream (4)
    stream.close()

    # Release PortAudio system resources (5)
    p.terminate()