# -*- coding:utf-8 -*-
"""对爬虫组件进行封装"""
from scrapy_option.http.request import Request
from scrapy_option.item import Item


class Spider(object):
    """
    1. 构建请求信息生成请求对象
    2. 解析响应对象, 生成数据对象
    """

    # start_url = "http://www.baidu.com"  # 框架初始测试url
    start_urls = []  # 多个url请求

    def start_request(self):
        # 处理多个url
        request_list = []
        for start_url in self.start_urls:
            # 构建初始请求对象冰并返回
            request_list.append(Request(start_url))

        return request_list

    def parse(self, response):
        # 解析请求, 并返回新的请求对或者数据对象
        return Item(response.body)
