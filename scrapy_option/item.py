# -*- coding:utf-8 -*-
"""item对象"""


class Item(object):
    """框架内置Item对象"""
    def __init__(self, data):
        # data表示传入的数据
        self._data = data  # 设为简单的私有属性

    @property
    def data(self):
        # 对外提供data进行访问, 一定程度达到保护的作用
        return self._data
