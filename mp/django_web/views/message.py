# -*- coding: UTF8 -*-
import time
from hashlib import sha1
from django.conf import settings
from django.views.generic import View
from django.http.response import HttpResponse, Http404
from common.tools.lycxml import XmlParser


class ReMsgPackage(HttpResponse):
    def __init__(self, to_user: str, msg_type: str):
        """

        :param to_user: user open_id
        :param msg_type:
        """
        self.msg_type = msg_type
        self.to_user = to_user
        self.xml = XmlParser(xml_data="")

        self.xml.add_element("ToUserName", self.to_user, is_cdata=True)
        self.xml.add_element("FromUserName", settings.WECHAT_PUB_ID, is_cdata=True)
        self.xml.add_element("MsgType", self.msg_type, is_cdata=True)
        self.xml.add_element("CreateTime", int(time.time()))
        super(ReMsgPackage, self).__init__()

    def to_string(self):
        return self.xml.to_string(encoding="utf8")#.decode("utf8").replace('<?xml version="1.0" encoding="utf8"?>', "")


class TextMsgPackage(ReMsgPackage):
    def __init__(self, to_user, content):
        super(TextMsgPackage, self).__init__(to_user, "text")
        self.__content = content
        self.xml.add_element("Content", self.__content, is_cdata=True)
        self.content = self.to_string()


class ImageMsgPackage(ReMsgPackage):
    def __init__(self, to_user, media_id):
        super(ImageMsgPackage, self).__init__(to_user, "image")
        img_child = self.xml.add_element("Image", self.__content, is_cdata=True)
        self.xml.add_element("MediaId", media_id, is_cdata=True, parent_element=img_child)
        self.content = self.to_string()


class NewsMsgItem:
    xml = XmlParser(xml_data="<item></item>")

    def __init__(self, title, desc, pic_url, url):
        self.xml.add_element("Title", title, is_cdata=True)
        self.xml.add_element("Description", desc, is_cdata=True)
        self.xml.add_element("PicUrl", pic_url, is_cdata=True)
        self.xml.add_element("Url", url, is_cdata=True)


class NewsMsgPackage(ReMsgPackage):
    """
    图文消息
    """

    def __init__(self, to_user, items=list[NewsMsgItem]):
        super(NewsMsgPackage, self).__init__(to_user, "news")
        self.xml.add_element("ArticleCount", str(len(items)))
        self.articles_child = self.xml.add_element("Articles")
        for i in items:
            self.__add_item(i)
        self.content = self.to_string()

    def __add_item(self, item):
        self.articles_child.appendChild(item.xml.root)


class TransferCoustomerServiecPackage(ReMsgPackage):
    def __init__(self, to_user):
        super(TransferCoustomerServiecPackage, self).__init__(to_user, "transfer_customer_service")
        self.content = self.to_string()


class WechatPubMessageBaseView(View):

    @staticmethod
    def check_signature(request):
        sig = request.GET.get("signature", "")
        timestamp = request.GET.get("timestamp", "")
        nonce = request.GET.get("nonce", "")
        str_list = [settings.WECHAT_PUB_APPTOKEN, timestamp, nonce]
        str_list.sort()
        sig_ = "".join(str_list)
        if sha1(bytes(sig_, "utf8")).hexdigest() == sig:
            res = request.GET["echostr"]
            return True, HttpResponse(res)
        else:
            return False, ""

    def get(self, request, *args, **kwargs):
        success, res = self.check_signature(request)
        if success:
            return res
        raise Http404

    def post(self, request, *args, **kwargs):
        xmldata = XmlParser(xml_data=request.body)
        user_open_id = xmldata.get_element_text("FromUserName")
        msg_type = xmldata.get_element_text("MsgType")
        handle_result = None
        if msg_type == "event":
            event_name = xmldata.get_element_text("Event").lower()
            handle_result = self.handle_event(user_open_id, event_name, xmldata)
        elif msg_type in ["text", "voice", "image", "video", "shortvideo", "location", "link"]:
            handle_result = self.handle_msg(user_open_id, msg_type, xmldata)
        if handle_result:
            return handle_result
        return HttpResponse("success")

    def handle_event(self, from_user_open_id: str, event_name: str, xml_data: XmlParser):
        pass

    def handle_msg(self, from_user_open_id: str, msg_type: str, xml_data: XmlParser)->HttpResponse:
        pass
