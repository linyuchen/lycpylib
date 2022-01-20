# -*- coding:UTF-8 -*-

__author__ = "linyuchen"
__doc__ = """
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from test_config import APPID, APPSECRET
from api import WechatPubApiBase


wechatpub_api = WechatPubApiBase(appid=APPID, appsecret=APPSECRET)
