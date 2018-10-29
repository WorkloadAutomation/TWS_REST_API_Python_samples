#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse

parser = argparse.ArgumentParser(description='Rerun a job')
parser.add_argument('-w','--workstationName', help='TWS workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-js','--jsName', help='job stream name', required=True, metavar="JS_NAME")
parser.add_argument('-ia','--schedTime', help='job stream scheduled time / input arrival', metavar="JS_SCHED_TIME")
parser.add_argument('-j','--jobName', help='job name', required=True, metavar="JOB_NAME")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

# now we get the job in plan instance

filter = {"filters": {"jobInPlanFilter": {"jobStreamName": args.jsName, "jobName": args.jobName, "workstationName":args.workstationName, "lastInRerunChain": True}}}

if args.schedTime:
    filter["filters"]["jobInPlanFilter"]["inputArrivalTime"]=args.schedTime

print "Running query with filter: " + str(filter)

resp = conn.post('/plan/current/job/query', json=filter, headers={'How-Many': '10'})

r = resp.json()
if len(r) == 0:
    print('No job found')
    exit(2)

# and we call the rerun

for j in r:
    workstationName=j["jobStreamInPlan"]["workstationKey"]["name"]
    jobStreamName=j["jobStreamInPlan"]["name"]
    inputArrivalTime=j["jobStreamInPlan"]["startTime"]
    jobName=j["name"]
    jobId=j["id"]
    print
    print "---------------------------"
    print "Rerunning %s#%s(%s).%s - id: %s" % (workstationName,jobStreamName,inputArrivalTime,jobName,jobId)
    url = '/plan/current/job/' + jobId + '/action/rerun'

    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    resp = conn.put(url, json={}, headers=headers)

print("done!")


