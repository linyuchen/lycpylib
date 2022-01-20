import json
import urllib
import requests
from enum import Enum
from dataclasses import dataclass
from .api_base import ApiBase, api_res_checker, APIResBase


class ResUploadMedia(APIResBase):
    media_id: str
    url: str


class ResUploadArticle(APIResBase):
    media_id: str


class ResSendArticle(APIResBase):
    type: str
    msg_id: str


class ArticleMediaType(Enum):
    IMAGE = "image"
    VOICE = "voice"
    VIDEO = "video"
    THUMB = "thumb"


class Article:
    title: str
    content: str
    digest: str = ""
    thumb_media_id: str = ""
    show_cover_pic: bool = True
    need_open_comment: bool = True
    only_fans_can_comment: bool = False
    author: str = ""
    content_source_url: str = ""

    def to_dict(self):
        data = {
            "thumb_media_id": self.thumb_media_id,
            "title": self.title,
            "content": self.content,
            "digest": self.digest,
            "show_cover_pic": int(self.show_cover_pic),
            "need_open_comment": int(self.need_open_comment),
            "only_fans_can_comment": int(self.only_fans_can_comment),
            "author": self.author,
            "content_source_url": self.content_source_url
        }
        return data


class ArticleTool(ApiBase):
    """
    文章相关
    上传图片，生成文章，群发文章
    """

    def __upload_file(self, url, path):
        f = open(path, "rb")
        files = {
            "media": (f.name, f)
        }
        res = self.http_post(url, files=files, headers={"Content-Type": "multipart/form-data"}).json()
        return res

    @api_res_checker
    def upload_file_tmp(self, path: str, media_type: ArticleMediaType) -> ResUploadMedia:
        url = f"https://api.weixin.qq.com/cgi-bin/media/upload?type={media_type.value}"
        res = self.__upload_file(url, path)
        return ResUploadMedia(**res)

    @api_res_checker
    def upload_file_forever(self, path: str, media_type: ArticleMediaType) -> ResUploadMedia:
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?type={media_type.value}"
        res = self.__upload_file(url, path)
        return ResUploadMedia(**res)

    @api_res_checker
    def add_news(self, articles: list[Article]):
        url = "https://api.weixin.qq.com/cgi-bin/material/add_news"
        data = {
            "articles": [article.to_dict() for article in articles]
        }
        res = self.http_post(url, data=data).json()
        return res

    @api_res_checker
    def upload_article(self, articles: list[Article]):
        url = "https://api.weixin.qq.com/cgi-bin/material/add_news"
        data = {
            "articles": [article.to_dict() for article in articles]
        }

        res = self.http_post(url, data=data).json()
        res = ResUploadArticle(**res)
        return res

    @api_res_checker
    def send_article(self, to_user: list[str], media_id: str):
        data = {
            "touser": to_user,
            "mpnews": {
                "media_id": media_id
            },
            "msgtype": "mpnews",
            "send_ignore_reprint": 0
        }

        url = 'https://api.weixin.qq.com/cgi-bin/message/mass/send'
        res = self.http_post(url, json=data).json()
        res = ResSendArticle(**res)
        return res

    @api_res_checker
    def get_medias(self):
        url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material"
        data = {
            "type": "news",
            "offset": 0,
            "count": 20
        }
        res = self.http_post(url, json=data).json()
        return res

