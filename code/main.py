# -*- coding:utf-8 -*-
import time

from scrapy_option.core.engine import Engine

if __name__ == '__main__':
    # 1.并创建对象
    # spider = BaiduSpider()

    # 2.豆瓣电影测试--1
    # spider = DoubanSpider()

    # 3.将爬虫对象传入到engine中
    # engine = Engine(spider)
    # engine.start()
    """运行结果: 管道中打印的item对象
    框架基本功能测试OK
    ('item:', <scrapy_option.item.Item object at 0x7f39323d5690>)
    """
    # douban_spider = DoubanSpider()
    # baidu_spider = BaiduSpider()
    #
    # # 4. 处理多个爬虫  + 添加管道
    # spiders = {baidu_spider.name: baidu_spider, douban_spider.name: douban_spider}
    # pipelines = [BaiduPipeline, DoubanPipeline]

    # 项目完善之添加爬虫 下载中间件测试
    # spider_mids = [
    #     SpiderMiddlewares1,
    #     SpiderMiddlewares2
    # ]
    #
    # downloader_mids = [
    #     DownloaderMiddlewares1,
    #     DownloaderMiddlewares2
    # ]
    #
    # engine = Engine(spiders,
    #                 pipelines,
    #                 # 添加中间件到engine中完善框架
    #                 spider_mids,
    #                 downloader_mids)
    """以上注释内容全部添加到settings中, 通过settings控制组件的启用"""

    engine = Engine()
    while True:
        engine.start()
        time.sleep(5)



