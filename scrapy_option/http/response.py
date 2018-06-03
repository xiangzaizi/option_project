# -*- coding:utf-8 -*-
"""封装Response对象"""


class Response(object):
    """框架内置Response对象"""
    def __init__(self, url, status_code, headers, body):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body
