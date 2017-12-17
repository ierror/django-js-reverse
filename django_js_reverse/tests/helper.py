# -*- coding: utf-8 -*-
from django import VERSION


def is_django_ver_gte_2():
    return VERSION[0] >= 2
