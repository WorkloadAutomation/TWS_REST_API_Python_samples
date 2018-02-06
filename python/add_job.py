#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse

parser = argparse.ArgumentParser(description='Add a job in to the model')
parser.add_argument('-j','--jobname', help='job name', required=True, metavar="JOB_NAME")
parser.add_argument('-u','--twsuser', help='TWS user', required=True, metavar="TWS_USER")
parser.add_argument('-w','--workstationName', help='TWS workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-t','--taskString', help='JOB task string', required=True, metavar="TASK_STRING")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

url = '/model/jobdefinition'
filters = {
		"header": {
			"jobDefinitionKey": {
				"name": args.jobname,
				"workstationName":args.workstationName
			},
			"description":"Added by REST API.",
			"taskType": "UNIX",
			"userLogin": args.twsuser
		},
	"taskString": args.taskString,
	"recoveryOption": "STOP"
		}


headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


resp = conn.post(url, json=filters, headers=headers)

r = resp.json()

print('The command "add" completed successfully on object "'+r['id']+'"')