from google.cloud import speech
from naoqi import ALProxy
import time as t

def stt():
	speech_client = speech.Client.from_service_account_json('/home/nao/ourcodes/MyFirstProject-47fa9e048ac2.json')

	tts = ALProxy("ALTextToSpeech","localhost",9559)
	tts.resetSpeed()

	channels = []

	channels.append(0)
	channels.append(0)
	channels.append(1)
	channels.append(0)

	rec = ALProxy("ALAudioRecorder","localhost",9559)
	leds = ALProxy("ALLeds","localhost",9559)

	rec.startMicrophonesRecording("/home/nao/ourcodes/test.wav", "wav", 16000, channels)

	leds.rotateEyes(0x000000FF,1,5)

	rec.stopMicrophonesRecording()
	leds.on("FaceLeds")

	with open("/home/nao/ourcodes/test.wav", 'rb') as audio_file:
			content = audio_file.read()
			audio_sample = speech_client.sample(
				content=content,
				source_uri=None,
				encoding='LINEAR16',
				sample_rate=16000)
			try:
				alternatives = speech_client.speech_api.sync_recognize(audio_sample,language_code='en-IN')
				return (str(alternatives[0].transcript))
			except ValueError:
    				return ""	

