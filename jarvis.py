import pvporcupine
import os
from pvrecorder import PvRecorder
import picollm
def main():
    print("Starting Jarvis voice assistant...")
    porcupine, recorder = initialize_wake_word_detection()
    while True:
        audio_frame = get_next_audio_frame(recorder)
        keyword_index = porcupine.process(audio_frame)
        if keyword_index == 0:
            print ("detected `jarvis`")
            pllm = initLLM()
            if pllm:
                #todo: add conversation history
                #todo: add speech to text
                #todo: add text to speech
                #todo: add context awareness maybe?
                #todo: add more advanced prompt engineering
                #todo intent recognition for changing models
                res = pllm.generate(prompt='You are Jarvis, a helpful AI assistant. Introduce yourself briefly.')
                print(res.completion)
                #print("Jarvis has been summoned.")

        elif keyword_index == 1:
            print ("detected `bumblebee`")
    
    



def initialize_wake_word_detection():
    porcupine = pvporcupine.create(
      access_key= os.environ.get("ACCESS_KEY"),
      keywords=['jarvis', 'bumblebee']
    )
    #make this a start recording function, and make a stop recording function
    recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)
    recorder.start()
    return porcupine, recorder


def get_next_audio_frame(recorder):
  return recorder.read()



def initLLM():
    pllm = picollm.create(
    access_key = os.environ.get("ACCESS_KEY"),
    model_path ='llama-3.2-3b-instruct-505.pllm')
    return pllm

main()