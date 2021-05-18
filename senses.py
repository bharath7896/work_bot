import speech_recognition as sr
import pyttsx3

# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()
r.energy_threshold = 4000


def listen_speech():
    with sr.Microphone() as source:
        print("Listening....")
        audio_text = r.listen(source, timeout=5, phrase_time_limit=4)
        # recoginizer() method will throw a request error if the API is unreachable, hence using exception handling

        try:
            print("Jarvis thinks you said " + r.recognize_google(audio_text))
            return r.recognize_google(audio_text)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            listen_speech()
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))
            listen_speech()


def speak(text):
    """
    :param text: input text that needs to be spoke
    :return: speech
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


user_speech = listen_speech()

