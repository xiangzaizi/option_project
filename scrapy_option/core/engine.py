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

# 3. 导入中间件middlwares
from scrapy_option.middlewares.spider_middlewares import SpiderMiddlewares
from scrapy_option.middlewares.downloader_middlewares import DownloaderMiddlewares


class Engine(object):
    def __init__(self):
        # 创建初始化对象
        self.spider = Spider()
        self.scheduler = Scheduler()
        self.downloader = Downloader()
        self.pipeline = Pipeline()

        # 初始化中间件文件
        self.spider_middlewares = SpiderMiddlewares()
        self.downloader_middlewares = DownloaderMiddlewares()

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

            ### 3.1 将请求经过下载中间件预处理--->请求
            request = self.downloader_middlewares.process_request(request)

            # 4. 将请求交个下载器
            response = self.downloader.get_response(request)

            ### 4.1 将响应经过下载中间件预处理--->响应
            response = self.downloader_middlewares.process_response(response)

            # 5. 得到响应对象交给spider解析数据
            result = self.spider.parse_request(response)

            # 6. 判断解析出来的结果进行在判断
            if isinstance(result, Request):

                ### 6.1 如果是请求对象, 交给爬虫中间件预处理, 添加请求入队列
                result = self.spider_middlewares.process_request(result)

                # 是请求继续入队列请求数据
                self.scheduler.add_request(result)

            elif isinstance(result, Item):

                ### 6.2 如果是Item数据, 爬虫中间件预处理,在交给管道
                result = self.spider_middlewares.process_item(result)

                # 得到请求的数据转到管道, 进行存储
                self.pipeline.process_item(result)

            else:
                raise Exception("Error: parse返回的数据不能被处理")




