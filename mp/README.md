# django的settings配置

需要以下变量:

```python
STATIC_ROOT = "static"  # 静态文件路径
WECHAT_PUB_SERVER_HTTP_HOST = "http://xxx"
WECHAT_PUB_ID = "公众号的微信号"
WECHAT_PUB_APPID = ""
WECHAT_PUB_APPSECRET = ""
WECHAT_PUB_APPTOKEN = ""

WECHAT_PUB_QRCODE_URL = "http://xxx.jpg"  # 公众号二维码

```

同时需要把django_web这个文件夹加入到settings的INSTALLED_APPS

# TODO List

