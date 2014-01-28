#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import requests
import json

credentialFile = open('./creds.json')
creds = json.load(credentialFile)

username = creds['name']
password = creds['pass']
loginURL = 'https://kylechamplin.appcenterhq.com/admin/login'
updateURL = 'https://kylechamplin.appcenterhq.com/admin/message/list'
#create a requests session object
s = requests.Session()
#get our session cookies, headers, etc etc
resp = s.get(loginURL)
soup = BeautifulSoup(resp.content)
form = soup.form
csrfInfo = soup.find(type="hidden")
csrfToken = csrfInfo['value']

authPayload = {'csrfmiddlewaretoken':csrfToken,'username':username,'password':password,'login':'Login'}
headerUpdate = {'Content-Type':'x-www-form-urlencoded'}

resp = s.post(loginURL, data=authPayload, headers=headerUpdate)

if(resp.status_code == 200):
  updateStream = s.get(updateURL)
else:
  print "Authentication Error...Maybe?"


messageFile = open('lastMessageTime.txt','r+')
timeStamp = messageFile.read()
updateJSON = json.loads(updateStream.content)
currMsgTime = str(updateJSON["messages"][0]["date_created"])

if(currMsgTime == timeStamp):
  print "No new messages, going to sleep"
else:
  print currMsgTime 
  messageFile.seek(0)
  messageFile.write(currMsgTime) 
  messageFile.close

