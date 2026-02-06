import pvporcupine
import os
from pvrecorder import PvRecorder
import picollm
import pvcheetah
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
                res = pllm.generate(prompt='You are Jarvis, a helpful AI assistant. Introduce yourself briefly. be creative and witty.', temperature=.7)
                print(res.completion)
                #print("Jarvis has been summoned.")

        elif keyword_index == 1:
            print ("detected `bumblebee`")
    
    



def initialize_wake_word_detection():
    porcupine = pvporcupine.create(
      access_key= os.environ.get("ACCESS_KEY"),
      keywords=['jarvis', 'bumblebee']
    )
    #this shit really needs to be fixed
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

def initCheetah():
    cheetah = pvcheetah.create(
    access_key = os.environ.get("ACCESS_KEY"),
    endpoint_duration_sec=0.5
    )
    return cheetah

#main()

cheetah = initCheetah()
recorder = PvRecorder(device_index=-1, frame_length=cheetah.frame_length)
recorder.start()

transcript_so_far = ""

while True:
    partial_transcript, is_endpoint = cheetah.process(get_next_audio_frame(recorder))

    # keep everything Cheetah emits during the utterance
    if partial_transcript:
        transcript_so_far += partial_transcript

    if is_endpoint:
        final_transcript = cheetah.flush()
        if final_transcript:
            transcript_so_far += final_transcript

        # print the full utterance, with whitespace cleaned up
        print(" ".join(transcript_so_far.split()))

        # reset for the next utterance
        transcript_so_far = ""
