# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 17:33:17 2019

@author: boner
"""

import speech_recognition as sr
import sys

r = sr.Recognizer()
mic = sr.Microphone()

# List of flagged words.
dangerous_words_list = ['help',
                        'runaway',
                        'getout',
                        'goaway',
                        'callthepolice',
                        'callpolice',
                        'somebodyhelp',
                        'someonehelp',
                        'stop',
                        'hurt',
                        'hurts',
                        'hurting',
                        'hellomachine']


# Listens for phrases using the specified microphone.
# Params:
#   source: the sr.Microphone() instance to listen with
# Returns:
#   text (str): the String (with spaces) of text that it heard
def listen_for_phrase(source):
    
    try:
        # Adjust for ambient noise (1 sec)
        r.adjust_for_ambient_noise(source)
        
        # Indicate that we're live.
        sys.stdout.write('\rRecording....')
        sys.stdout.flush()
        
        # Listen for key words, timeout after 3 secodns to keep things fresh
        # and readjust for ambient noise. 
        # Time out phrases after 2 seconds to stop long, drawn out sentences.
        # The expectation is that people in danger won't be talking for long.
        audio = r.listen(source, timeout=3, phrase_time_limit=2)
        
        sys.stdout.write('\rProcessing...')
        sys.stdout.flush()
        
        # Process the text using Google's Speech Recognition API.
        text = r.recognize_google(audio).lower()
    
    # Check to see if Google couldn't figure out the word.
    except sr.UnknownValueError:
        text = ""
    # Check to see if our listening period didn't hear anything.
    except sr.WaitTimeoutError:
        sys.stdout.write('\rProcessing...')
        sys.stdout.flush()
        text = ""
    # Check to see if reaching the API failed.
    except sr.RequestError:
        text = ""
        print('API Unreachable. Try again.')
    
    return text

def call_the_police(text):
    print("\n\nDangerous word detected!: {}\n".format(text))

# identifies words in the dangerous_words_list
# Params:
#   source: The sr.Microphone() instance used to listen.
def run(source):

    text = listen_for_phrase(source)
    
    # Get rid of spaces (keeps consistency)
    stripped = text.replace(" ","")
    
    # Check if one of the words in dangerous_words_list were said.
    if any(word in stripped.lower() for word in dangerous_words_list):
        call_the_police(text)
    
    # If the text wasn't in the dangerous words list, AND it isn't empty, print it.
    elif(text != ""):
        print("\n"+text+"\n")

# Continuously run mainfunction
if __name__ == '__main__':
    with mic as source:
        print("Up and running!")
        while(True):
            run(source)
        