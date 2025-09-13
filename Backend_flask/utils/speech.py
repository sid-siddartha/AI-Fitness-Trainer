import pyttsx3
import threading

def speak_text(text):
    def _speak():
        tts = pyttsx3.init()
        tts.say(text)
        tts.runAndWait()
    threading.Thread(target=_speak, daemon=True).start()
