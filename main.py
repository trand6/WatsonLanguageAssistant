# This program will help convert and/or translate speech and text.
# To add next time:
# - Choose a language to translate to and/or from

# TEXT TO SPEECH
TTS_url = ''
TTS_apikey = ''

# SPEECH TO TEXT
STT_url = ''
STT_apikey = ''

# LANGUAGE TRANSLATOR
LT_url = ''
LT_apikey = ''

from ibm_watson import TextToSpeechV1, SpeechToTextV1, LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# AUTHENTICATOR
# Setup Service
tts_authenticator = IAMAuthenticator(TTS_apikey)
stt_authenticator = IAMAuthenticator(STT_apikey)
lt_authenticator = IAMAuthenticator(LT_apikey)

# New Services
tts = TextToSpeechV1(authenticator=tts_authenticator)
stt = SpeechToTextV1(authenticator=stt_authenticator)
lt = LanguageTranslatorV3(version='2018-05-01', authenticator=lt_authenticator)

# Set Service URL
tts.set_service_url(TTS_url)
stt.set_service_url(STT_url)
lt.set_service_url(LT_url)

options = ["Input a string for audio", "Convert a text file to audio", "Convert audio to text", "Translate a string",
           "Translate a text file", "End program"]

def main():
    for i in range(len(options)):
        print(str(i + 1) + ":", options[i])
    inp = int(input("Enter a number: "))
    if inp in range(1, len(options)+1):
        if inp == 1:
            string_to_audio()
        elif inp == 2:
            txt_convert()
        elif inp == 3:
            speech_to_text()
        elif inp == 4:
            string_to_translate()
        elif inp == 5:
            txt_translate()
        elif inp == 6:
            quit()
    else:
        print("Invalid input!")


def string_to_audio():
    string = input("Enter a string to be converted to audio: ")
    audio_convert(string)

def string_to_translate():
    string = input("Enter a string to be translated: ")
    text_translate(string)

def text_translate(string):
    translation = lt.translate(string, model_id='en-zh-TW').get_result()
    text = translation['translations'][0]['translation']
    audio_translate(text)

# Formatting a txt file to proper paragraph
def txt_convert():
    with open('output.txt', 'r') as f:
        text = f.readline()
        text = [line.replace('\n', '') for line in text]
        text = ''.join(str(line) for line in text)
        audio_convert(text)

# Formatting txt file before translating to Chinese
def txt_translate():
    with open('output.txt', 'r') as f:
        text = f.readline()
        text = [line.replace('\n', '') for line in text]
        text = ''.join(str(line) for line in text)
        translation = lt.translate(text, model_id='en-zh-TW').get_result()
        text = translation['translations'][0]['translation']
        audio_translate(text)

# Create mp3 file with English voice
def audio_convert(string):
    with open('./speech.mp3', 'wb') as audio_file:
        res = tts.synthesize(string, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
        audio_file.write(res.content)
        print("Audio creation complete. Please check your folder.")

# Create mp3 file with Chinese translation
def audio_translate(string):
    with open('./speech.mp3', 'wb') as audio_file:
        res = tts.synthesize(string, accept='audio/mp3', voice='zh-CN_LiNaVoice').get_result()
        audio_file.write(res.content)
    print("Audio translation complete. Please check your folder.")

# Create txt file using mp3
def speech_to_text():
    with open('./speech.mp3', 'rb') as f:
        res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel',
                            continuous=True).get_result()
        text = res['results'][0]['alternatives'][0]['transcript']
        with open('output.txt', 'w') as out:
            out.writelines(text)
            print("Speech to text complete. Please check your folder.")

# Create language model
def language_translate(lang1, lang2):
    pass

if __name__ == "__main__":
    main()