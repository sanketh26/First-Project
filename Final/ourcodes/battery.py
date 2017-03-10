from naoqi import ALProxy

bat = ALProxy('ALBattery','localhost',9559)
tts = ALProxy('ALTextToSpeech','localhost',9559)

charge = bat.getBatteryCharge()

tts.say(str(charge))
