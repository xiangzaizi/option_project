# -*- coding:utf-8 -*-
"""封装Response对象"""
import json
import re
from lxml import etree

class Response(object):
    """框架内置Response对象"""
    def __init__(self, url, status_code, headers, body):
        self.url = url
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def xpath(self, rule):
        html_obj = etree.HTML(self.body)
        return html_obj.xpath(rule)

    # 将网页返回的json字符串, 转为python数据类型
    @property
    def json(self):
        return json.loads(self.body)

    def re_findall(self, rule, string=None):
        if string is None:
            string = self.body
        return re.findall(rule, string)

