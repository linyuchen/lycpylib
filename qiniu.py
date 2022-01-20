from typing import Tuple
from qiniu import Auth, put_file, etag, BucketManager


class QiniuTool:
    def __init__(self, access_key: str, access_secret: str, bucket: str):
        self.q = Auth(access_key, access_secret)
        self.bucket_name = bucket

    def get_upload_token(self, bucket_path, **kwargs) -> Tuple[str, str]:
        token = self.q.upload_token(self.bucket_name, bucket_path, 3600, **kwargs)
        return token, bucket_path

    def upload(self, local_path, bucket_path, **kwargs) -> str:

        put_file(self.get_upload_token(bucket_path)[0], bucket_path, local_path, **kwargs)
        return bucket_path

    def upload_remote(self, url: str, bucket_path: str) -> str:
        """

        :param url: 要转存的资源链接
        :param bucket_path: 七牛上保存的位置路径
        :return:
        """

        bucket_manager = BucketManager(self.q)
        bucket_manager.fetch(url, self.bucket_name, bucket_path)
        return bucket_path
