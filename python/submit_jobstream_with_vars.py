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
parser.add_argument('-w','--workstationName', help='job stream workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-v','--variables', nargs='+', help='variables in key:value format', required=True, metavar="KEY:VALUE")
nargs='+'

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

# first rest call to get the js id

now = datetime.datetime.utcnow().isoformat()

resp = conn.post('/model/jobstream/header/query', 
	json={"filters": {"jobstreamFilter": {"jobStreamName": args.jsName,"workstationName":args.workstationName,"validIn": now}}},
	headers={'How-Many': '1'})

r = resp.json()
if len(r) == 0:
    print('job stream not found')
    exit(2)

jsId=r[0]["id"]

print("the js id is: " + jsId)

json = {"inputArrivalTime": now}

VarBug = True # Change to True if running with master older than 9.4 FP3 or 9.3 FP4, False otherwise

if VarBug:    
	#Get full JS
	r = conn.get('/model/jobstream/'+jsId)
	js = r.json()

	if "variableTableId" in js:
		vtId=js["variableTableId"]
		print("the variable table id is: " + vtId)
	else:
		#get default table
		resp = conn.post('/model/variabletable/header/query', 
			json={"filters": {"variableTableFilter": {"isDefaultTable": True}}},
			headers={'How-Many': '1'})

		r = resp.json()
		if len(r) == 0:
			print('Default variable table not found')
			exit(2)

		vtId=r[0]["id"]
		print("the default variable table id is: " + vtId)

	json["variableTableId"]=vtId

def varToTableVar(v):
	a=v.split(":")
	return {"key":a[0],"value":a[1]}

if args.variables:
	m = map(lambda v: varToTableVar(v), args.variables)
	l = list(m)
	json["variableTable"]=l

# now we can submit the js
print "submit content: " +str(json)
resp = conn.post('/plan/current/jobstream/' + jsId + '/action/submit_jobstream', json=json)

#print(json.dumps(resp.json(), indent=2))
r = resp.json()

for js in r:
	print ('Submitted '+js)