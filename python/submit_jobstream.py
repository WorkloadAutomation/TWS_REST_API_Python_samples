#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################


VarBug = True # Change to True if running with master older than 9.4 FP3 or 9.3 FP4, False otherwise

import waconn
import argparse
import datetime

parser = argparse.ArgumentParser(description='Submit a job stream to the plan')
parser.add_argument('-j','--jsName', help='job stream', required=True, metavar="JOB_STREAM")
parser.add_argument('-w','--workstationName', help='job stream workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-a','--alias', help='job stream alias', required=False, metavar="JS_ALIAS")
parser.add_argument('-v','--variables', nargs='+', help='variables in key:value format', required=False, metavar="KEY:VALUE")

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

submit = {"inputArrivalTime": now}

#define a function to convert a key:value pair in the json structure
def varToTableVar(v):
	a=v.split(":")
	return {"key":a[0],"value":a[1]}

if args.variables:
	# This list/map/lambda function, will apply the above varToTableVar function to each key:value pair specified with the "--variables" argument
	submit["variableTable"]=list(map(lambda v: varToTableVar(v), args.variables))

	if VarBug:    
		# Before 9.4 FP3 and 9.3 FP4 the variable table id was required in order to pass variables
		# Here we get the JS definition to check if it's using a specific variable table,
		# if not we will search for the default variable table
		
		# Get full JS
		r = conn.get('/model/jobstream/'+jsId)
		js = r.json()

		if "variableTableId" in js:
			# If JS uses a varibale table, let's use it
			vtId=js["variableTableId"]
			print("the variable table id is: " + vtId)
		else:
			# If Not, let's search for the default variable table
			resp = conn.post('/model/variabletable/header/query', 
				json={"filters": {"variableTableFilter": {"isDefaultTable": True}}},
				headers={'How-Many': '1'})

			r = resp.json()
			if len(r) == 0:
				print('Default variable table not found')
				exit(2)

			vtId=r[0]["id"]
			print("the default variable table id is: " + vtId)

		# Add the variable table id to the submit request body
		submit["variableTableId"]=vtId

# Eventually add the argument for alias argument
if args.alias:
	submit["alias"] = args.alias

# now we can submit the js
print "submit parameters: " +str(submit)
resp = conn.post('/plan/current/jobstream/' + jsId + '/action/submit_jobstream', json=submit)
print resp
print resp.headers
r = resp.json()

for js in r:
	print ('Submitted: '+js)
