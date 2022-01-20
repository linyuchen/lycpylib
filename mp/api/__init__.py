# -*- coding:UTF-8 -*-

__author__ = "linyuchen"
__doc__ = """
"""
from .auth import AuthTool
from .token import TokenTool
from .url import UrlTool
from .user import UserTool
from .menu import MenuTool
from .module_msg import ModuleMsgTool
from .jssdk import JssdkTool
from .qrcode import QRCodeTool, QRCodeMiniAppTool
from .article import ArticleTool


class WechatPubApiBase(AuthTool, UrlTool, UserTool, ModuleMsgTool,
                       MenuTool, JssdkTool, QRCodeTool, ArticleTool):

    def __init__(self, appid, appsecret, is_app=False):
        super(WechatPubApiBase, self).__init__(appid, appsecret, is_app)
