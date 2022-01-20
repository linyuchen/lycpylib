# -*- coding: UTF8 -*-
import re
from typing import Optional
from dataclasses import dataclass
from django.http.response import HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.views import static
from django.shortcuts import render
from django.conf import settings
from ... import WechatPubApiBase


@dataclass
class WXUserInfo:
    nickname: str
    subscribe: int
    headimgurl: str
    openid: str
    unioid: Optional[str]

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class WechatAuthBaseView(View):
    server_http_host = settings.WECHAT_PUB_SERVER_HTTP_HOST

    # WechatPubApiBase Object
    wechatpub_api_object = WechatPubApiBase(appid=settings.WECHAT_PUB_APPID, appsecret=settings.WECHAT_PUB_APPSECRET)

    subscribe_message = ""
    subscribe_qrcode_url = settings.WECHAT_PUB_QRCODE_URL

    must_authenticate = False  # 哪怕已经登陆过了也需要微信认证

    ignore_path = []

    def user_info_handle(self, user_info: WXUserInfo):
        """
        :param user_info:
            {
            nickname: 昵称
            subscribe: 0 or 1, 0为未关注
            headimgurl: 头像url
            sex: 性别，0未知，1男，2女
            openid: 微信用户唯一id,
            unionid: 微信开放平台用户唯一id，绑定了微信开放平台才有此字段
            }
        :return:
        """
        subscribe = user_info.subscribe
        if subscribe is None:
            return self.auth_fail_handle()
        if subscribe == 0:
            return render(self.request, "wechatpub/subscribe.html", {"subscribe_message": self.subscribe_message,
                                                                     "subscribe_qrcode_url": self.subscribe_qrcode_url})

    def auth_fail_handle(self):
        path = self.request.get_full_path()
        auth_url = self.wechatpub_api_object.make_code_url(self.server_http_host + path)
        return HttpResponseRedirect(auth_url)

    def dispatch(self, request, *args, **kwargs):
        for ignore_path in self.ignore_path:
            if re.match(ignore_path, request.path):
                return super(WechatAuthBaseView, self).dispatch(request, *args, **kwargs)
        code = request.GET.get("code")  # 微信传过来的
        if not request.user.is_authenticated or self.must_authenticate:
            if code:
                openid, access_token = self.wechatpub_api_object.code2openid(code)
                if not openid:
                    return self.auth_fail_handle()
                user_info = self.wechatpub_api_object.get_user_info(openid, access_token)
                user_info = WXUserInfo(**user_info)
                handle_result = self.user_info_handle(user_info)
                if handle_result:
                    return handle_result
            else:
                return self.auth_fail_handle()

        return super(WechatAuthBaseView, self).dispatch(request, *args, **kwargs)


class ApiWechatAuthBase(WechatAuthBaseView):

    def user_info_handle(self, user_info):
        pass

    def auth_fail_handle(self):
        return JsonResponse({
            "code": -1,
            "msg": "请先登录!"
        })


class WechatHtmlAuthBaseView(WechatAuthBaseView):
    """
    前端html文件当做静态文件直接输出，同时做一层身份验证
    验证逻辑在父类
    """
    STATIC_PATH = "wechatpub/html"

    def get(self, request, *args, **kwargs):
        return self.get_file(request, *args, **kwargs)

    @classmethod
    def get_file(cls, request, *args, **kwargs):
        html_name = kwargs.get("html_name", "index.html")
        return static.serve(request, f"{cls.STATIC_PATH}/{html_name}", settings.STATIC_ROOT)
