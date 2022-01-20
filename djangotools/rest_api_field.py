# -*- coding: UTF8 -*-
from django.utils import timezone
from rest_framework import serializers


class CustomBaseField(serializers.Field):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data


class NativeDateTimeField(serializers.DateTimeField, CustomBaseField):

    def __init__(self, format_str="%Y-%m-%d %H:%M:%S", input_formats=None, default_timezone=None, *args, **kwargs):
        super(NativeDateTimeField, self).__init__(format=format_str, input_formats=input_formats,
                                                  default_timezone=default_timezone, *args, **kwargs)

    def to_representation(self, value):
        value = timezone.make_naive(value)
        return super(NativeDateTimeField, self).to_representation(value)


class Fen2YuanField(CustomBaseField):
    """
    分转成元，并保留两位小数
    """

    def to_representation(self, value: int):
        return round(value / 100, 2)
