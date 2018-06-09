# -*- coding:utf-8 -*-
"""引擎组件
1. 对外提供整个程序的入口
2. 依次调用其他组件对外提供的接口, 实现整个框架的运作
"""
import time
# 1. 导入请求响应
from scrapy_option.http.request import Request
from scrapy_option.http.response import Response

# 2. 导入核心组件
from .scheduler import Scheduler
from .downloader import Downloader
from scrapy_option.item import Item


# 4. 在引擎中导入日志文件
from scrapy_option.utils.log import logger
from datetime import datetime

# 5. 导入default_setting文件
from scrapy_option.conf.default_settings import *

# # 6. 导入线程, 创建线程池, 用法和进程相同
# from multiprocessing.dummy import Pool
#
# # 7. 导入协程的Pool, 导入重写后的协程就可以直接使用原有的线程池不需要在修改代码
# from scrapy_option.async.coroutine import Pool

# 8. 提供可选的多任务优化 线程 or 协成
if ASYNC_TYPE == "coroutine":
    from scrapy_plus.async.coroutine import Pool
    logger.info(u"正在启用协程异步模式")
elif ASYNC_TYPE == "thread":
    from multiprocessing.dummy import Pool
    logger.info(u"正在启用多线程异步模式")

else:
    raise Exception(u"不支持该异步类型")


class Engine(object):
    def __init__(self):
        # 创建初始化对象
        # 接收实际项目spider,
        self.spiders = self._auto_import_module_cls(SPIDERS, True)

        self.scheduler = Scheduler()
        self.downloader = Downloader()
        # self.pipeline = Pipeline()
        # 完善框架处理多管道能力
        self.pipelines = self._auto_import_module_cls(PIPELINES)


        # 初始化中间件文件
        # self.spider_middlewares = SpiderMiddlewares()
        # self.downloader_middlewares = DownloaderMiddlewares()

        # 框架完善处理项目重写的爬虫 下载中间件
        self.spider_mids = self._auto_import_module_cls(SPIDER_MIDDLEWARES)
        self.downloader_mids = self._auto_import_module_cls(DOWNLOADER_MIDDLEWARES)

        # 创建线程池对象
        self.pool = Pool()  # 请求在那里就在那里使用, 写两个方法 异步处理

        # 添加计数器
        self.total_response = 0  # 添加响应的计数器

        # 设置主线程的运行状态, 主线程是否在执行?
        self.is_running = True


    def _auto_import_module_cls(self, paths=[], isspider=False):
        import importlib
        if isspider:
            result = {}  # 如果是爬虫, 返回给__init__(self)的就是字典
        else:
            result = []  # 如果不是爬虫, 返回给__init__的就是列表

        for path in paths:
            module_name = path[:path.rfind(".")]
            ret = importlib.import_module(module_name)

            cls_name = path[path.rfind(".")+1:]

            cls = getattr(ret, cls_name)  # 根据绝对路径,返回指定文件里的指定类名的类对象

            if isspider:
                result[cls.name] = cls()
            else:
                result.append(cls())

        return result
    """关于这个方法先在setting中添加配置文件,然后在编写_auto_import_moudule_cls的方法进行测试
    1. 将main中的配置信息提取到settings中
    2. 优化engine, 通过_auto_import_moudule_cls获取项目配置的管道 中间件信息
    """

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

    def _callback(self, _): # 这个的callback必须传一个参数,但是这里不用，none所以传一个下划线
        if self.is_running == True:
            self.pool.apply_async(self._excute_request_response_item, callback=self._callback)  # 一个递归的过程

    def _start_engine(self):
        # 处理请求
        # self._start_requests()  # --->发送请求

        """__*** 异步非阻塞写法发送请求***__"""
        self.pool.apply_async(self._start_requests)


        # 处理调度器的请求
        # while True:
            # ---->执行请求 但并发的数量不能控制
            # self.pool.apply_async(self._excute_request_response_item())

        # 如何控制并发的次数？
        for i in range(ASNYC_MAX_COUNT):
            logger.info(u'子线程正在执行...')
            self.pool.apply_async(self._excute_request_response_item, callback=self._callback)

        while True:
            # 优化while True等待, 当网络响应慢的时候, 一个响应需要2秒, 那CPU就处在空转中
            # 通过测试这样优化后可以减轻cpu负担
            time.sleep(0.001)

            if self.total_response == self.scheduler.total_request and self.total_response != 0:
                self.is_running = False
                # total_response != 0 因为初始值是0, 程序没有开始就结束所以去除
                # 当请求数==响应数时断开
                break
        self.pool.close()  # 不在向线程池中添加任务了
        self.pool.join()  # 让主线程等待所有子线程执行结束

        logger.info(u"主线程执行结束")

    """处理多爬虫, 对_start_engine方法进行重构"""
    def _start_requests(self):
        for spider_name, spider in self.spiders.items():
            # 1.获取spider中的url请求list
            start_request_list = spider.start_requests()

            for start_request in start_request_list:  # 处理spider发送的多个请求
                start_request.spider_name = spider.name

                ### 1.1请求经过爬虫中间件
                for spider_middleware in self.spider_mids:
                    start_request = spider_middleware.process_request(start_request)
                # 2. 请求入调度器
                self.scheduler.add_request(start_request)

    def _excute_request_response_item(self):
        # 执行请求   响应   items数据

        # 3. 获取调度器中的请求对象, 这样就是scheduler中过滤之后的请求
        request = self.scheduler.get_request()
        # 注意: add请求, put请求
        # 请求结束时-->所以设定scheduler中的队列get(False)-->表示添加的url请求完, 返回响应None


        # 当队列中的请求为空的时候, 退出程序
        if request is None:
            # break
            return   # 没有请求函数进来, 程序退出

        ### 3.1 将请求经过下载中间件预处理--->请求
        for downloader_middleware in self.downloader_mids:
            request = downloader_middleware.process_request(request)

        # 4. 将请求交个下载器
        response = self.downloader.get_response(request)

        ### 4.1 将响应经过下载中间件预处理--->响应
        for downloader_middleware in self.downloader_mids:
            response = downloader_middleware.process_response(response)

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
                for spider_middleware in self.spider_mids:
                    result = spider_middleware.process_request(result)

                # 是请求继续入队列请求数据
                self.scheduler.add_request(result)

            elif isinstance(result, Item):

                ### 6.2 如果是Item数据, 爬虫中间件预处理,在交给管道
                for spider_middleware in self.spider_mids:
                    result = spider_middleware.process_item(result)

                # 得到请求的数据转到管道, 进行存储
                # 框架完善--->多管道处理能力
                for pipeline in self.pipelines:
                    result = pipeline.process_item(result, spider)

                    # result -->接受在pipelins中处理完毕return的文件


            else:
                raise Exception("Error: parse返回的数据不能被处理")

        # 不管当前有几个线程, 只要有一个线程提取完响应后就+1
        self.total_response += 1
        # 这里的响应--->对应调度器发完请求进行同样的+1计数





