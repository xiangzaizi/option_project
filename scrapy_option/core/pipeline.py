# -*- coding:utf-8 -*-
"""对管道组件的封装"""


class Pipeline(object):
    # 处理数据对象(Item)

    def process_item(self, item):
        # 处理item对象, 接受数据对象作为参数
        print ("item:", item)
