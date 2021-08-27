import time
import datetime
import re
import PyRSS2Gen
import os
import requests

timeofday = 86400  # 24*60*60
datemap = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sept': 9, 'Oct': 10,
           'Nov': 11, 'Dec': 12}


class RSSGenerator():
    def __init__(self, rssname=None, url=None, save='feeds/defualt.xml', frequency=1, description=None):
        '''
        the base class of RSSGenerator.
        :param rssname:
        :param url:
        :param save:
        :param frequency:
        '''
        self.url = url
        self.savepath = save
        self.frequency = frequency
        self.rssname = rssname if not rssname == None else self.url
        self.description = description if not description == None else self.url

    def generate(self, rule):
        raise NotImplemented

    def rule(self):
        raise NotImplemented
