#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import requests
import json
import sys
print (sys.version)
host = ''
user = ''
pwd = ''
jobName = ''
jobAlias = ''
jobWorkStationName = ''
jsInternalIdentifier = ''
jsWorkstationName = ''
port = '31116'


if len(sys.argv) < 8 or len(sys.argv) > 9:
	print ('Usage: '+sys.argv[0]+' <tws_host> <tws_user> <password> <job_name> <job_alias> <job_workstation_name> <job_stream_id> [<js_workstation_name>]')
	sys.exit(2)

host = sys.argv[1]
user = sys.argv[2]
pwd = sys.argv[3]
jobName = sys.argv[4]
jobAlias = sys.argv[5]
jobWorkStationName = sys.argv[6]
jsInternalIdentifier = sys.argv[7]


jsWorkstationName = sys.argv[6]
if len(sys.argv) >= 9:
	jsWorkstationName = sys.argv[8]


# first rest call to get the jd id

url = 'https://'+host+':'+port+'/twsd/model/jobdefinition/header/query'
filters = {
		"filters": {
			"jobDefinitionFilter": {
				"jobDefinitionName": jobName,
				"workstationName":jobWorkStationName
			}
		}
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)

if resp.status_code != 200:
    # This means something went wrong.
	raise (BaseException('POST {} : {}'.format(url, resp.status_code)))

r = resp.json()

for jd in r:
	jobId=jd["id"]

print("the jd id is: " + jobId)

# now we get the job in plan instance

url = 'https://' + host +':' + port +'/twsd/plan/current/jobstream/' + jsWorkstationName + '%3B' + jsInternalIdentifier + '/action/submit_job'


filters = {
    "jobDefinitionId": jobId,
    "alias": jobAlias
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)

print(json.dumps(resp.json(), indent=2))
if resp.status_code != 200:
    # This means something went wrong.
	raise (BaseException('POST {} : {}'.format(url, resp.status_code)))

jobInplanInstance = resp.json()


# now we can submit the job into the js

url = 'https://' + host +':' + port +'/twsd/plan/current/job/action/submit_ad_hoc_job'

filters = {
    "job": jobInplanInstance
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)

r = resp.json()
print(json.dumps(r, indent=2))

if resp.status_code != 200:
    # This means something went wrong.
	raise (BaseException('POST {} : {}'.format(url, resp.status_code)))


