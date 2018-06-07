# sudo apt-get install -y espeak
# sudo apt-get install -y libttspico-utils
import os
import time
import urllib.request
from gtts import gTTS
from google.cloud import texttospeech
from boto3 import client


def espeak(textFile):
    start_time = time.time()
    os.system('espeak --stdout <{}> {}'.format(textFile, "espeak.wav"))
    return time.time() - start_time

def svox_pico(text):
    start_time = time.time()
    os.system('pico2wave -w=svox_pico.wav {}'.format(text))
    #os.system('aplay pico.wav')
    return time.time() - start_time

def google_gtts(text):
    start_time = time.time()
    rec_tts = gTTS(text=text, lang='ko', slow=False)
    rec_tts.save("gtts.mp3")
    #os.system('aplay gtts.mp3')
    return time.time() - start_time

def google_cloud_tts(text):
    start_time = time.time()
    """Synthesizes speech from the input string of text."""
    client = texttospeech.TextToSpeechClient()
    input_text = texttospeech.types.SynthesisInput(text=text)
    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.types.VoiceSelectionParams(
        language_code='ko-KR',
        ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(
        audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = client.synthesize_speech(input_text, voice, audio_config)
    # The response's audio_content is binary.
    with open('google_cloud.mp3', 'wb') as out:
        out.write(response.audio_content)
        # print('Audio content written to file "output.mp3"')
    return time.time() - start_time

def naver_clova(text):
    start_time = time.time()
    client_id = os.getenv('naver_tts_client_id')
    client_secret = os.getenv('naver_tts_client_secret')
    encText = urllib.parse.quote(text)
    data = "speaker=mijin&speed=0&text=" + encText
    url = "https://naveropenapi.apigw.ntruss.com/voice/v1/tts"
    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", client_id)
    request.add_header("X-NCP-APIGW-API-KEY", client_secret)
    response = urllib.request.urlopen(request, data=data.encode('utf-8'))
    rescode = response.getcode()
    if (rescode == 200):
        response_body = response.read()
        with open("naver_clova.mp3", 'wb') as f:
            f.write(response_body)
    else:
        print("Error Code:" + rescode)
    return time.time() - start_time

def aws_polly(text):
    start_time = time.time()
    polly = client("polly", region_name="ap-northeast-2")
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat="mp3",
        VoiceId="Seoyeon")
    stream = response.get("AudioStream")
    with open("aws_polly.mp3", 'wb') as f:
        data = stream.read()
        f.write(data)
    return time.time() - start_time


text = "무엇을 도와드릴까요"
text2 = "'an young ha se yo'"
text3 = "'mu eos-eul do wa deu lil kka yo'"
textFile = "hello.txt"
textFile2 = "mu.txt"

print(" Input Text        >> ", text)
print(" Input(SVOX Pico)  >> ", text3)
print(" espeak            >> ", espeak(textFile2))
print(" SVOX Pico         >> ", svox_pico(text3))
print(" gTTS              >> ", google_gtts(text))
print(" Google Cloud TTS  >> ", google_cloud_tts(text))
print(" Naver Clova       >> ", naver_clova(text))
print(" AWS Polly         >> ", aws_polly(text))
