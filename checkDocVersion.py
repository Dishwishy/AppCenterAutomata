#test rewrapping all apps by emulating browser
#this is not QA'd

import mechanize, cookielib, json, time, argparse, getpass

parser = argparse.ArgumentParser(description='Tenant Info')
parser.add_argument('--tenant', help='please enter your tenant name', required=True)
parser.add_argument('--admin', help='enter the name of an admin account', required=True)
args = parser.parse_args()

print "please enter the password for the admin account" 
password = getpass.getpass()

tenantURL = "https://" + args.tenant + ".appcenterhq.com"

br = mechanize.Browser()
#mechanize debug options
#br.set_debug_redirects(True)
#br.set_debug_responses(True)
#br.set_debug_http(True)

cj = cookielib.LWPCookieJar('disCookie')
br.set_cookiejar(cj)

br.set_handle_equiv(1)
br.set_handle_gzip(1)
br.set_handle_redirect(1)
br.set_handle_referer(1)
br.set_handle_robots(0)

br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36')]

tenantAdminURL = '%s/admin/apps/list' %tenantURL
print tenantAdminURL
r = br.open(tenantAdminURL)
br.select_form(nr=0)
br.form['username'] = args.admin
br.form['password'] = password
br.submit()
deviceWebService = '%s/appstore/webapi1/devices/topdevices?start=0&length=500&order=name' %tenantURL
deviceResponse = br.open(deviceWebService)
deviceData = deviceResponse.read()
deviceDataJSON = json.loads(deviceData)

for x in deviceDataJSON['devices']:
  deviceName = x['device']['name']
  deviceDataURL =  x['device']['device_inventory_url'] 
  deviceDataURL =  tenantURL + deviceDataURL
  contentResponse = br.open(deviceDataURL)
  contentData = contentResponse.read()
  contentDataJSON = json.loads(contentData)
  for x in contentDataJSON['installed_content_versions']:
    print  deviceName + ", " + x['title'] + ", " + x['version_string']
