# -*- coding:utf-8 -*-
from scrapy_option.core.spider import Spider


class BaiduSpider(Spider):
    name = "baidu"
    start_url = [
        "http://news.baidu.com/",
        "http://www.baidu.com/",
        "http://news.baidu.com/"
    ]