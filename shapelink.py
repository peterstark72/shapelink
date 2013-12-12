#!/usr/bin/env python


import urllib
import urllib2
import json
import hashlib


from collections import OrderedDict



AUTH_REQUIRETOKEN = "/auth/requiretoken"

BASEURL = "http://api.shapelink.com"



SHAPELINK_METHODS = {
    'get_user' : {
        'required' : [],
        'optional' : ['user_id'],
        'endpoint' : "/user/get"
    },
    'get_profile' : {
        'required' : ['culture'],
        'optional' : ['user_id'],
        'endpoint' : "/user/getProfile"
    },
    'get_user_challenges' : {
        'required' : ['culture'],
        'optional' : ['active', 'user_id','string'],
        'endpoint' : "/challenge/getUserChallenges"    
    },
    'get_challenge' : {
        'required' : ['challenge_id', 'culture'],
        'optional' : [],
        'endpoint' : "/challenge/getChallenge"    
    },
    'get_challenges' : {
        'required' : [],
        'optional' : ['string', 'type', 'category','hide_my'],
        'endpoint' : "/challenge/getChallenges"    
    },
    'get_challengeresult' : {
        'required' : ['challenge_id'],
        'optional' : [],
        'endpoint' : "/challenge/getResults"    
    },
    'save_weight' : {
        'required' : ['value', 'date'],
        'optional' : ['weight_id','description'],
        'endpoint' : "/diary/saveWeightNotation"    
    },
    'get_weight' : {
        'required' : ['weight_id'],
        'optional' : [],
        'endpoint' : "/diary/getWeightNotation"    

    }

}


class ShapelinkException( Exception ):
    pass


class ShapelinkAccumulator:
    def __init__( self, shapelink_obj, name ):
        self.shapelink_obj = shapelink_obj
        self.name          = name
    
    def __repr__( self ):
        return self.name
    
    def __call__( self, *args, **kw ):
        return self.shapelink_obj.call_method( self.name, *args, **kw )


class Shapelink(object):

    def __init__(self):

        for method, _ in SHAPELINK_METHODS.items():
            if not hasattr( self, method ):
                setattr( self, method, ShapelinkAccumulator( self, method ))


    def call_method(self, method, *args, **kw):

        meta = SHAPELINK_METHODS[method]

        kw['user_token'] = self.token
        kw['apikey'] = self.apikey

        if args:
            names = meta['required'] + meta['optional']
            for i in range(len(args)):
                kw[names[i]] = args[i]

        url = BASEURL + meta['endpoint'] + "?" + urllib.urlencode(kw) + "&sig=" + self._calcsig(kw)

        return self._geturl(url)


    def authenticate(self, fname):

        credentials = json.load(open(fname, "r"))         

        self.apikey = credentials.get('APIKEY', None)
        self.secret = credentials.get('SECRET', None)
    
        params = {
            'username': credentials.get('USERNAME', None),
            'password' : credentials.get('PASSWORD', None),
            'apikey' : self.apikey
        }

        url = BASEURL + AUTH_REQUIRETOKEN + "?" + urllib.urlencode(params)

        result = self._geturl(url)

        self.token = result.get('token')
        self.user_id = result.get('user_id')

        return self      


    def _geturl(self, url):
        response = json.loads(urllib2.urlopen(url).read())

        status = response.get('status', None)

        if status == "error":
            raise ShapelinkException(response.get('message'))

        return response.get('result')



    def _calcsig(self, params):
        '''Signs API parameters according to algorithm at 
        http://developer.shapelink.com/index.php/Creating_the_request_signature
        '''

        sorted_params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))

        s = ""
        for k,v in sorted_params.items():
            s += "=".join((k,str(v)))
        s += self.secret

        return hashlib.md5(s).hexdigest()





