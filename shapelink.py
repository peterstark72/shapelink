#!/usr/bin/env python


import urllib
import urllib2
import json
import hashlib
import datetime

from collections import OrderedDict



AUTH_REQUIRETOKEN = "/auth/requiretoken"

BASEURL = "http://api.shapelink.com"


class ShapelinkException( Exception ):
    pass


SHAPELINK_METHODS = {
    'get_token' : {
        'required' : ['username', 'password'],
        'optional' : [],
        'endpoint' : "/auth/requiretoken"
    },
    'get_user' : {
        'required' : ['user_token'],
        'optional' : ['user_id'],
        'endpoint' : "/user/get"
    },
    'get_profile' : {
        'required' : ['user_token', 'culture'],
        'optional' : ['user_id'],
        'endpoint' : "/user/getProfile"
    },
    'get_day' : {
        'required' : ['user_token', 'date', 'culture'],
        'optional' : [],
        'endpoint' : "/diary/getDay"
    },
    'get_activities' : {
        'required' : ['user_token', 'type', 'culture'],
        'optional' : [],
        'endpoint' : "/diary/getActivities"
    },
    'get_user_challenges' : {
        'required' : ['user_token', 'culture'],
        'optional' : ['active', 'user_id','string'],
        'endpoint' : "/challenge/getUserChallenges"    
    },
    'get_challenge' : {
        'required' : ['user_token', 'challenge_id', 'culture'],
        'optional' : [],
        'endpoint' : "/challenge/getChallenge"    
    },
    'get_challenges' : {
        'required' : ['user_token'],
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
        'required' : ['user_token','weight_id'],
        'optional' : [],
        'endpoint' : "/diary/getWeightNotation"    
    },
    'get_days' : {
        'required' : ['user_token','start_date', 'end_date'],
        'optional' : [],
        'endpoint' : "/statistics/getDays"    
    },
    'get_summary' : {
        'required' : ['user_token'],
        'optional' : [],
        'endpoint' : "/statistics/getTrainingSummary"    
    },
    'get_health' : {
        'required' : ['user_token', 'culture'],
        'optional' : [],
        'endpoint' : "/statistics/getHealthSummary"    
    }

}



def loadurl(url):
    '''Loads resource from URL. Raises ShapelinkException if error'''

    try:
        response = json.loads(urllib2.urlopen(url).read())
    except IOError:
        raise ShapelinkException("Could not access Shapelink server")

    status = response.get('status', None)

    if not status or status == "error":
        raise ShapelinkException(response.get('message'))

    return response.get('result')



class ShapelinkAccumulator:
    '''Used by Shapelink API object to generate methods for all Shapelink API calls'''
    def __init__( self, shapelink_obj, name ):
        self.shapelink_obj = shapelink_obj
        self.name          = name
    
    def __repr__( self ):
        return self.name
    
    def __call__(self, *args, **kw ):
        return self.shapelink_obj.call_method( self.name, *args, **kw )


class ShapelinkApi(object):
    '''Wrapper for the API available from developer.shapelink.com'''

    def __init__(self, apikey, secret):

        self.apikey = apikey
        self.secret = secret

        for method, _ in SHAPELINK_METHODS.items():
            if not hasattr( self, method ):
                setattr( self, method, ShapelinkAccumulator( self, method ))


    def call_method(self, method, *args, **kw):
        '''Generic method for calling an API endoint'''

        meta = SHAPELINK_METHODS[method]

        kw['apikey'] = self.apikey

        if args:
            names = meta['required'] + meta['optional']
            for i in range(len(args)):
                kw[names[i]] = args[i]

        url = BASEURL + meta['endpoint'] + "?" + urllib.urlencode(kw) + "&sig=" + self._calcsig(kw)

        return loadurl(url)



    def _calcsig(self, params):
        '''Signs API parameters according to algorithm at 
        http://developer.shapelink.com/index.php/Creating_the_request_signature
        '''

        sorted_params = OrderedDict(sorted(params.items(), key=lambda t: t[0]))

        s = ""
        for k,v in sorted_params.items():
            s += "=".join((k,str(v)))
        s += self.secret #don't forget to add secret

        return hashlib.md5(s).hexdigest()




def get_api(apikey, secret):
    '''Returns API object from given API-key and secret

    apikey - Shapelink API-key
    secret - Shapelink API-secret

    '''
    return ShapelinkApi(apikey, secret)



def get_api_fromsecrets(fname):
    '''Returns API object from API-key and secret available in the file
    fname - name of file that contais the API-key and secret

    '''
    credentials = json.load(open(fname, "r"))         
    apikey = credentials.get('APIKEY', None)
    secret = credentials.get('SECRET', None)

    return ShapelinkApi(apikey, secret)


def get_user(api, username, password):
    '''Returns a ShapelinkUser object 

    api - API object
    username - Shapelink username 
    password - Shapelink password

    '''
    result = api.get_token(username, password)
    return ShapelinkUser(api, result.get('token'))



class ShapelinkUser(object):

    def __init__(self, api, user_token, culture="sv"):
        self.user_token = user_token
        self.api = api
        self.culture = culture


    def diary(self, date=None):
        '''Returns day activity for a specific day, today is default.

        date - YYYY-MM-DD

        '''
        if not date:
            date = datetime.datetime.today().strftime("%Y-%m-%d")
        return self.api.get_day(self.user_token, date, self.culture)


    def profile(self):
        return self.api.get_profile(self.user_token, self.culture)


    def activities(self, type_):
        return self.api.get_activities(self.user_token, 
                                                type_, self.culture)        


    def joined_challenges(self):
        '''Returns user's chanllenges'''
        return self.api.get_user_challenges(self.user_token, self.culture)


    def challenges(self):
        '''Returns available chanllenges to join'''
        return self.api.get_challenges(self.user_token)


    def challenge(self, challenge_id):
        '''Returns a specific chanllenge'''
        return self.api.get_challenge(self.user_token, 
                            challenge_id, self.culture)


    def stats(self, start_date, end_date):
        '''Returns day by day stats'''
        return self.api.get_days(self.user_token, start_date, end_date)


    def save_weight(self, value, date):
        return self.api.save_weight(self.user_token, value, date)


    def health(self):
        return self.api.get_health(self.user_token, self.culture)






















