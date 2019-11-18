#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/11 11:11
# @Author  : niuliangtao
# @Site    :
# @Software: PyCharm
import os

import demjson
import requests


class AccessToken:
    def __init__(self, api_key=None, secret_key=None, access_token=None, refresh_token=None, secret_dir='~/.secret'):
        self.secret = None
        secret_dir = secret_dir.replace("~", os.environ['HOME'])
        self.secret_path = '{}/.baidu_drive'.format(secret_dir)
        self.read()

        if api_key is not None:
            self.secret['token']['client_id'] = api_key
        if secret_key is not None:
            self.secret['token']['client_secret'] = secret_key

        if refresh_token is not None:
            self.secret['token']['refresh_token'] = refresh_token
        if access_token is not None:
            self.secret['token']['access_token'] = access_token

        self.write()

    def get_authorization_code(self):
        url1 = 'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id={}' \
               '&redirect_uri={}&scope=netdisk'.format(self.secret['token']['client_id'], 'oob')

        print(url1)

        self.secret['token']['authorization_code'] = input("点击网页授权并输入authorization_code：")
        self.write()

    def init_refresh_token(self):
        self.get_authorization_code()
        url2 = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code={}&client_id={}&' \
               'client_secret={}&scope=basic,netdisk&redirect_uri=oob' \
            .format(self.secret['token']['authorization_code'],
                    self.secret['token']['client_id'],
                    self.secret['token']['client_secret'])
        print(url2)

        res = requests.post(url2)
        tokens = demjson.decode(res.text)
        print(tokens)
        self.secret['token']['access_token'] = tokens['access_token']
        self.secret['token']['refresh_token'] = tokens['refresh_token']
        self.write()

    def refresh_access_token(self):
        url3 = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token={}&client_id={}&' \
               'scope=basic+netdisk&client_secret={}'.format(self.secret['token']['refresh_token'],
                                                             self.secret['token']['client_id'],
                                                             self.secret['token']['client_secret'])

        try:
            print(url3)
            res3 = requests.post(url3)

            token_new = demjson.decode(res3.text)
            print(token_new)
            self.secret['token']['access_token'] = token_new['access_token']
            self.secret['token']['refresh_token'] = token_new['refresh_token']
        except Exception as e:
            print(e)
        self.write()

    def get_access_token(self):
        if self.secret['token']['access_token'] is not None:
            return self.secret['token']['access_token']
        elif self.secret['token']['refresh_token'] is not None:
            self.refresh_access_token()

        else:
            self.init_refresh_token()
            self.refresh_access_token()

        self.write()
        return self.secret['token']['access_token']

    def read(self):
        try:
            self.secret = demjson.decode(open(self.secret_path).read())
        except Exception as e:
            print("read error ,init {}".format(e))

        if self.secret is None:
            self.secret = {'token': {}}
        if 'token' not in self.secret.keys() or not isinstance(self.secret['token'], dict):
            self.secret['token'] = {}

        for key in ['api_key', 'secret_key', 'access_token', 'refresh_token', 'authorization_code']:
            if key not in self.secret['token'].keys():
                self.secret['token'][key] = ""

        return self.secret

    def write(self):
        secret_dir = os.path.dirname(self.secret_path)

        if not os.path.exists(secret_dir):
            os.mkdir(secret_dir)

        with open(self.secret_path, 'w')as f:
            f.write(demjson.encode(self.secret))
