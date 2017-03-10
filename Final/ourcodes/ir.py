# -*- coding: utf-8 -*-
import urllib
import re
from naoqi import ALProxy

def searchweb(searchquery):
        
    url = 'http://www.bing.com/search?q='
    
    #searchquery = raw_input('Enter search query: ')
    
    url = url + searchquery
    
    htmlfile = urllib.urlopen(url)
    
    htmltext = htmlfile.read()
    
    tts = ALProxy('ALTextToSpeech','localhost',9559)
    #print htmltext
    
    if searchquery.startswith(('who','whos','who\'s')) or re.search(r'^[Ww]ho is',searchquery):
        regex = '<div class="b_hide"(.*?)><span>(.+?)</span></div>' #check with .* and .*?

        so = re.search(regex,htmltext,re.M|re.I)
        #print so.group()

        #answer = re.findall(regex,str(htmltext))
        #print answer some weird tuple forms

        sentences = re.split('\.',so.group(2))
    
        print sentences[0]
    
    elif searchquery.startswith(('distance')) or re.search(r'^[Hh]ow far',searchquery):
        regex = '<p class="drHours" data-tag="drDistance">(.+?)</p>'
        answer = re.findall(regex, str(htmltext))
        
        regex ='<p class="drHoursLabel" data-tag="drDistanceLabel">(.+?)</p>'
        answer.append((re.findall(regex,htmltext))[0])
        
        #print answer
    
        print "".join(answer)

    else:
        regex = '<div class="(\w*\s*)b_focusText(Medium|Large|Small)">(.+?)</div>'
        
        #so = re.search(regex,htmltext,re.M|re.I)
        #print so.group()
        
        
        #pattern = re.compile(regex)
        
        answer = re.findall(regex, str(htmltext))
        
        #print answer
        if answer:
            so1 = re.search(r'<a(.*)>(.+?)</a>',answer[0][2],re.M|re.I) #extracting from href
            if so1:
                print  'Answer: ',tts.say(so1.group(2))
            else:
                print 'Answer: ',tts.say(answer[0][2])
        else:
            print 'Sorry. Couldn\'t find anything'
