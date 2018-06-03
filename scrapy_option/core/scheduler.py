# -*- coding:utf-8 -*-
"""创建可兼容py2_py3的队列"""

# 方式一
try:
    from Queue import Queue # py2
except ImportError:
    from queue import Queue # py3

# 方式二
# 利six模块实现py2和py3的兼容
# 被移动的属性和模块six被加载得太迟了, 所以Pycharm无法引用解析
# from six.moves.queue import Queue


class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        self._filter_set = set()  # 保存指纹, 目前是测试的url, 使用set()对请求的url进行去重

    def add_request(self, request):
        # 对请求去重, 并添加不重复的请求到队列中
        if not self._filter_request(request):
            self.queue.put(request)
            # add请求到队列中
            self._filter_set.add(request.url)

    def get_request(self):
        # 获取排队中的请求--->进入下载器下载
        try:
            return self.queue.get(False)
        except:
            return None

    def _filter_request(self, request):
        # 判断是否是重复的请求, 如果是重复的返回True, 否则返回False
        if request.url in self._filter_set:
            return True
        else:
            return False
