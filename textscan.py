# coding=utf-8
# 以下代码用于调用文本检测接口。
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
import json
import uuid
import datetime


class TextScan(object):
    """垃圾文本检测"""

    def __init__(self, content):
        self._clt = client.AcsClient("LTAI4GGVZ6XJKvbVru8F5fYx", "OTULNVRFv09CjTn09srw4fLLkJkdr2", 'cn-shanghai')
        self.conent = content
        self.dataId = str(uuid.uuid1())
        self.time = datetime.datetime.now().microsecond

    def response(self):
        region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
        # 每次请求时需要新建request，请勿复用request对象。
        request = TextScanRequest.TextScanRequest()
        request.set_accept_format('JSON')
        task1 = {"dataId": self.dataId,
                 "content": self.conent,
                 "time": self.time
                 }
        # 文本反垃圾检测场景的场景参数是antispam。
        request.set_content(bytearray(json.dumps({"tasks": [task1], "scenes": ["antispam"]}), "utf-8"))
        return self._clt.do_action_with_exception(request)

    def result(self, result):
        result = json.loads(result)
        print(result)
        if 200 == result["code"]:
            taskResults = result["data"]
            for taskResult in taskResults:
                if (200 == taskResult["code"]):
                    sceneResults = taskResult["results"]
                    for sceneResult in sceneResults:
                        suggestion = sceneResult["suggestion"]
                        return suggestion
        else:
            return None
