#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse
import datetime

parser = argparse.ArgumentParser(description='Add a job in to the model')
parser.add_argument('-j','--jsName', help='job stream', required=True, metavar="JOB_STREAM")
parser.add_argument('-w','--workstationName', help='TWS workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-ja','--jsAlias', help='job stream alias', required=False, metavar="JS_ALIAS")
parser.add_argument('-vf','--validFrom', help='valid from', required=False, metavar="VALID_FROM")
parser.add_argument('-vt','--validTo', help='valid to', required=False, metavar="VALID_TO")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')



# first rest call to get the js id

url = '/model/jobstream/header/query'
filters = {
		"filters": {
			"jobstreamFilter": {
				"jobStreamName": args.jsName,
				"workstationName":args.workstationName,
				"validFrom": args.validFrom,
				"validTo": args.validTo
			}
		}
	}
#we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print ('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

r = resp.json()
if len(r) == 0:
    print('job stream not found')
    exit(2)

for js in r:
	jsId=js["id"]

print("the js id is: " + jsId)

# now we can submit the js
now = datetime.datetime.utcnow().isoformat()

url = '/plan/current/jobstream/' + jsId + '/action/submit_jobstream'

filters = {
		"inputArrivalTime": now,
		"alias": args.jsAlias
	}

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

#print(json.dumps(resp.json(), indent=2))
r = resp.json()

for js in r:
	print ('Submitted '+js)
