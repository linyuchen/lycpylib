import json
import random
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_sms(phone, code=""):
    """
    发送短信验证码
    """
    if not code:
        code = ''
        for i in range(6):
            add = random.choice(str(random.randrange(10)))
            code += str(add)
    code_json = {
        "code": code
    }
    code_data = json.dumps(code_json)
    client = AcsClient('', '', 'cn-hangzhou')
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "推推鱼")
    request.add_query_param('TemplateCode', "SMS_206640177")
    request.add_query_param('TemplateParam', code_data)
    response = client.do_action(request)
    response = json.loads(str(response, encoding='utf-8'))
    if response["Message"] == "OK":
        return code
    else:
        return None
