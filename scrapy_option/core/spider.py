# -*- coding:utf-8 -*-
"""对爬虫组件进行封装"""
from scrapy_option.http.request import Request
from scrapy_option.item import Item


class Spider(object):
    """
    1. 构建请求信息生成请求对象
    2. 解析响应对象, 生成数据对象
    """

    start_url = "http://www.baidu.com"  # 框架初始测试url

    def start_request(self):
        # 构建初始请求对象并返回
        return Request(self.start_url)

    def parse_request(self, response):
        # 解析请求, 并返回新的请求对或者数据对象
        return Item(response.body)
