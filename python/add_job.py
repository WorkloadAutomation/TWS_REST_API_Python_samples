#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import requests
import json
import sys

host = ''
user = ''
pwd = ''
jobName = ''
workstationName = ''
taskString = ''
port = '31116'


if len(sys.argv) != 7:
	print ('Usage: '+sys.argv[0]+' <tws_host> <tws_user> <password> <job_name> <workstation_name> <task_string>')
	sys.exit(2)

host = sys.argv[1]
user = sys.argv[2]
pwd = sys.argv[3]
jobName = sys.argv[4]
workstationName = sys.argv[5]
taskString = sys.argv[6]

url = 'https://'+host+':'+port+'/twsd/model/jobdefinition'
filters = {
		"header": {
			"jobDefinitionKey": {
				"name": jobName,
				"workstationName":workstationName
			},
			"description":"Added by REST API.",
			"taskType": "UNIX",
			"userLogin": user
		},
	"taskString": taskString,
	"recoveryOption": "STOP"
		}


headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = requests.post(url, json=filters, headers=headers, auth=(user,pwd), verify=False)

r = resp.json()
print(json.dumps(r, indent=2))

if resp.status_code != 201:
	raise (BaseException('POST {} : {}'.format(url,resp.status_code)))