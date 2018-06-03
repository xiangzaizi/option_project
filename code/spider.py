# -*- coding:utf-8 -*-
"""自定义spider测试"""
from scrapy_option.core.spider import Spider
from scrapy_option.http.request import Request
from scrapy_option.item import Item


class BaiduSpider(Spider):
    start_url = [
        "http://news.baidu.com",
        "http://www.baidu.com/",
        "http://news.baidu.com/"
    ]


class DoubanSpider(Spider):
    # 豆瓣电影抓取
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko"}

    def start_request(self):
        start_urls = ["https://movie.douban.com/top250?start=" + str(page) for page in range(0, 226, 25)]

        for start_url in self.start_urls:
            yield Request(start_url, headers=self.headers)  # 这里就会直接交给engine内部对多url请求做遍历

    def parse(self, response):
        for node in response.xpath("//div[@class='hd']"):
            title = node.xpath(".//span[@class='title'][1]/text()")[0]
            link = node.xpath("./a/@href")[0]
            yield Request(link, headers=self.headers, parse="parse_ext")

    def parse_next(self, response):
        yield Item(response.xpath("//title/text()")[0].strip())