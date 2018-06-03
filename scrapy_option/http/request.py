# -*- coding:utf-8 -*-
"""封装Request对象"""


class Request(object):
    """框架内置请求对象, 设置请求信息"""
    def __init__(self, url, method='GET', headers=None, params=None, data=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data
