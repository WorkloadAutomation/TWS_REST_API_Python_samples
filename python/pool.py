#!/usr/bin/python
#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################
import waconn
import argparse

parser = argparse.ArgumentParser(description='Add/Remove member of a static pool.')
parser.add_argument('--pool','-p', help='name of the pools to update (accepts wildcards)', required=True, metavar="POOL_NAME")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('--add','-a', help='add a member to the pool', metavar="MEMBER_NAME")
group.add_argument('--rm','-r', help='remove a member to the pool', metavar="MEMBER_NAME")

args = parser.parse_args()
conn = waconn.WAConn('waconn.ini','/twsd')

# Query to find pools matching provided filter
resp = conn.post('/model/workstation/header/query',
	{ "filters": { "workstationFilter": { "workstationName": args.pool } } }, 
	headers={'How-Many': '500'})

r = resp.json()

for w in r:
	print 'Processing workstation ' + w['name']
	if w['type']=='POOL':
		wks = conn.get('/model/workstation/'+w['id']).json()
		print 'Original workstation: %s' % wks
		if 'agentLinks' not in wks:
			wks['agentLinks'] = []
		
		agents = wks['agentLinks'] 

		print 'Original members: %s' % agents
		
		#remove members to be deleted
		if args.rm:
			agents = list(filter(lambda a : a['workstationName'] != args.rm, agents))

		if args.add:
			agents.append({ 'workstationName' : args.add})
		
		print 'Final members: %s' % agents
		wks['agentLinks'] = agents
		print 'Final workstation: %s' % wks

		conn.put('/model/workstation/'+w['id'], wks)

	else:
		print 'Ignoring %s workstation that is not a pool' % (w['name'])
		

