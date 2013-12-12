Shapelink
=========

Python module for accessing Shapelink.com API


# Getting started



´´´python
import os

import shapelink


'''
Place your login credential in a file called "shapelink_secrets.json" with the following (json) format:

{
    "APIKEY" : {YOUR API KEY},
    "SECRET" : {YOUR API SECRET},
    "USERNAME" : {YOUR USERNAME},
    "PASSWORD" : {YOUR PASSWORD}
}
'''
CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'shapelink_secrets.json')


sl = shapelink.Shapelink()

sl.authenticate(CLIENT_SECRETS)

challenges = sl.get_user_challenges(culture="sv")

for c in challenges.get('challenges'):
    print c

´´´
