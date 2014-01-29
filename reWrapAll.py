#test rewrapping all apps by emulating browser
#this is not QA'd
#the intention of this script is to grab all the apps that 
#are already wrapped, find their wrap URL and request it
#via mechanize, thus rewrapping everything

from BeautifulSoup import BeautifulSoup
import requests
import json
import time

credentialFile = open('./creds.json')
creds = json.load(credentialFile)

tenantURL = creds['baseURL']
username = creds['name']
password = creds['pass']
loginURL = '%s/admin/login' %tenantURL
updateURL = '%s/admin/message/list' %tenantURL

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



appWebService = '%s/appstore/webapi1/apps' %tenantURL
appResponse = s.get(appWebService)
appData = appResponse.content
appDataJSON = json.loads(appData)

print appDataJSON

for x in appDataJSON['apps']:
  if x['policy']: 
    rewrapApp = x['rewrap_url']
    print "now wrapping: " + x['title']
    rewrapURL = tenantURL + rewrapApp
    print rewrapURL
    wrapResponse = s.get(rewrapURL)
    print "Pausing for 10 seconds"
    time.sleep(10)
  #print x['policy']
