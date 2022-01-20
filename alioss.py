# -*- coding: utf-8 -*-
import json
import oss2
from oss2 import ObjectIterator
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdksts.request.v20150401.AssumeRoleRequest import AssumeRoleRequest


class AliOSSApi:
    def __init__(self, endpoint, accesskey_id, accesskey_secret, bucket_name, host):
        """

        :param endpoint: https://help.aliyun.com/document_detail/31837.html?spm=a2c4g.11186623.2.13.2a74f2eeoLPsd6
        :param accesskey_id:
        :param accesskey_secret:
        :param bucket_name: 空间名
        :param host: 绑定的域名http host
        """
        auth = oss2.Auth(accesskey_id, accesskey_secret)
        self.host = host
        self.bucket = oss2.Bucket(auth, endpoint, bucket_name)

        # 构建一个阿里云客户端，用于发起请求。
        # 构建阿里云客户端时需要设置AccessKey ID和AccessKey Secret。
        self.acs_client = AcsClient(accesskey_id, accesskey_secret)  # 用户生成临时令牌

    def get_url(self, bucket_file_path):
        return f"{self.host}/{bucket_file_path}"

    def upload(self, local_file_path: str, bucket_file_path: str, **kwargs):
        bucket_file_path = bucket_file_path.removeprefix("/")
        self.bucket.put_object_from_file(bucket_file_path, local_file_path, **kwargs)
        return self.get_url(bucket_file_path)

    def download(self, local_file_path, bucket_file_path, **kwargs) -> str:
        """

        :param local_file_path:
        :param bucket_file_path:
        :return: 完整的url
        """
        self.bucket.get_object_to_file(bucket_file_path, local_file_path, **kwargs)
        return self.get_url(bucket_file_path)

    def delete(self, bucket_file_path, **kwargs):
        if isinstance(bucket_file_path, str):
            bucket_file_path = [bucket_file_path]
        self.bucket.batch_delete_objects(bucket_file_path, **kwargs)

    def list(self) -> ObjectIterator:
        return oss2.ObjectIterator(self.bucket)


class AliSTSApi:
    """
    生成阿里云OSS储存对象的临时凭证
    """
    def __init__(self, access_key: str, access_secret: str, arn: str, session: str):
        self.access_key = access_key
        self.access_secret = access_secret
        self.arn = arn
        self.session = session

    def create(self, duration_seconds: int = 60 * 15):
        """

        :param duration_seconds: 凭证有效期，单位秒, 15分到1小时之间
        :return:
        """

        acs_client = AcsClient(self.access_key, self.access_secret)  # 用户生成临时令牌
        # 构建请求。
        request = AssumeRoleRequest()
        request.set_accept_format('json')

        # 设置参数。
        request.set_RoleArn(self.arn)
        request.set_RoleSessionName(self.session)
        request.set_DurationSeconds(duration_seconds)

        # 发起请求，并得到响应。
        response = acs_client.do_action_with_exception(request)
        # python2:  print(response)
        # print(response['Credentials'])
        return json.loads(str(response, encoding="utf8"))
