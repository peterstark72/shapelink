#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import shapelink
import os


CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 
    'shapelink_secrets.json')


class TestShapelink(unittest.TestCase):

    def setUp(self):        
        api = shapelink.get_api_fromsecrets(CLIENT_SECRETS)
        username = os.environ['SHAPELINK_USERNAME']
        password = os.environ['SHAPELINK_PASSWORD']
        self.user = shapelink.get_user(api, username, password) 
        self.assertTrue(self.user)


    def test_profile(self):
        profile = self.user.profile()
        self.assertTrue(profile)


    def test_diary(self):
        diary = self.user.diary()
        self.assertTrue(diary )


if __name__ == '__main__': 
    unittest.main()

