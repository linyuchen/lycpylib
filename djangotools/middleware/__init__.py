# -*- coding:utf8 -*-
from django.utils.deprecation import MiddlewareMixin


class DisableCSRFCheck(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        setattr(request, '_dont_enforce_csrf_checks', True)
