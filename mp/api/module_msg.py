# -*- coding: UTF8 -*-
import json
import requests
from .token import TokenTool
from .api_base import ApiBase, api_res_checker


class ModuleMsgTool(ApiBase):

    @api_res_checker
    def __get_module_id(self, template_id):
        """
        :param template_id: 模板库中模板的编号，
        :return:
        """
        url = "https://api.weixin.qq.com/cgi-bin/template/api_add_template"
        res = self.http_post(url, data={"template_id_short": template_id}).json()
        return res

    def get_module_msg_id(self, template_id):
        res = self.__get_module_id(template_id)
        return res.get("template_id")

    @api_res_checker
    def __send(self, to_user_open_id, module_id, url="", **params):
        """

        :param to_user_open_id: open_id
        :param module_id:
        :param url: 点击后跳转的url
        :param params: {param_name, value}, value encoding unicode
        :return: result
        :rtype: dict
        """

        data = {
            "touser": to_user_open_id,
            "template_id": module_id,
            "url": url,
            "topcolor": "#FF0000",
            "data": {

            }
        }
        # print params
        for key, value in params.items():
            if isinstance(value, dict):
                data["data"][key] = value
            else:
                data["data"][key] = {"value": value, "color": "#000000"}

        # print data
        url = "https://api.weixin.qq.com/cgi-bin/message/template/send"
        # print url
        res = self.http_post(url, data=data).json()
        return res

    def send_module_msg(self, to_user_open_id, module_id, url="", **params):
        return self.__send(to_user_open_id, module_id, url, **params)
