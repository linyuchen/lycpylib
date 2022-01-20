# -*- coding:UTF-8 -*-

__author__ = "linyuchen"
__doc__ = """
"""
from test_api import wechatpub_api

qrcode_url = wechatpub_api.create_qrcode("login_2765242")
print(qrcode_url)

