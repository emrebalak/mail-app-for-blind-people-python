import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import pyaudio
from ctypes import *
from contextlib import contextmanager
import time
from mutagen.mp3 import MP3

import gmail_api
import send_mail
import read_mail


def speak(say):
    """Writes text to a mp3 file and play the sound in english.

    Args:
      say:any text to convert

    """
    tts = gTTS(text=say, lang='en-US')
    filename = 'say.mp3'
    tts.save(filename)
    audio = MP3(filename) # to get audio length
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(audio.info.length)  # wait till programme speaks
    return


def speak_turkish(say):
    """Writes text to a mp3 file and play the sound in turkish

    Args:
      say:any text to convert

    """
    tts = gTTS(text=say, lang='TR')
    filename = 'say_turkish.mp3'
    tts.save(filename)
    audio = MP3(filename) # to get audio length
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    time.sleep(audio.info.length)  # wait till programme speaks
    return


text = ""


def get_audio():
    """Performs speech recognition from source and save it as a text

    Returns:
      Text as perceived. It is stored as string.

    """
    speak("I'm listening'")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I'm listening")
        r.adjust_for_ambient_noise(source, duration=2)
        audio = r.listen(source)
        said = ""

        try:
            said = r.recognize_google(audio, language="en-US")
            print(said)
            global text
            text = said
        except Exception as e:
            print("Exception: " + str(e))
            speak("I couldn't hear you. Try again please")
            get_audio()

    return said


# ERROR HANDLING
ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)


def py_error_handler(filename, line, function, err, fmt):
    pass


c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)


@contextmanager
def noalsaerr():
    asound = cdll.LoadLibrary('libasound.so')
    asound.snd_lib_error_set_handler(c_error_handler)
    yield
    asound.snd_lib_error_set_handler(None)


with noalsaerr():
    p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=44100, output=1)

# Run GMAIL API
service = gmail_api.main()

# Run the programme
speak("How can i help you? I'm able to open inbox, open outbox and send mail.")

count = 0
while True:
    if count != 0:  # If programme have been run before
        speak("Is there anything else that i can help? ")

    get_audio()

    if "inbox" in text:
        speak("I have opened inbox. Now you have 3 options. You can say read last mail, read today's mails or read yesterday's mails.")
        get_audio()
        while True:
            if "last" in text:
                speak("I am reading last message in inbox.")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: inbox')
                message = read_mail.get_message(service, 'me', messagesId[0].get('id'))
                speak_turkish('Mesaj: %s' % (message['snippet']))
                break
            elif "today" in text:
                speak("I am reading today's messages in inbox.")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: inbox AND newer_than:1d')
                i = 0
                for key in messagesId:
                    message = read_mail.get_message(service, 'me', messagesId[i].get('id'))
                    speak_turkish('%s. Mesaj: %s' % (i + 1, message['snippet']))
                    i += 1
                break
            elif "yesterday" in text:
                speak("I am reading messages left from yesterday in inbox")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: inbox AND newer_than:2d')
                i = 0
                for key in messagesId:
                    message = read_mail.get_message(service, 'me', messagesId[i].get('id'))
                    speak_turkish('%s . Mesaj: %s' % (i + 1, message['snippet']))
                    i += 1
                break
            else:
                speak("You said " + text)
                speak("Please tell me that i can help")
                get_audio()
        count += 1  # increment counter before exit
    elif "outbox" in text or "Xbox" in text or "sent" in text:
        print("okay i will open outbox")
        speak("I have opened outbox. Now you have 3 options. You can say read last mail, read today's mails or read yesterday's mails.")
        get_audio()
        while True:
            if "last" in text:
                speak("I am reading last message in outbox.")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: sent')
                message = read_mail.get_message(service, 'me', messagesId[0].get('id'))
                speak_turkish('Mesaj: %s' % (message['snippet']))
                break
            elif "today" in text:
                speak("I am reading today's messages in outbox.")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: sent AND newer_than:1d')
                i = 0
                for key in messagesId:
                    message = read_mail.get_message(service, 'me', messagesId[i].get('id'))
                    speak_turkish('%s. Mesaj: %s' % (i + 1, message['snippet']))
                    i += 1
                break
            elif "yesterday" in text:
                speak("I am reading messages left from yesterday in outbox")
                messagesId = read_mail.list_messages_matching_query(service, 'me', 'label: sent AND newer_than:2d')
                i = 0
                for key in messagesId:
                    message = read_mail.get_message(service, 'me', messagesId[i].get('id'))
                    speak_turkish('%s. Mesaj: %s' % (i + 1, message['snippet']))
                    i += 1
                break
            else:
                speak("You said " + text)
                speak("Please tell me that i can help")
                get_audio()
        count += 1  # increment counter before exit
    elif "mail" in text:
        speak("I am ready to send mail. Please write recipient mail: ")
        to = input("Write recipient mail: ")
        while True:
            speak("Tell me the subject snippet ")
            subject = get_audio()
            speak('Subject is ' + subject)
            speak("If subject is correct say, yes!")
            get_audio()
            if 'yes' in text or 'Yes' in 'text':
                break
        while True:
            speak("Tell me the body of your message ")
            body = get_audio()
            speak('Body is ' + body)
            speak("If subject is correct say, yes!")
            get_audio()
            if 'yes' in text or 'Yes' in 'text':
                break
        message = send_mail.create_message('emrebalak@gmail.com', to, subject, body)
        send_mail.send_message(service, 'me', message)
        count += 1  # increment counter before exit
    elif "stop" in text:
        speak("Good Bye.")
        print("Good Bye.")
        break
    else:
        speak("You said " + text)
        speak("Please tell me that i can help")
        print("Please tell me that i can help")
