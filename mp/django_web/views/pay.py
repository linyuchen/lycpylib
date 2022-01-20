# -*- coding: UTF8 -*-
import xmltodict
from django.views.generic import View
from django.http.response import HttpResponse
from django.conf import settings
from ...api.pay import WechatPayApiBase


class WechatPayResultBaseView(View):

    def post(self, request, *args, **kwargs):
        xml_data = request.body
        dict_data = xmltodict.parse(xml_data)
        dict_data = dict_data["xml"]
        sign = dict_data.pop("sign")
        sign2 = WechatPayApiBase.make_sign(settings.WECHAT_PAY_KEY, dict_data)
        if sign == sign2 and (dict_data.get("result_code") == dict_data.get("return_code") == "SUCCESS"):
            self.handle_paid(dict_data)

        res = """<xml>
          <return_code><![CDATA[SUCCESS]]></return_code>
          <return_msg><![CDATA[OK]]></return_msg>
        </xml>
        """
        return HttpResponse(res)

    def handle_paid(self, result_data: dict):
        """

        :param result_data: {out_trade_no, total_fee(单位分)}
        :return:
        """
        pass
