# -*- coding: UTF8 -*-

import json
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
from typing import List
from collections.abc import Iterable
from django.http.response import JsonResponse
from django.core.paginator import Paginator
from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from .respack import status
from user.models import User
from django.utils import timezone


SECRET_KEY = 'le6974edbdb6d26cda884a440642a9bc93131128822b5a316371acc75308e81d9'
ALGORITHM = 'HS256'


def gen_jwt_token(user_id: int, expire_days: Optional[int] = 30):
    data = {"user_id": user_id}
    expire = timezone.datetime.now() + timezone.timedelta(days=expire_days)
    data.update({'expire': expire.timestamp()})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_jwt_token(token: str) -> Optional[int]:
    """
    返回user_id
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id', -1)
        exp = payload.get('expire', -1)
    except:
        return None
    if datetime.now().timestamp() - exp >= 0:
        return None
    return user_id


class ApiBaseView(APIView):
    err_msg: str = ""
    ERR: int = status.ERR
    NOT_LOGIN_ERR: int = status.NOT_LOGIN_ERR
    OK: int = status.OK
    auth_http_method_names: List[str] = ["post", "delete"]

    def err_response(self, err_msg):
        self.err_msg = err_msg
        return Response()

    def ok_response(self, data={}):
        self.err_msg = ""
        return Response(data)

    def format_errors(self, errors):
        self.err_msg = json.dumps(errors)
        return self.err_msg

    @staticmethod
    def get_user(user_id: int):
        """
        根据user id查找user
        """
        return User.objects.filter(id=user_id).first()

    def dispatch(self, request: Request, *args, **kwargs):

        if request.method.lower() in self.auth_http_method_names:
            token = request.headers.get("Authorization", "")
            if token:
                user_id = verify_jwt_token(token)
                user = self.get_user(user_id)
                if user:
                    request.user = user

            if not request.user.is_authenticated:
                data = {"code": self.NOT_LOGIN_ERR, "msg": u"请先登录", "data": {}}
                res = JsonResponse(data)
                res.data = data
                return res

        res = super(ApiBaseView, self).dispatch(request, *args, **kwargs)
        if self.err_msg:
            res.data = {
                "code": self.ERR,
                "msg": self.err_msg,
                "data": {}
            }
        elif res.status_code == 200:
            res.data = {
                "code": self.OK,
                "data": res.data
            }
        elif res.status_code == 403:
            res.data = {
                "code": self.NOT_LOGIN_ERR,
                "msg": res.data["detail"],
                "data": {}
            }
        else:
            res.data = {
                "code": self.ERR,
                "msg": res.data.get("detail", ""),
                "data": {}
            }
        return res


class LycApiBaseView(ApiBaseView):
    # authentication_classes = []
    permission_classes: List[BasePermission] = [IsAuthenticated]
    serializer_class = None
    model_class = None
    update_key = "id"

    def __get_model_class(self):
        if not self.model_class:
            self.model_class = self.serializer_class.Meta.model
        return self.model_class

    def filter_exist_many_save(self, exist_keys):
        """
        检查已有的多个id
        :param exist_keys:
        :return:
        """
        exist = self.__get_model_class().objects.filter(id__in=exist_keys)
        return exist

    def filter_exist_save(self, exist_key):
        """
        检查已有的id
        :param exist_key:
        :return:
        """
        exist = self.__get_model_class().objects.filter(id=exist_key).first()
        return exist

    def filter_instance(self, save_item):
        """
        这里可以对保存时的每项实例进行操作
        :param save_item: 新建或者更新的实例
        :return:
        """
        pass

    def save(self, data, exist_key="", many=False):

        if isinstance(data, dict) and not data.get(exist_key):
            exist_key = None
            data[exist_key] = None

        if exist_key:
            if many:
                exist_keys = [i.get(exist_key) for i in data]
                exist = self.filter_exist_many_save(exist_keys)

            else:
                exist_key = data.get(exist_key)
                exist = self.filter_exist_save(exist_key)

            if isinstance(exist, QuerySet):
                for i in exist:
                    check_result = self.check_model_save_permission(i)
                    if not check_result:
                        return self.err_response("权限不足")
            elif exist:
                check_result = self.check_model_save_permission(exist)
                if not check_result:
                    return self.err_response("权限不足")

            serializer = self.serializer_class(exist, data=data, many=many)
        else:
            serializer = self.serializer_class(data=data, many=many)
        if not serializer.is_valid():
            return Response(self.format_errors(serializer.errors))

        save_instance = serializer.save()
        if isinstance(save_instance, Iterable):
            for i in save_instance:
                self.filter_instance(i)
        else:
            self.filter_instance(save_instance)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = self.__get_model_class().objects.all()
        return queryset

    def reads(self):
        queryset = self.get_queryset()
        try:
            iter(queryset)
            many = True
        except TypeError:
            many = False
        # if isinstance(queryset, Iterable):
        #     many = True
        if not queryset and not many:
            return Response()
        else:
            res = Response(self.serializer_class(queryset, many=many).data)
            return res

    def delete(self, request, *args, **kwargs):
        ids = request.data.get("ids")
        self.get_queryset().filter(id__in=ids).delete()
        return Response()

    def get(self, request, *args, **kwargs):
        return self.reads()

    def post(self, request, *args, **kwargs):
        many = False
        if isinstance(request.data, list):
            many = True
        return self.save(exist_key=self.update_key, data=request.data, many=many)

    def check_model_save_permission(self, queryset_item) -> bool:
        """
        是否有权限保存
        :param queryset_item:
        :return:
        """
        return True


class PagesApi(LycApiBaseView):

    num_of_page: int = 30
    overflow_page_null = True  # 超过最大页数返回空列表
    use_rest_response = True

    def __init__(self):
        super(PagesApi, self).__init__()
        self.pages = 0
        self.total = 0  # 总数量

    def pages_queryset(self, queryset):
        self.total = queryset.count()
        paginator = Paginator(queryset, self.num_of_page)
        self.pages = paginator.num_pages
        query_page = self.get_query_page()
        if query_page > self.pages:
            if self.overflow_page_null:
                return []
            query_page = self.pages
        query_p = paginator.page(query_page)
        return query_p.object_list

    def get_queryset(self):
        queryset = super(PagesApi, self).get_queryset()
        return self.pages_queryset(queryset)

    def get_query_page(self) -> int:
        page = self.request.query_params.get("p", "1")
        try:
            page = int(page)
        except ValueError:
            page = 1

        return page

    def dispatch(self, request, *args, **kwargs):
        response = super(PagesApi, self).dispatch(request, *args, **kwargs)
        if not self.use_rest_response:
            return response
        if not isinstance(response, Response):
            return response
        results = response.data.get("data", [])
        new_data = {
            "data":
                {
                    "results": results,
                    "pages": self.pages,
                    "total": self.total,
                    "page_size": self.num_of_page
                }
        }
        response.data.update(new_data)
        return response


class NoAuthGetApiView(LycApiBaseView):
    http_method_names = ["get"]
    auth_http_method_names = []
    permission_classes = []


class NoAuthPostApiView(LycApiBaseView):
    http_method_names = ["post"]
    auth_http_method_names = []
    permission_classes = []
