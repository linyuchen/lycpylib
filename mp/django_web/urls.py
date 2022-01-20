# -*- coding: UTF8 -*-
from django.conf.urls import url
from .views.wechat_auth import WechatHtmlAuthBaseView
from .views.mp_verify import MPVerifyView

urlpatterns = [
    # 这个是用于微信开发验证
    url("^MP_verify_(?P<code>.+)\.txt", MPVerifyView.as_view()),
]


wechat_html_auth_url = url(r"^wechatpub/fe/(?P<html_name>.+\.html$)", WechatHtmlAuthBaseView.as_view())
