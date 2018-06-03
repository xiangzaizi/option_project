# -*- coding:utf-8 -*-
"""自定义spider测试"""
from scrapy_option.core.spider import Spider


class BaiduSpider(Spider):
    start_url = [
        "http://news.baidu.com",
        "http://www.baidu.com/",
        "http://news.baidu.com/"
    ]
