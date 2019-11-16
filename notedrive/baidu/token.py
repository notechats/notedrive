#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 11:11
# @Author  : niuliangtao
# @Site    :
# @Software: PyCharm
import demjson
import requests


class AccessToken:
    def __init__(self, api_key=None, secret_key=None, access_token=None, refresh_token=None):
        self.token = None

        self.client_id = api_key
        self.client_secret = secret_key

        self.authorization_code = None

        self.access_token = access_token
        self.refresh_token = refresh_token

    def get_authorization_code(self):
        url1 = 'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={}' \
               '&redirect_uri={}&scope=basic,netdisk&error=access_denied'.format(self.client_id, 'oob')

        print(url1)

        self.authorization_code = input("点击网页授权并输入authorization_code：")

    def init_refresh_token(self):
        url2 = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={}&client_id={}&' \
               'client_secret={}&scope=basic,netdisk&redirect_uri=oob'.format(self.authorization_code,
                                                                              self.client_id,
                                                                              self.client_secret)
        print(url2)

        res = requests.post(url2)
        token = demjson.decode(res.text)
        print(token)
        self.access_token = token['access_token']
        self.refresh_token = token['refresh_token']

    def refresh_access_token(self):
        url3 = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={}&client_id={}&' \
               'scope=basic,netdisk&client_secret={}'.format(self.refresh_token,
                                                             self.client_id,
                                                             self.client_secret)
        print(url3)
        res3 = requests.post(url3)

        token_new = demjson.decode(res3.text)
        print(token_new)
        self.access_token = token_new['access_token']
        self.refresh_token = token_new['refresh_token']

    def get_access_token(self):
        if self.access_token is not None:
            return self.access_token
        elif self.refresh_token is not None:
            self.refresh_access_token()
            return self.access_token
        else:
            self.init_refresh_token()
            self.refresh_access_token()
            return self.access_token
