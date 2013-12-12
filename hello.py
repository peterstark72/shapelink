#!/usr/bin/env python

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

print sl.get_challengeresult(challenge_id=53760, culture="sv")

print sl.save_weight(value=81,date="2013-12-12", weight_id=42)

print sl.get_weight(42)

