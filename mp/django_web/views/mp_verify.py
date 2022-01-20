# -*- coding: UTF8 -*-
from django.views.generic import View
from django.http.response import HttpResponse


class MPVerifyView(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse(kwargs.get("code", ""))
