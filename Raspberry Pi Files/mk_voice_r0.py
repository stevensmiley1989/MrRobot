from gtts import gTTS
import os
from pydub import AudioSegment
from pydub.playback import play
import pydub as pydub
import numpy as np
import time
def make_voice(rq):
    while True:
        try:
            text=rq.get(False)
            random_num=str(np.random.randint(1000))
            filename='text_'+random_num+'.mp3'
            language = 'en'
            speech = gTTS(text=text,lang=language, slow=True)
            speech.save(filename)

            sound = AudioSegment.from_mp3(filename)
            play(sound)
            #pydub.playback._play_with_simpleaudio(sound)

            #os.system('omxplayer -o alsa {}'.format(filename))
            os.system('rm {}'.format(filename))

        except:
            pass
        
def make_voice_once(text):
        try:
            #text=rq.get(False)
            random_num=str(np.random.randint(1000))
            filename='text_'+random_num+'.mp3'
            language = 'en'
            speech = gTTS(text=text,lang=language, slow=True)
            speech.save(filename)

            sound = AudioSegment.from_mp3(filename)
            play(sound)
            #pydub.playback._play_with_simpleaudio(sound)

            #os.system('omxplayer -o alsa {}'.format(filename))
            os.system('rm {}'.format(filename))

        except:
            pass