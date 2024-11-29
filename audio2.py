import wave
import sys
import signal
import audioop

CHUNK = 1024

#if len(sys.argv) < 2:
#    print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#    sys.exit(-1)

import pasimple

with wave.open("temp.wav", 'rb') as wave_file:
    format = pasimple.width2format(wave_file.getsampwidth())
    channels = wave_file.getnchannels()
    sample_rate = wave_file.getframerate()
    #audio_data = wave_file.readframes(wave_file.getnframes())

    chunked_file = []

    while len(data := wave_file.readframes(CHUNK)):  # Requires Python 3.8+ for :=
        chunked_file.append(data)

SAMPLE_WIDTH = pasimple.format2width(format)
BPS = channels * sample_rate * SAMPLE_WIDTH

pa_stream = pasimple.PaSimple(pasimple.PA_STREAM_PLAYBACK, format, channels, sample_rate, app_name="pasimple-test", stream_name="stream-name-ph", maxlength=BPS//10, minreq=BPS//10, prebuf=BPS//10, tlength=BPS//10)

running = True
def sigint_handler(sig, frame):
    global running
    print('\rStopping...')
    running = False
signal.signal(signal.SIGINT, sigint_handler)

for i in range(len(chunked_file)):
    if not running: break
    try:
        print(f"Progress: {i}/{len(chunked_file)} ({(i/len(chunked_file))*100})")
    except: pass
    data = audioop.mul(chunked_file[i], 2, 0.5)
    pa_stream.write(data)

