# -*- coding: UTF8 -*-

import datetime
import requests
import time
import xmltodict
from hashlib import md5


# from lycxml import XmlParser


def api_res_checker(api_func):
    def new_api_func(self: "WechatPayApiBase", *args, **kwargs):
        xml_dict: dict = api_func(self, *args, **kwargs)
        code = xml_dict.get("return_code")
        if code == "SUCCESS":
            return True, "", ""

        err_msg = xml_dict.get("return_msg")
        self.api_err_handle(code, err_msg)
        return False, code, err_msg

    return new_api_func


class WechatPayApiBase(object):
    TRAD_TYPE_APP = "APP"
    TRAD_TYPE_JS = "JS"
    TRAD_TYPE_NATIVE = "NATIVE"

    def __init__(self, cert_pem_path: str, key_pem_path: str, mch_id: str, pay_key: str, wechatpub_appid: str):
        """

        :param cert_pem_path: 证书路径 (apiclient_cert.pem)
        :param key_pem_path: 密钥路径 (piclient_key.pem)
        :param mch_id: 商户号
        :param pay_key: api 密钥
        :param wechatpub_appid: appid
        """
        self.cert_paths = (
            cert_pem_path,
            key_pem_path
        )
        self.mch_id = mch_id
        self.pay_key = pay_key
        self.wechatpub_appid = wechatpub_appid
        self.host = "api.mch.weixin.qq.com"

    def api_err_handle(self, err_code, err_msg):
        pass

    @api_res_checker
    def refund(self, out_id, refund_fee, total_fee) -> dict:
        """

        :param out_id: 外部订单id, 商户自己设置的
        :param refund_fee:  退款金额，单位元
        :param total_fee:  订单总金额，单位元
        :return: xml dict
        """
        refund_fee *= 100  # 1元=100分
        total_fee *= 100
        url = "https://%s/secapi/pay/refund" % self.host

        data = {"appid": self.wechatpub_appid, "mch_id": self.mch_id,
                "nonce_str": "abcdef" + str(int(time.time())),
                "out_trade_no": out_id, "out_refund_no": out_id, "total_fee": int(total_fee),
                "refund_fee": int(refund_fee),
                "op_user_id": self.mch_id
                }
        self.make_sign(self.pay_key, data)
        result = requests.post(url=url, data=self.make_xml(data), cert=self.cert_paths).content
        return xmltodict.parse(result)

    @api_res_checker
    def send_red_packet(self, to_user, money, act_name, sender_name, remark, wishing) -> dict:
        """

        :param to_user:  接受红包的用户openid
        :param money: 金额,单位是分
        :param act_name: 活动名称
        :param sender_name: 发送方名称
        :param remark: 备注
        :param wishing: 祝福语
        :return: dict
        """
        act_name = act_name
        sender_name = sender_name
        remark = remark
        today = datetime.datetime.today()
        url = "https://%s/mmpaymkttransfers/sendredpack" % self.host

        data = {"nonce_str": "dsafjaosj",
                #  mch_id + today.strftime("%Y%m%d") + 10位数字, mach_billno必须是唯一的
                "mch_billno": self.mch_id + today.strftime("%Y%m%d") + ("%f" % time.time()).replace(".", "")[-10:],
                "mch_id": self.mch_id, "wxappid": self.wechatpub_appid,
                "send_name": sender_name, "re_openid": to_user,
                "total_amount": money, "total_num": 1, "wishing": wishing, "client_ip": "192.168.1.1",
                "act_name": act_name, "remark": remark
                }
        sign = self.make_sign(self.pay_key, data)
        data["sign"] = sign
        xml = self.make_xml(data)
        result = requests.post(url=url, data=xml, cert=self.cert_paths).content
        return xmltodict.parse(result)

    @api_res_checker
    def create_order(self, order_summary: str, out_trade_no: str, money: int, trade_type: str, product_id, to_user, notify_url, sign_callback) -> str:
        """
        :param order_summary: 订单简介
        :param out_trade_no: 订单编号,32个字符内, 唯一性
        :param money: 订单付款金额, 单位 分
        :param trade_type: 取值如下：JSAPI，NATIVE，APP
        :param product_id: 商品id
        :param to_user: 付款人的openid, 当trade_type=JSAPI，此参数必传
        :param notify_url: 接受支付结果通知的url
        :param jssdk_sign_callback: 签名回调函数, 接受一个dict类型的参数,
            dict: {
                timestamp: 0, // 支付签名时间戳，注意微信jssdk中的所有使用timestamp字段均为小写。但最新版的支付后台生成签名使用的timeStamp字段名需大写其中的S字符
                nonceStr: '', // 支付签名随机串，不长于 32 位
                package: '', // 统一支付接口返回的prepay_id参数值，提交格式如：prepay_id=\*\*\*）
                signType: '', // 签名方式，默认为'SHA1'，使用新版支付需传入'MD5'
                paySign: '', // 支付签名
            }
        :param sign_callback: 签名回调，把签好名的参数传出去
        :return: xml dict
        """
        money = int(money)
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        today = datetime.datetime.today()
        data = {"appid": self.wechatpub_appid, "mch_id": self.mch_id, "nonce_str": "hafnapfj",
                "body": order_summary,
                "out_trade_no": out_trade_no, "total_fee": money,
                "time_start": today.strftime("%Y%m%d%H%M%S"),
                "time_expire": (today + datetime.timedelta(days=2)).strftime("%Y%m%d%H%M%S"),
                "notify_url": notify_url, "trade_type": trade_type, "product_id": product_id}
        if to_user:
            data["openid"] = to_user

        # print data
        sign = self.make_sign(self.pay_key, data)
        data["sign"] = sign
        xml = self.make_xml(data)
        # print(xml.decode("utf8"))
        __res = requests.post(url=url, data=xml)
        result = __res.content

        xml = xmltodict.parse(result)["xml"]
        nonce_str = xml.get("nonce_str", "")
        prepay_id = xml.get("prepay_id", "")
        timestamp = int(time.time())

        sign_data = {}
        if trade_type == self.TRAD_TYPE_JS:
            sign_data = {"timeStamp": timestamp, "nonceStr": nonce_str, "package": "prepay_id=" + prepay_id, "signType": "MD5", "appId": self.wechatpub_appid}
            sign = self.make_sign(self.pay_key, sign_data)
            sign_data["paySign"] = sign
            sign_data["timestamp"] = timestamp
        elif trade_type == self.TRAD_TYPE_APP:
            sign_data = {"timestamp": str(timestamp), "noncestr": nonce_str,
                         "package": "Sign=WXPay", "appid": self.wechatpub_appid, "partnerid": self.mch_id, "prepayid": prepay_id}

            sign = self.make_sign(self.pay_key, sign_data)
            sign_data["sign"] = sign
        sign_callback(sign_data)

        return xmltodict.parse(result)

    @staticmethod
    def make_xml(dic):
        xml = "<xml>"
        for k in dic:
            # print k, dic[k]
            text = u"<{key}><![CDATA[{data}]]></{key}>".format(key=k, data=dic[k])
            xml += text

        xml += "</xml>"
        xml = xml.encode("u8")
        return xml

    @staticmethod
    def make_sign(pay_key, data: dict):

        keys = sorted(data.keys())
        vs = []
        for k in keys:
            vs.append(u"%s=%s" % (k, data[k]))

        vs = "&".join(vs)
        vs += ("&key=" + pay_key)
        # print vs
        vs = vs.encode("u8")
        sign = md5(vs).hexdigest().upper()
        data["sign"] = sign
        return sign


if __name__ == "__main__":
    test = WechatPayApiBase()
    touser = ""
    # xml = test.create_order(u"没有什么".encode("u8"), "112234", 100, "JSAPI", 1, touser)
    # print xml.get_element_text("return_msg")
    # xml = test.send_red_packet("o36q4wM9B7QMPgANgZGKFecfLbqI", 100, u"打折提现", u"我母鸡", u"请尽快领取", u"谢谢您支持我母鸡")
    # print xml
    # xml = XmlParser(xml_data=xml.encode("u8"))
    # print xml.get_element_text("return_code")
    # print xml.get_element_text("return_msg")
    # print xml.get_element_text("result_code")
    res = test.refund("1480560501437", 0.1, 0.1)
    print(res)
    print(test.check_result(res))
