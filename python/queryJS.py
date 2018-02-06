#!/usr/bin/python
#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################
import waconn
import argparse

parser = argparse.ArgumentParser(description='Query job streams.')
parser.add_argument('-js','--jsname', help='job stream name filter', required=True, metavar="JS_FILTER")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

# Query to find pools matching provided filter
resp = conn.post('/plan/current/jobstream/query',
	{ "filters": { "jobStreamInPlanFilter": { "jobStreamName": args.jsname } } }, 
	headers={'How-Many': '500'})

r = resp.json()

#print json.dumps(r, indent=2)
for js in r:
	print js["key"]["workstationKey"]["name"]+'#'+js["key"]["name"]+'('+js["key"]["startTime"]+')'

