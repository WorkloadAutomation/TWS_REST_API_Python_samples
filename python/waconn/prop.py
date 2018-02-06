#############################################################################
# Licensed Materials - Property of HCL*
# (C) Copyright HCL Technologies Ltd. 2017, 2018 All rights reserved.
# * Trademark of HCL Technologies Limited
#############################################################################
import ConfigParser
import base64

def readProps(inifile):
	pwd=''
	user=''
	hosts=[]
	
	config = ConfigParser.SafeConfigParser(allow_no_value=True)
	config.read(inifile)

	if not config.has_section('WASERVER'):
		raise Exception(inifile + " must have connection properties in WASERVER section")

	if config.has_option('WASERVER', 'pwd'):
		pwd=config.get('WASERVER', 'pwd')
		enc=base64.b64encode(pwd)
		config.remove_option('WASERVER', 'pwd')
		config.set('WASERVER', '; pwd = yourpassword')
		config.set('WASERVER', 'key', enc);
		with open(inifile, 'wb') as configfile:
			config.write(configfile)
	elif config.has_option('WASERVER', 'key'):
		enc=config.get('WASERVER', 'key')
		pwd=base64.b64decode(enc)

	if config.has_option('WASERVER', 'user'):
		user=config.get('WASERVER', 'user')
	
	if config.has_option('WASERVER', 'hosts'):
		rawhosts=config.get('WASERVER', 'hosts');
		hosts=rawhosts.split(",")

	if config.has_option('WASERVER', 'verify'):
		rawVerify=config.get('WASERVER', 'verify');
		verify=(rawVerify.lower == 'true')

	props={'user' : user, 'pwd' : pwd, 'hosts': hosts, 'verify': verify}
	return props
	
