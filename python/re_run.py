#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import requests
import sys

host = ''
user = ''
pwd = ''
jobName = ''
workStationName = ''
jsInternalIdentifier = ''
port = '31116'

if len(sys.argv) != 7:
	print ('Usage: '+sys.argv[0]+' <tws_host> <tws_user> <password> <job_name> <workstation_name> <job_stream_id>')
	sys.exit(2)

host = sys.argv[1]
user = sys.argv[2]
pwd = sys.argv[3]
jobName = sys.argv[4]
workStationName = sys.argv[5]
jsInternalIdentifier = sys.argv[6]

# now we get the job in plan instance

url = 'https://' + host + ':' + port + '/twsd/plan/current/job/' + workStationName + '%3B' \
      + jsInternalIdentifier + '%3B' + jobName + '/action/rerun'

filters = {}

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

print ('Connecting to '+url)
resp = requests.put(url, json=filters, headers=headers, auth=(user,pwd), verify=False)


if resp.status_code != 202:
    # This means something went wrong.
	raise (BaseException('PUT {} : {}'.format(url, resp.status_code)))


print("done!")


