# -*- coding: UTF8 -*-
import json
import requests
from .token import TokenTool
from .api_base import ApiBase, api_res_checker


class MenuTool(ApiBase):

    @api_res_checker
    def create_menu(self, menu_data):
        # print menu_data
        url = "https://api.weixin.qq.com/cgi-bin/menu/create"
        return self.http_post(url, data=menu_data).json()
