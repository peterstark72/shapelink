#!/usr/bin/env python

import os
import sys
import shapelink
import pprint


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 
    'shapelink_secrets.json')

def main():

	if len(sys.argv)<2:
		sys.stderr.write("Usage : python %s username\n" % sys.argv[0])
		raise SystemExit(1)
	username = sys.argv[1]
	password = raw_input("password : ")


	api = shapelink.get_api_fromsecrets(CLIENT_SECRETS)
	user = shapelink.get_user(api, username, password)


	pprint.pprint(user.stats("2013-11-01", "2013-12-01"))
	pprint.pprint(user.health())


if __name__ == '__main__':
    main()