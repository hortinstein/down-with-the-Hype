import urllib2
import re
import MySQLdb
import time
import sys

if len(sys.argv) != 2:
  print "...usage: username"
  exit(1)
loveDict = {}
cookie = ""
#returns the HTML for a hype machine page where information can be extracted
def getPage(pageNum):
  songNumReq = urllib2.Request('http://hypem.com/'+sys.argv[1]+'/' + str(pageNum) + '/?ax=1&ts='+ str(time.time()) )
  response = urllib2.urlopen(songNumReq)
  cookie = response.headers.get('Set-Cookie')#saves the cookie
  return response.read(),cookie #grab the HTML

#creates a database of loved songs
def getLoved(songnum):
  for i in range((int(songnum)/20)+1):
    page,cookie = getPage(i+1)
    idMatches = re.findall("(?<=\tid:\')\w*(?=\')", page)
    keyMatches = re.findall("(?<=\tkey: \')\w*(?=\')", page)
    songMatches= re.findall("(?<=\tsong:\').*(?=\')", page)
    artistMatches= re.findall("(?<=\tartist:\').*(?=\')", page)
    for i in range(len(idMatches)):
      loveDict[idMatches[i]] = ( ("key",keyMatches[i]),("artist",artistMatches[i]),("song",songMatches[i].replace('/',"")), cookie ) #putting songs into a dictionary for later reference


print "...gathering " +sys.argv[1]+ "'s Hype Machine Loved Songs" #
songnum = getPage(1)[0].split("favorite songs\"><em>")[1].split("</em> <span>")[0]#
print "..." + sys.argv[1]+" has "+songnum+" favorite songs" 

#creates a database of all loved songs
getLoved(songnum)

for songIds in loveDict.keys():
  print loveDict[songIds][1][1] + " - " + loveDict[songIds][2][1]
  url = "http://hypem.com/serve/play/" + songIds + '/' + loveDict[songIds][0][1] + ".mp3"
  req2 = urllib2.Request(url)
  req2.add_header('cookie', loveDict[songIds][3])
  response = urllib2.urlopen(req2)
	#grab the data
  data2 = response.read()
  mp3Name = loveDict[songIds][2][1] + ".mp3"
  song = open(mp3Name, "wb")
  song.write(data2)
  song.close()
	#if we make too many requests, they ban us. So lets sleep
  time.sleep(1)
