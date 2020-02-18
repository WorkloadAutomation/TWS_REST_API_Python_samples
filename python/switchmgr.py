#!/usr/bin/python

#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################

import waconn
import argparse

parser = argparse.ArgumentParser(description='Perform a switch of a domain manager ')
parser.add_argument('-d','--domain', help='domain name', required=True, metavar="DOMAIN_NAME")
parser.add_argument('-m','--manager', help='new manager workstation name', required=True, metavar="WORKSTATION_NAME")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')


# first rest call to get the domain id
url = '/plan/current/domain/query'
filters = {
  "filters": {
    "domainInPlanFilter": {
      "domainName": args.domain
    }
  }
}

# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

r = resp.json()

for dom in r:
	domId=dom["id"]

print("the domain id is: " + domId)

# second rest call to get the workstation id
url = '/plan/current/workstation/query'
filters = {
  "filters": {
    "workstationInPlanFilter": {
      "workstationName": args.manager
    }
  }
}

# we get the first result
headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'How-Many': '1'}

print('Connecting to '+url)
resp = conn.post(url, json=filters, headers=headers)

r = resp.json()

for wks in r:
	wksId=wks["id"]

print("the workstation id is: " + wksId)


# now we can perform the switch manager

url = '/plan/current/domain/'+domId+'/action/switch_domain_workstation'
print ('Connecting to '+url)
resp = conn.put(url, data=wksId)

if resp.ok:
  print ('Swithmgr started')




