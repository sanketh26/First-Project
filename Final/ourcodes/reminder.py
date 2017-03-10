import time
from time import strftime
import naogooglestt as stt
from naoqi import ALProxy

def reminder():
	IP = "localhost"
	port = 9559
	
	file = open('rem.txt','w+')
	tts = ALProxy("ALTextToSpeech",IP,port)
	
	remtime = [None] * 2
	
	tts.say("What is your reminder?")
	file.write(stt.stt())		#set the reminder and write it to a text file
	tts.say("When do you want me to remind you?")
	remind = stt.stt()			#set time at which you want the reminder
	remind = remind.split(' ')
	print remind
	if ':' in remind[0]:
		remtime = remind[0].split(':')
		timehour = int(remtime[0])
													#extracting hour part from the time input
	else:
		remtime[0] = remind[0]
		remtime[1] = '00'
		timehour = int(remtime[0])
	
	if(timehour == 12 and remind[1] == 'p.m.'):
		remtimehour = str(timehour)
		
	elif(timehour == 12 and remind[1] == 'a.m.'):
		timehour = timehour - 12
		remtimehour = '0'+str(timehour)
	                                                #handling A.M. and P.M.
	elif(remind[1] == 'p.m.'):
		timehour = timehour + 12
		remtimehour = str(timehour)
		
	elif(remind[1] == 'a.m.'):
		remtimehour = str(timehour)
		if(timehour < 10):
			remtimehour = '0'+remtimehour;
	
	file.close()
	file = open('rem.txt','r')
	
	currtime = strftime('%H:%M:%S') 
	hmstime = currtime.split(':')
	while(hmstime[2] != '00'):
		currtime = strftime('%H:%M:%S') 
		hmstime = currtime.split(':')
		continue
	
	while True:
		currtime = strftime('%H:%M:%S') 
		hmstime = currtime.split(':')
		if(hmstime[0] == remtimehour and hmstime[1] == remtime[1]):		#comparing system time with time input
			data = file.read()
			tts.say(data)			#on above condition becoming true NAO will say out loud the reminder
			break
		time.sleep(60)