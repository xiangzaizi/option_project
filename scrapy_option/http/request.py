# -*- coding:utf-8 -*-
"""封装Request对象"""


class Request(object):
    """框架内置请求对象, 设置请求信息"""
    def __init__(self, url, method='GET', headers=None, params=None, data=None,
                 parse='parse',
                 filter=True,
                 meta=None):
        self.url = url
        self.method = method
        self.headers = headers
        self.params = params
        self.data = data

        # parse处理多级页面
        self.parse = parse

        # 增量爬虫, 请求默认做去重filter = True
        self.filter = filter  # True默认做去重-->在那里判断？-->schedule

        self.meta = meta  # 请求发送的响应, 响应里面的数据, 请求里面的数据传给meta然后交给响应文件