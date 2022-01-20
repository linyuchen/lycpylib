# -*- coding: UTF8 -*-
from urllib import parse
from .api_base import ApiBase


class UrlTool(ApiBase):

    def make_code_url(self, url):
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&" \
              "redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=123#wechat_redirect" % \
              (self.appid, parse.quote(url, safe=""))
        return url

