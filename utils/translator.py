# -*- coding:utf-8 -*-
import os
from googletrans import Translator
import requests
import json


class Translator():
    def __init__(self, method=0):
        self.method = method

    def translate(self, content, src, dest):
        response_content = self.request(content, src, dest)
        trans_result = self.gettrans(response_content)
        return trans_result

    def request(self, content, src, dest):
        if self.method == 0:
            self.url = 'http://translate.google.cn/translate_a/single'
            self.dict = {'client': 'gtx', 'dt': 't', 'dj': '1', 'ie': 'UTF-8', 'sl': src, 'tl': dest}
            self.dict['q'] = content
            r = requests.get(self.url, self.dict)
            if not r.status_code == 200:
                self.method += 1
                return self.request(self, content, src, dest)
            else:
                result = r.json()
                return result

    def gettrans(self, response_content):
        if self.method == 0:
            try:
                trans_result = response_content['sentences'][0]['trans']
            except KeyError or IndexError:
                print('The return format has changed')
                trans_result = '!@#$%^&*()'
            return trans_result
