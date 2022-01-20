# -*- coding: UTF8 -*-

import time
import uuid
import hashlib
from .api_base import ApiBase


class JssdkTool(ApiBase):

    def jssdk_config(self, url: str) -> dict:
        """

        :param url: 当前网页url，不包含#部分
        :return:
        """
        ticket = self.token_tool.get_jsapi_tiket()
        noncestr = uuid.uuid4().hex
        timestamp = int(time.time())
        data = f"jsapi_ticket={ticket}&noncestr={noncestr}&timestamp={timestamp}&url={url}"
        # print url
        # print data
        sign = hashlib.sha1(data.encode("utf8")).hexdigest()
        config_data = {
            "appId": self.appid,
            "timestamp": timestamp,
            "nonceStr": noncestr,
            "signature": sign
        }
        return config_data

