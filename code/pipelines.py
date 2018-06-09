# -*- coding:utf-8 -*-
from spiders.baidu import BaiduSpider
from spiders.douban import DoubanSpider


class BaiduPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, BaiduSpider):
            print(u"BaiduSpider item:{}".format(item.data))

        return item


class DoubanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(spider, DoubanSpider):
            print(u"DoubanSpider item:{}".format(item.data))

            # UnicodeEncodeError-->此处位置不添加u会报的错误
            # 'ascii' codec can't encode characters in position 0-5: ordinal not in range(128)

        return item
