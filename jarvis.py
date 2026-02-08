import pvporcupine
import os
from pvrecorder import PvRecorder
import picollm
import pvcheetah
import pvorca
from pvspeaker import PvSpeaker

def main():
    print("Starting Jarvis voice assistant...")
    
    
    porcupine, recorder = initialize_wake_word_detection()
    pllm = initLLM()
    
    cheetah = initCheetah()
    orca = initOrca()
    speaker = PvSpeaker(sample_rate=orca.sample_rate, bits_per_sample=16)
    speaker.start()
    
    



    print("Jarvis is listening for the wake word...")
    while True:
        
        
        audio_frame = get_next_audio_frame(recorder)
        keyword_index = porcupine.process(audio_frame)
        if keyword_index == 0:
            print ("detected `jarvis`")
            
            if pllm:
                #todo: add conversation history
                #todo: add speech to text
                print ("Listening for command...")
                #todo: add text to speech
                #todo: add context awareness maybe?
                #todo: add more advanced prompt engineering
                #todo intent recognition for changing models
                sebSaid = listenCheetah(cheetah)
                print(sebSaid)
                res = pllm.generate(prompt=sebSaid, temperature=.7, completion_token_limit=75)
                print(res.completion)
                speakOrca(orca, speaker, res.completion)

                #print("Jarvis has been summoned.")

        elif keyword_index == 1:
            #print ("detected `bumblebee`")
            sebSaid = listenCheetah()
            print(f"Bumblebee heard: {sebSaid}")
    
    



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



def listenCheetah(cheetah):

    
    cheetahRecorder = PvRecorder(device_index=-1, frame_length=cheetah.frame_length)
    cheetahRecorder.start()

    transcript_so_far = ""

    while True:
        partial_transcript, is_endpoint = cheetah.process(get_next_audio_frame(cheetahRecorder))

        # keep everything Cheetah remits during the utterance
        if partial_transcript:
            transcript_so_far += partial_transcript

        if is_endpoint:
            final_transcript = cheetah.flush()
            if final_transcript:
                transcript_so_far += final_transcript

                # print the full utterance, with whitespace cleaned up
                #print(" ".join(transcript_so_far.split()))
                return (" ".join(transcript_so_far.split()))
                # reset for the next utterance
                #transcript_so_far = ""

def initOrca():
    orca = pvorca.create(
        access_key=os.environ.get("ACCESS_KEY"),
        # model_path is optional. If you want a specific voice/language, pass a .pv model file path:
        # model_path="/path/to/orca_model.pv"
    )
    return orca

def speakOrca(orca, speaker, text: str):
    stream = orca.stream_open()

    pcm = stream.synthesize(text)
    if pcm is not None:
        speaker.write(pcm)   # <-- play the whole buffer

    pcm = stream.flush()
    if pcm is not None:
        speaker.write(pcm)

    stream.close()



if __name__ == "__main__":    main()