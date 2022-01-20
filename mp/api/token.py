# -*- coding: UTF8 -*-
import os
import json
import requests
import time


class TokenTool(object):

    def __init__(self, appid, appsecret):

        self.appid = appid
        self.appsecret = appsecret
        self.expires = 7200
        self.config_path = os.path.join(os.path.dirname(__file__), "config.json")

        self.configs = {f"{appid}": {
            "access_token": "",
            "access_token_time": 0.0,
            "jsapi_ticket": "",
            "jsapi_ticket_time": 0.0,
            "user_access_token": {},
        }}
        # self.read()

    def read(self):
        try:
            self.configs[self.appid] = json.load(open(self.config_path))
        except:
            pass

    def save(self):
        return
        json.dump(self.configs, open(self.config_path, "w"))

    def __check_expire(self, token_time):
        return time.time() - token_time >= self.expires

    def get_user_access_token(self, openid):
        user_access_token_data = self.configs[self.appid]["user_access_token"].get(openid, {})

    def set_user_access_token(self, openid, data):
        self.configs[self.appid]["user_access_token"][openid] = data
        self.save()

    def get_access_token(self):

        access_token = self.configs[self.appid]["access_token"]

        if access_token:
            if self.__check_expire(self.configs[self.appid]["access_token_time"]):
                self.__web_get_access_token()
        else:
            self.__web_get_access_token()

        return self.configs[self.appid]["access_token"]

    def refresh_access_token(self):
        self.__web_get_access_token()

    def get_jsapi_tiket(self):
        ticket = self.configs[self.appid]["jsapi_ticket"]
        if ticket:
            if self.__check_expire(self.configs[self.appid]["jsapi_ticket_time"]):
                self.__web_get_jsapi_ticket()
        else:
            self.__web_get_jsapi_ticket()

        return self.configs[self.appid]["jsapi_ticket"]

    def __web_get_jsapi_ticket(self):

        url = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % self.get_access_token()
        data = requests.get(url).json()
        ticket = data.get("ticket")
        self.configs[self.appid]["jsapi_ticket"] = ticket
        self.configs[self.appid]["jsapi_ticket_time"] = time.time()
        self.save()

    def __web_get_access_token(self):

        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
        url = url.format(appid=self.appid, secret=self.appsecret)
        resp = requests.get(url)
        res_json = resp.json()
        # print(res_json)
        access_token = res_json.get("access_token")
        self.configs[self.appid]["access_token"] = access_token
        self.configs[self.appid]["access_token_time"] = time.time()
        self.save()
