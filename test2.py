import pyaudio
import alsaaudio

from alsaaudio import PCM_PLAYBACK

p = pyaudio.PyAudio()

print(alsaaudio.pcms(pcmtype=PCM_PLAYBACK))

print(p.get_default_output_device_info())

print("\n-----------\n")

def get_default_device(p:pyaudio.PyAudio):
  for i in range(p.get_device_count()):
    if p.get_device_info_by_index(i)["name"] == "default":
      return i
    
print(f"Default device is {get_default_device(p)}")

for i in range(p.get_device_count()):#list all available audio devices
  dev = p.get_device_info_by_index(i)
  print((i,dev['name'],dev['maxInputChannels']))