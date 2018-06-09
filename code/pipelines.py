# -*- coding:utf-8 -*-
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class BaiduPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print("BaiduSpider item:{}".format(item.data))

        return item


class DoubanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print("DoubanSpider item:{}".format(item.data))

        return item
