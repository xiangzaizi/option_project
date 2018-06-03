# -*- coding:utf-8 -*-
from scrapy_option.core.engine import Engine
from spider import BaiduSpider, DoubanSpider
if __name__ == '__main__':
    # 导入项目爬虫, 并创建对象
    # spider = BaiduSpider()

    # 豆瓣电影测试--1
    spider = DoubanSpider()

    # 将爬虫对象传入到engine中
    engine = Engine(spider)
    engine.start()
    """运行结果: 管道中打印的item对象
    框架基本功能测试OK
    ('item:', <scrapy_option.item.Item object at 0x7f39323d5690>)
    """

