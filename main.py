url = ''
apikey = ''

from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# AUTHENTICATOR
# Setup Service
authenticator = IAMAuthenticator(apikey)
# New TTS Service
tts = TextToSpeechV1(authenticator=authenticator)
# Set Service URL
tts.set_service_url(url)

options = ["Input a string for audio", "Convert a txt file to audio"]

def main():
    for i in range(len(options)):
        print(str(i + 1) + ":", options[i])
    inp = int(input("Enter a number: "))
    if inp in range(1, len(options)+1):
        #inp = options[inp-1]
        if inp == 1:
            string_to_audio()
        elif inp == 2:
            txt_convert()
    else:
        print("Invalid input!")


def string_to_audio():
    string = input("Enter a string to be converted to audio: ")
    audio_convert(string)

# Convert from a txt file
def txt_convert():
    with open('test_speech.txt', 'r') as f:
        text = f.readline()
        text = [line.replace('\n', '') for line in text]
        text = ''.join(str(line) for line in text)
        audio_convert(text)

# Create mp3 file with English voice
def audio_convert(string):
    with open('./speech.mp3', 'wb') as audio_file:
        res = tts.synthesize(string, accept='audio/mp3', voice='en-US_AllisonV3Voice').get_result()
        audio_file.write(res.content)

if __name__ == "__main__":
    main()