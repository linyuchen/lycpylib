# -*- coding: UTF8 -*-
import requests
from .api_base import ApiBase, api_res_checker, APIResBase
from .token import TokenTool


class MiniPCode2OpenIDRes(APIResBase):
    openid: str
    session_key: str
    unionid: str


class AuthTool(ApiBase):

    @api_res_checker
    def __code2openid(self, code):
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
              "appid={appid}&secret={secret}&code={code}&grant_type=authorization_code"
        url = url.format(appid=self.appid, secret=self.appsecret, code=code)
        return requests.get(url).json()

    def code2openid(self, code):
        data = self.__code2openid(code)
        open_id = data.get("openid")
        return open_id, data.get("access_token")

    @api_res_checker
    def minip_code2openid(self, code) -> MiniPCode2OpenIDRes:
        """
        小程序
        :param code:
        :return:
        """
        url = f"https://api.weixin.qq.com/sns/jscode2session?appid={self.appid}&secret={self.appsecret}&js_code={code}&grant_type=authorization_code"
        res = requests.get(url).json()
        res = MiniPCode2OpenIDRes(**res)
        return res
