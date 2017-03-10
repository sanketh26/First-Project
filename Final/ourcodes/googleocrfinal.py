import io
import json
from google.cloud import vision
import os
import sys
import time
from naoqi import ALProxy

def read():
	IP = '127.0.0.1'
	PORT = 9559

	# Create a proxy to ALPhotoCapture
	try:
		photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
		leds=ALProxy("ALLeds","localhost",9559)
	except Exception, e:
		print "Error when creating proxy:"
		print str(e)
		exit(1)

	photoCaptureProxy.setResolution(2)
	photoCaptureProxy.setPictureFormat("jpg")
	leds.setIntensity("LeftFaceLedsRed",1)
	leds.setIntensity("LeftFaceLedsGreen",0)
	leds.setIntensity("LeftFaceLedsBlue",0)

	leds.setIntensity("RightFaceLedsRed",1)
	leds.setIntensity("RightFaceLedsGreen",0)
	leds.setIntensity("RightFaceLedsBlue",0)

	photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")		#NAO captures an image
	leds.on("FaceLeds")

	tts=ALProxy('ALTextToSpeech',"localhost",9559)

	vision_client = vision.Client.from_service_account_json('/home/nao/ourcodes/MyFirstProject-47fa9e048ac2.json')

	path = '/home/nao/recordings/cameras/image.jpg'
	
	with io.open(path, 'rb') as image_file:
		content = image_file.read()

	image = vision_client.image(content=content)
	texts = image.detect_text()			# image sent to Google for OCR
	file=open("op.txt",'w')
	file.write(str(texts[0].description))			#text obtained from OCR written to text file
	file.close()
	print texts[0].description
	file=open("op.txt",'r')				#text read from file
	data=file.readlines()
	for line in data:
		tts.say(line)			#NAO says out loud the text
