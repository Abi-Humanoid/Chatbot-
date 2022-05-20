#This file has the entire chatbot system, but requires manual recording of files
#Uses huggingface models for STT and machine learning
#Uses Google speech to text API for TTS

#For sound file IO:
from playsound import playsound
playsound('abi_out.mp3')


#ASR Section

import requests
import json

API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"
headers = {"Authorization": "Bearer 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"}

def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))

stt_output = query("inception.mp3")
stt_output = stt_output['text'].lower()
print(stt_output)

#Machine learning section:
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot_small-90M"
headers = {"Authorization": "Bearer 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"}
user_statement = stt_output
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

output = query({
    "inputs": {
        "past_user_inputs": [user_statement],
        "generated_responses": [""],
        "text": "Can you explain why ?"
    },
})

print("Abi: ", output['generated_text'])
abi_text = output['generated_text']


#STT section
# Import the required module for text
# to speech conversion
from gtts import gTTS
  
# This module is imported so that we can
# play the converted audio
import os
  
# The text that you want to convert to audio
mytext = abi_text
  
# Language in which you want to convert
language = 'en'
  
# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
  
# Saving the converted audio in a mp3 file named
# welcome
myobj.save("abi_out.mp3")
  
# Playing the converted file
os.system("abi_out.mp3")



