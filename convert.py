from pydub import AudioSegment

def convert_audio_format(filename):
    """ Converts raw audio into playable mp3 or ogg vorbis """
    #print("###   CONVERTING TO " + MUSIC_FORMAT.upper() + "   ###")
    raw_audio = AudioSegment.from_file(filename, format="mp3",
                                       frame_rate=44100, channels=2, sample_width=2)
    bitrate = "160k"
    raw_audio.export("temp.wav", format="wav", bitrate=bitrate)

convert_audio_format("test.mp3")