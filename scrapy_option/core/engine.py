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

# 4. 在引擎中导入日志文件
from scrapy_option.utils.log import logger
from datetime import datetime


class Engine(object):
    def __init__(self, spiders, pipelines, spider_mids, downloader_mids):
        # 创建初始化对象
        # 接收实际项目spider,
        self.spiders = spiders

        self.scheduler = Scheduler()
        self.downloader = Downloader()
        # self.pipeline = Pipeline()
        # 完善框架处理多管道能力
        self.pipelines = pipelines


        # 初始化中间件文件
        # self.spider_middlewares = SpiderMiddlewares()
        # self.downloader_middlewares = DownloaderMiddlewares()

        # 框架完善处理项目重写的爬虫 下载中间件
        self.spider_mids = spider_mids
        self.downloader_mids = downloader_mids

    def start(self):
        # 添加日信息, 记录程序的运行时间
        start = datetime.now()
        logger.info("start time{}".format(start))

        # 启动engine
        self._start_engine()

        stop = datetime.now()
        logger.info("stop time{}".format(stop))

        # 记录程序运行时间
        # total_seconds()  计算两个时间之间的总差
        logger.info("total time{}".format((stop-start).total_seconds()))

    def _start_engine(self):
        for spider_name, spider in self.spiders.items:
            # 1.获取spider中的url请求list
            start_request_list = spider.start_request()

            for start_request in start_request_list:  # 处理spider发送的多个请求
                start_request.spider_name = spider.name

                ### 1.1请求经过爬虫中间件
                for spider_middlewares in self.spider_mids:
                    start_request = spider_middlewares.process_request(start_request)
                # 2. 请求入调度器
                self.scheduler.add_request(start_request)

        while True:
            # 3. 获取调度器中的请求对象
            request = self.scheduler.get_request()

            # 当队列中的请求为空的时候, 退出程序
            if request is None:
                break

            ### 3.1 将请求经过下载中间件预处理--->请求
            for downloader_middlewares in self.downloader_mids:
                request = downloader_middlewares.process_request(request)

            # 4. 将请求交个下载器
            response = self.downloader.get_response(request)

            ### 4.1 将响应经过下载中间件预处理--->响应
            for downloader_middlewares in self.downloader_mids:
                response = downloader_middlewares.process_response(response)

            # 5. 得到响应对象交给spider解析数据
            # results = self.spider.parse(response)
            # 1.request.parse--->取parse对应的解析方法
            spider = self.spiders[request.spider_name]
            parse_func = getattr(spider, request.parse)



            # 2.使用parse_next(处理响应)
            results = parse_func(response)

            for result in results:
                # 6. 判断解析出来的结果进行在判断
                if isinstance(result, Request):
                    result.spider_name = request.spider_name  # 给爬虫添加一个名字
                    ### 6.1 如果是请求对象, 交给爬虫中间件预处理, 添加请求入队列
                    for spider_middlewares in self.spider_mids:
                        result = spider_middlewares.process_request(result)

                    # 是请求继续入队列请求数据
                    self.scheduler.add_request(result)

                elif isinstance(result, Item):

                    ### 6.2 如果是Item数据, 爬虫中间件预处理,在交给管道
                    for spider_middlewares in self.spider_mids:
                        result = spider_middlewares.process_item(result)

                    # 得到请求的数据转到管道, 进行存储
                    # 框架完善--->多管道处理能力
                    for pipeline in self.pipelines:
                        result = pipeline.process_item(result)

                        # result -->接受在pipelins中处理完毕return的文件


                else:
                    raise Exception("Error: parse返回的数据不能被处理")




