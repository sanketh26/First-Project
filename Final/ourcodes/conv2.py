#Final Test

import os

import naogooglestt as stt

from naoqi import ALProxy

import json

import re

import reminder as rem

import ir

import googleocrfinal as read

from watson_developer_cloud import ConversationV1



conversation = ConversationV1(

  username='77506896-a41e-41fc-8a7d-136654c16ba5',

  password='uphkLiI6IN8D',

  version='2017-02-03'

)

context = {}



workspace_id = 'bcff13af-48e5-4db1-a874-bdaafb577b47'



IP = "localhost"

port = 9559



tts = ALProxy("ALTextToSpeech",IP,port)

aup = ALProxy("ALAudioPlayer",IP,port)

regexValue = re.compile('(.+?).py')

flag = 0

global flag

converseText = stt.stt()

print converseText


while(1):
    
    	if not converseText:
        	tts.say("Didn't hear anything!")
        	converseText = stt.stt()
        	continue

	with open('robocon_script.json') as data_file:    

		jsonText = json.load(data_file)


	for key in jsonText.keys():	

		if(re.search(r'\b'+re.escape(converseText)+r'\b',key,re.IGNORECASE)):

			if regexValue.search(jsonText[key]):

				os.system(jsonText[key])

				flag = 1

			else:

				tts.say(str(jsonText[key]))

				flag = 1

		

    	if flag == 0:

		response = conversation.message(

			workspace_id=workspace_id,

			message_input={'text':converseText},

			context=context

		)

		print converseText

		context=response['context']

		print '#' + response['intents'][0]['intent']

		#print 'Visited:',response['output']['nodes_visited'][0]

		if response['intents'][0]['intent']=='searchweb':

			searchquery = converseText.split(' ', 1)[1]

			ir.searchweb(searchquery)

		elif response['intents'][0]['intent']=='reminder':

			rem.reminder()

		elif response['intents'][0]['intent']=='reading':

			read.read()

        	elif response['intents'][0]['intent']=='bye':
            
            		tts.say(str(response['output']['text'][0]))
                
            		break


		else:

			tts.say(str(response['output']['text'][0]))

            #print(json.dumps(response, indent=2))

	converseText = stt.stt()

	flag = 0
