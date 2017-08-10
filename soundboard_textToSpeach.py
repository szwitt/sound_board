# Need to install pip install git+https://github.com/jpercent/pyttsx.git


"""
import pyttsx3
engine = pyttsx3.init()
engine.say("I am talking now ");
engine.setProperty('rate',100)
engine.runAndWait();
"""

"""
audio_file = "hello.mp3"
tts = gTTS(text="Hello Imig", lang="en")
tts.save(audio_file)
return_code = subprocess.call(["afplay", audio_file])
"""

import subprocess
from gtts import gTTS


def convert_text_to_audio(text_to_convert):
    audio_file = ("%s.mp3" % (text_to_convert[:20]))
    tts = gTTS(text=text_to_convert, lang="en")
    tts.save(audio_file)
    return_code = subprocess.call(["mpg123", audio_file]) # mpg123 is the local audio player
    return return_code

convert_text_to_audio('Hello world')
