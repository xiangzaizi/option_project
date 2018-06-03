# -*- coding:utf-8 -*-
from scrapy_option.core.engine import Engine

if __name__ == '__main__':
    engine = Engine()
    engine.start()
    """运行结果: 管道中打印的item对象
    框架基本功能测试OK
    ('item:', <scrapy_option.item.Item object at 0x7f39323d5690>)
    """

