# -*- coding:utf-8 -*-
"""引擎组件
1. 对外提供整个程序的入口
2. 依次调用其他组件对外提供的接口, 实现整个框架的运作
"""
# 1. 导入请求响应
from scrapy_option.http.request import Request
from scrapy_option.http.response import Response

# 2. 导入核心组件
from .spider import Spider
from .scheduler import Scheduler
from .downloader import Downloader
from .pipeline import Pipeline
from scrapy_option.item import Item


class Engine(object):
    def __init__(self):
        # 创建初始化对象
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

    def start(self):
        # 启动engine
        self._start_engine()

    def _start_engine(self):
        # 1. 构建爬虫发送请求
        start_request = self.spider.start_request()

        # 2. 请求入调度器
        self.scheduler.add_request(start_request)

        while True:
            # 3. 获取调度器中的请求对象
            request = self.scheduler.get_request()

            # 当队列中的请求为空的时候, 退出程序
            if request is None:
                break

            # 4. 将请求交个下载器
            response = self.downloader.get_response(request)

            # 5. 得到响应对象交给spider解析数据
            result = self.spider.parse_request(response)

            # 6. 判断解析出来的结果进行在判断
            if isinstance(result, Request):
                # 是请求继续入队列请求数据
                self.scheduler.add_request(result)
            elif isinstance(result, Item):
                # 得到请求的数据转到管道, 进行存储
                self.pipeline.process_item(result)
            else:
                raise Exception("Error: parse返回的数据不能被处理")




