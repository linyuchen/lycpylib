# -*- coding: UTF8 -*-
import requests
import json
from .token import TokenTool
from urllib.parse import parse_qsl, urlencode, urlparse


class APIResBase:
    errcode: int = 0
    errmsg: str = ""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def api_res_checker(api_func):
    def new_api_func(self: ApiBase, *args, **kwargs):
        res = api_func(self, *args, **kwargs)
        if isinstance(res, APIResBase):
            errcode = res.errcode
        else:
            errcode = res.get("errcode")
        if errcode == 40001:
            self.api_err_handle(res, api_func, *args, **kwargs)
            self.token_tool.refresh_access_token()
            return api_func(self, *args, **kwargs)
        elif errcode:
            self.api_err_handle(res, api_func, *args, **kwargs)
        return res
    return new_api_func


class ApiBase(object):

    def __init__(self, appid, appsecret, is_app=False):
        self.appid = appid
        self.appsecret = appsecret
        self.is_app = is_app
        self.token_tool = TokenTool(appid=appid, appsecret=appsecret)

    def __make_url(self, url):
        url_parse_result = urlparse(url)
        qs_dict = dict(parse_qsl(url_parse_result.query))
        if not qs_dict.get("access_token"):
            qs_dict["access_token"] = self.token_tool.get_access_token()
        url = f"{url_parse_result.scheme}://{url_parse_result.netloc}{url_parse_result.path}?{urlencode(qs_dict)}"
        return url

    def http_post(self, url, **kwargs):
        url = self.__make_url(url)
        if isinstance(kwargs.get("data", ""), dict):
            body = json.dumps(kwargs["data"], ensure_ascii=False)
            body = body.encode('utf8')
            kwargs["data"] = body
        return requests.post(url, **kwargs)

    def http_get(self, url, **kwargs):
        url = self.__make_url(url)
        return requests.get(url, **kwargs)

    def api_err_handle(self, err: APIResBase, api_func, *args, **kwargs):
        pass

