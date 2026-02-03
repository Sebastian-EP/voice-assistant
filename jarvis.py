import pvporcupine
import os
from pvrecorder import PvRecorder

porcupine = pvporcupine.create(
  access_key= os.environ.get("ACCESS_KEY"),
  keywords=['jarvis', 'bumblebee']
)
#make this a start recoeding function, and make a stop recording function
recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
recorder.start()


def get_next_audio_frame():
  return recorder.read()

while True:
  audio_frame = get_next_audio_frame()
  keyword_index = porcupine.process(audio_frame)
  if keyword_index == 0:
      print ("detected `jarvis`")
  elif keyword_index == 1:
      print ("detected `bumblebee`")

