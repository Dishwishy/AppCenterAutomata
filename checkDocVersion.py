#Pull information on what content is installed on which device
#this is not QA'd
#This script is meant to pull data from App Center tenant
#and report on the document/content information on each device

from BeautifulSoup import BeautifulSoup
import requests
import json

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


deviceWebService = '%s/appstore/webapi1/devices/topdevices?start=0&length=500&order=name' %tenantURL
deviceResponse = s.get(deviceWebService)
deviceData = deviceResponse.content
deviceDataJSON = json.loads(deviceData)

for x in deviceDataJSON['devices']:
  deviceName = x['device']['name']
  deviceDataURL =  x['device']['device_inventory_url'] 
  deviceDataURL =  tenantURL + deviceDataURL
  contentResponse = s.get(deviceDataURL)
  contentData = contentResponse.content
  contentDataJSON = json.loads(contentData)
  for x in contentDataJSON['installed_content_versions']:
    print  deviceName + ", " + x['title'] + ", " + x['version_string']
