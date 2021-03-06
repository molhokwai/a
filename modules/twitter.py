#!/usr/bin/env python 
# coding: utf8 
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *

import urllib
import gluon.contrib.simplejson as simplejson

# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

class Manager():
    # constants
    SEARCH_URL = 'http://search.twitter.com/search.json?q=%s'
    USER_URL = 'http://twitter.com/%s?format=json'

    # attributes
    _username = None
    _hashes = None
    
    def __init__(self, _username, _hashes=None):
        self._username=_username
        self._hashes=_hashes

    def search_tweets(self, _filter):
        return simplejson.loads(
                urllib.urlopen(self.SEARCH_URL % _filter).read())['results']
        
    def get_user_tweets(self, _hashes=''):
        page = urllib.urlopen(self.USER_URL % (self._username)).read()
        tweets=simplejson.loads(page)
        
        if _hashes:
            _hashes=_hashes.split(',')
        if len(_hashes)>0:
            hash_tweets=[]
            for i in range(len(_hashes)):
                hash_tweets.append(XML(tweets['#%s' % _hashes[i]]))
            tweets=[]
            tweets=[tweets+h_t for h_t in hash_tweets]
        return tweets
