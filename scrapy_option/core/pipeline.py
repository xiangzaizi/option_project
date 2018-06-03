# -*- coding:utf-8 -*-
"""对管道组件的封装"""
from scrapy_option.utils.log import logger


class Pipeline(object):
    # 处理数据对象(Item)

    def process_item(self, item):
        # 处理item对象, 接受数据对象作为参数
        # print ("item:", item)
        # 将测试的数据输出到日志
        logger.info("item数据为:{}".format(item))