#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import requests
import datetime
import json
import sys

host = ''
user = ''
pwd = ''
jsName = ''
workStationName = ''
port = '31116'
# eg: 2018-12-23T00:00:00
validFrom = ''
validTo = ''
jsAlias = ''


if len(sys.argv) < 6 or len(sys.argv) > 7:
	print ('Usage: '+sys.argv[0]+' <tws_host> <tws_user> <password> <js_name> <workstation_name> [<js_alias>]')
	sys.exit(2)


host = sys.argv[1]
user = sys.argv[2]
pwd = sys.argv[3]
jsName = sys.argv[4]
workStationName = sys.argv[5]

if len(sys.argv) >= 7:
    jsAlias = sys.argv[6]



# first rest call to get the js id

url = 'https://'+host+':'+port+'/twsd/model/jobstream/header/query'
filters = {
		"filters": {
			"jobstreamFilter": {
				"jobStreamName": jsName,
				"workstationName":workStationName,
				"validFrom": validFrom,
				"validTo": validTo
			}
		}
	}
#we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print ('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)



if resp.status_code != 200:
    # This means something went wrong.
	raise (BaseException('POST {} : {}'.format(url, resp.status_code)))

r = resp.json()
if len(r) == 0:
    print('job stream not found')
    exit(2)

for js in r:
	jsId=js["id"]

print("the js id is: " + jsId)

# now we can submit the js
now = datetime.datetime.utcnow().isoformat()

url = 'https://' + host +':' + port +'/twsd/plan/current/jobstream/' + jsId + '/action/submit_jobstream'

filters = {
		"inputArrivalTime": now,
		"alias": jsAlias
	}

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)


if resp.status_code != 200:
    # This means something went wrong.
	raise (BaseException('POST {} : {}'.format(url, resp.status_code)))

print(json.dumps(resp.json(), indent=2))