# -*- coding: utf-8 -*-
from django.core.urlresolvers import get_script_prefix, set_script_prefix


class script_prefix(object):
    def __init__(self, newpath):
        self.newpath = newpath
        self.oldprefix = get_script_prefix()

    def __enter__(self):
        set_script_prefix(self.newpath)

    def __exit__(self, type, value, traceback):
        set_script_prefix(self.oldprefix)
