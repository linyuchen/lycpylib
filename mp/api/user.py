# -*- coding: UTF8 -*-
import json
import requests
from .token import TokenTool
from .api_base import ApiBase, api_res_checker


class UserTool(ApiBase):

    @api_res_checker
    def get_user_info(self, openid, access_token=None):
        # url = "https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={openid}&lang=zh_CN"
        # 这里的access_token是用户对应的access_token，每个用户的access_token都不一样？
        url = "https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
        if self.is_app:
            url = "https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
        token = self.token_tool.get_access_token()
        if access_token:
            token = access_token
        url = url.format(access_token=token, openid=openid)
        res = requests.get(url).content.decode("utf8")
        res = json.loads(res)
        return res

    @api_res_checker
    def get_users(self):
        """
        获取用户列表，只返回openid，一次可以拉取一万条
        :return:
        """
        url = "https://api.weixin.qq.com/cgi-bin/user/get"
        res = self.http_get(url).json()
        return res

    @api_res_checker
    def get_users_info(self, openids: list[str]):
        """
        获取用户列表，不仅返回openid，还返回用户基本信息，一次只能拉取一百条
        :return:
        """
        url = "https://api.weixin.qq.com/cgi-bin/user/info/batchget"
        data = {
            "user_list": [
                {"openid": openid} for openid in openids
            ]
        }
        res = self.http_post(url, json=data).json()
        return res

