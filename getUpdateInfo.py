#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import requests
import json

username = '' 
password = '' 
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

print updateStream.text
