import urllib2
import re
#import MySQLdb
import time
import string
import sys
import os.path
import mutagen
##########################
##  ANDROID PROMPTS
##########################
#import android
#droid = android.Android() 
#username = str(droid.getInput("please enter your hype machine user name", "") ).split('\'')[1] 

##########################
##  SHELL PROMPTS
##########################
if len(sys.argv) != 2:
  print "...usage: username"
  exit(1)
username = sys.argv[1]
##########################  

loveDict = {}
#cookie = ""

#returns the HTML for a hype machine page where information can be extracted
def getPage(pageNum):
  songNumReq = urllib2.Request('http://hypem.com/'+username+'/' + str(pageNum) + '/?ax=1&ts='+ str(time.time()) )
  response = urllib2.urlopen(songNumReq)
  cookie = response.headers.get('Set-Cookie')#saves the cookie
  return response.read(),cookie #grab the HTML

#creates a database of loved songs in a dictionary
def getLoved(songnum):
  for i in range((int(songnum)/20)+1):
    page,cookie = getPage(i+1)
    idMatches = re.findall("(?<=\tid:\')\w*(?=\')", page)       #regular expression to locate the song id, used to generate the URL and as the index for the loved songs dictionary
    keyMatches = re.findall("(?<=\tkey: \')\w*(?=\')", page)    #used for the second part of the URL
    songMatches= re.findall("(?<=\tsong:\').*(?=\')", page)     #stores song title for reference
    artistMatches= re.findall("(?<=\tartist:\').*(?=\')", page) #store artist for reference
    for i in range(len(idMatches)):
      loveDict[idMatches[i]] = ( ("key",keyMatches[i]),("artist",artistMatches[i]),("song",(songMatches[i].replace('/',"")).replace('\\',"")), cookie )


print "...gathering " +username+ "'s Hype Machine Loved Songs" #
songnum = getPage(1)[0].split("favorite songs\"><em>")[1].split("</em> <span>")[0]#
print "..."+username+" has "+songnum+" favorite songs" 

#creates a database of all loved songs
getLoved(songnum)

for songIds in loveDict.keys():
  mp3Name = loveDict[songIds][2][1] + ".mp3"
  print loveDict[songIds][1][1] + " - " + loveDict[songIds][2][1]
  if os.path.isfile("/sdcard/Music/hypem/"+mp3Name) == False:
		try:
			url = "http://hypem.com/serve/play/" + songIds + '/' + loveDict[songIds][0][1] + ".mp3"
  			req2 = urllib2.Request(url)
  			req2.add_header('cookie', loveDict[songIds][3])
  			response = urllib2.urlopen(req2)
			#grab the data
  			data2 = response.read()
  			song = open("/sdcard/Music/hypem/"+mp3Name, "wb")#hardcoded for convenience now
  			song.write(data2)
  			song.close()
  			time.sleep(1)#sleep to prevent suspicions of scripting from teh hype machinesz
		except urllib2.HTTPError, error:
			print "...not available for download"
