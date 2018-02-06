#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse

parser = argparse.ArgumentParser(description='Rerun a job')
parser.add_argument('-j','--jobname', help='job name', required=True, metavar="JOB_NAME")
parser.add_argument('-w','--workstationName', help='TWS workstation name', required=True, metavar="WORKSTATION_NAME")
parser.add_argument('-id','--jsInternalIdentifier', help='The js internal id', required=True, metavar="JS_ID")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

# now we get the job in plan instance

url = '/plan/current/job/' + args.workstationName + '%3B' \
      + args.jsInternalIdentifier + '%3B' + args.jobname + '/action/rerun'

filters = {}

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


resp = conn.put(url, json=filters, headers=headers)


print("done!")


