#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse

parser = argparse.ArgumentParser(description='Add a job in to the model')
parser.add_argument('-jn','--jobName', help='job name', required=True, metavar="JOB_NAME")
parser.add_argument('-jw','--jobWorkstationName', help='job workstation name', required=True, metavar="JOB_WORKSTATION_NAME")
parser.add_argument('-jsw','--jsWorkstationName', help='job stream workstation name', required=False, metavar="JS_WORKSTATION_NAME")
parser.add_argument('-id','--jsInternalIdentifier', help='job stream internal id', required=True, metavar="JS_ID")
parser.add_argument('-ja','--jobAlias', help='job alias', required=True, metavar="JOB_ALIAS")


args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')


# first rest call to get the jd id

url = '/model/jobdefinition/header/query'
filters = {
		"filters": {
			"jobDefinitionFilter": {
				"jobDefinitionName": args.jobName,
				"workstationName":args.jobWorkstationName
			}
		}
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

r = resp.json()

for jd in r:
	jobId=jd["id"]

print("the jd id is: " + jobId)

jsWorkstationName=args.jobWorkstationName
if args.jsWorkstationName:
	jsWorkstationName = args.jsWorkstationName

url = '/plan/current/jobstream/' + jsWorkstationName + '%3B' + args.jsInternalIdentifier + '/action/submit_job'


filters = {
    "jobDefinitionId": jobId,
    "alias": args.jobAlias
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

jobInplanInstance = resp.json()


# now we can submit the job into the js

url = '/plan/current/job/action/submit_ad_hoc_job'

filters = {
    "job": jobInplanInstance
	}
# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

r = resp.json()
print ('Submitted '+r["id"])




