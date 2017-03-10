import pprint,sys
from os.path import join, dirname
import json
from watson_developer_cloud import VisualRecognitionV3 as vr
import socket
from naoqi import ALProxy
import time as t

# Replace this with your robot's IP address
IP = '127.0.0.1'
PORT = 9559

# Create a proxy to ALPhotoCapture
try:
    photoCaptureProxy = ALProxy("ALPhotoCapture", IP, PORT)
    leds=ALProxy("ALLeds",IP,PORT)
    tts=ALProxy('ALTextToSpeech',IP,PORT)
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

photoCaptureProxy.takePictures(1, "/home/nao/recordings/cameras/", "image")			#NAO captures an image
leds.on("FaceLeds")

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
host = '172.16.133.83'     # Get local machine name
port = 60000                    # Reserve a port for your service.
s.connect((host, port))

file = open('/home/nao/recordings/cameras/image.jpg','rb')
data = file.read(512)
while data:
    s.send(data)			#send image to proxy server for processing
    data = file.read(512)
file.close()
s.close()

s1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)             # Create a socket object
host = '172.16.133.83'
port = 65000
t.sleep(1)
s1.connect((host, port))

file1 = open("test.txt",'w+')
data1 = s1.recv(512)
while data1:
	file1.write(data1)
	data1 = s1.recv(512)			#receive result from proxy server
file1.close()
s1.close()

file1 = open("test.txt",'r')
data=file1.readlines()
for line in data:
    print line
    tts.say(line)			#NAO says out loud the result
file1.close()
