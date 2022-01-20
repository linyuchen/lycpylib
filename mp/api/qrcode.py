# -*- coding: UTF8 -*-
import json
import requests
from .api_base import ApiBase, api_res_checker


class QRCodeMiniAppTool(ApiBase):
    """
    生成小程序的二维码
    """

    def __create_unlimited(self, scene_str: str):
        url = "https://api.weixin.qq.com/wxa/getwxacodeunlimit"
        param = {
            "scene": scene_str
        }
        res = self.http_post(url, json=param)
        data = res.content
        try:
            json_data = res.json()
            if json_data.get("errcode") == 40001:
                print(f"access_token: 失效, {url}")
                self.token_tool.refresh_access_token()
                res = self.http_post(url, json=param)
                data = res.content
        except:
            pass
        return data

    def create_qrcode(self, scene_str: str, save_path: str) -> str:
        """

        :param scene_str:
        :param save_path: 保存二维码的本地路径
        :return:
        """
        with open(save_path, "wb") as f:
            f.write(self.__create_unlimited(scene_str))


class QRCodeTool(ApiBase):
    """
    """

    @api_res_checker
    def __create_qrcode(self, scene_str: str, limit: bool) -> dict:
        """

        :param scene_str: 场景id
        :param limit: 是否永久二维码, 永久二维码，是无过期时间的，但数量较少（目前为最多10万个）
        :return:
        """
        url = "https://api.weixin.qq.com/cgi-bin/qrcode/create"
        data = {
            "expire_seconds": 2592000,
            "action_info":
                {
                    "scene":
                        {
                            "scene_str": scene_str
                        }
                }
        }

        if limit:
            data["action_name"] = "QR_LIMIT_STR_SCENE"
        else:
            data["action_name"] = "QR_STR_SCENE"

        return requests.post(url, json.dumps(data)).json()

    def create_qrcode(self, scene_str: str, limit=False):
        """
        公众号的二维码
        :param scene_str:
        :param limit:
        :return:
        """
        res = self.__create_qrcode(scene_str, limit)
        ticket = res.get("ticket", "")
        url = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=" + ticket
        return url
