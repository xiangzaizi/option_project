# -*- coding:utf-8 -*-
"""自定义spider测试"""
from scrapy_option.core.spider import Spider


class BaiduSpider(Spider):
    start_url = "http://tieba.baidu.com"
