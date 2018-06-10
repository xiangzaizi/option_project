# -*- coding:utf-8 -*-
"""创建可兼容py2_py3的队列"""
import six
from scrapy_option.utils.log import logger
from scrapy_option.conf.default_settings import *
# 方式一
# try:
#     from Queue import Queue # py2
# except ImportError:
#     from queue import Queue # py3

# 方式二
# 利six模块实现py2和py3的兼容
# 被移动的属性和模块six被加载得太迟了, 所以Pycharm无法引用解析
# from six.moves.queue import Queue

if ROLE is None:  # 非分布式, 使用python自己的队列
    from six.moves.queue import Queue
    from scrapy_option.set import NormalFilterSet as Set # 非分布式
elif ROLE in ["master", "slave"]:
    from scrapy_option.queue import Queue  # 导入配合redis写的queue.py
    from scrapy_option.set import RedisFilterSet as Set  # redis
else:
    raise Exception(u"不支持该模式{}".format(ROLE))


class Scheduler(object):
    def __init__(self):
        self.queue = Queue()
        # self._filter_set = set()  # 保存指纹, 目前是测试的url, 使用set()对请求的url进行去重
        self._filter_set = Set()    # 这些指纹就保存到redis中了可实现断点续传？
        self.total_request = 0  # 添加计数器, 与response相对应

    def add_request(self, request):
        # 进来先判断request.filter(True(去重) / False(不去重))
        """增量爬虫"""
        if not request.filter:  # False不做去重so(不用添加指纹, 不用对指纹去重)
            logger.info(u"添加请求（dont filter) 成功: [{}] <{}>".format(request.method, request.url))
            self.queue.put(request)

            # 只要put了请求了这里就自增1
            self.total_request += 1
            # return  # 到这里就结束不添加指纹, 不添加指纹

        # ***2.生成指纹(唯一性)
        fp = self._gen_fingerprint(request)

        # ***1. 对请求去重, 并添加不重复的请求到队列中
        if not self._filter_request(fp, request):
            logger.info(u"添加请求(not filter)成功:[{}]<{}>".format(request.method, request.url))
            self.queue.put(request)

            # put请求这里就自增1
            self.total_request += 1

            # add请求到队列中
            # self._filter_set.add(request.url)
            self._filter_set.add(fp)  # 通过指纹来去重

    def get_request(self):
        # 获取排队中的请求--->进入下载器下载
        try:
            return self.queue.get(False)
        except:
            return None

    def _filter_request(self, fp, request):
        # 判断是否是重复的请求, 如果是重复的返回True, 否则返回False
        # if request.url in self._filter_set:
        if fp in self._filter_set:
            logger.info(u"重复请求: [{}],<{}>".format(request.method, request.url))
            return True
        else:
            return False

    """请求指纹sha1值生成和去重处理"""
    def _gen_fingerprint(self, request):
        from hashlib import sha1
        import w3lib.url

        # 1. 获取请求进来的数据
        url = request.url
        method = request.method
        params = request.params
        data = request.data

        """对进来的参数进行处理"""
        # 1. url查询字符串规整
        url = w3lib.url.canonicalize_url(url)
        # 2. 请求方法字符串统一转为大写
        method = method.upper()

        # 3.处理params字符串, 因为update只仅仅接收字符串
        # 增加判断是否有提交的内容
        params = params if params is not None else {}
        params = str(sorted(params.items()))

        # 4. 处理data字符串
        data = data if data is not None else {}
        data = str(sorted(data.items()))

        # 构建一个sha1对象
        sha1 = sha1()

        # update() 必须接受一个非Unicode字符串
        # utf8_str方法, 1)过滤非Unicode的字符串 2）将Unicode的字符串转成utf-8的字符串
        sha1.update(self.utf8_str(url))
        sha1.update(self.utf8_str(method))
        sha1.update(self.utf8_str(params))
        sha1.update(self.utf8_str(data))

        # *** 生成16进制数的sha1的值
        fp = sha1.hexdigest()

        return fp

    def utf8_str(self, string):
        if six.PY2:
            if isinstance(string, str):
                return string
            else:
                return string.encode('utf-8')
        else:  # PY3的情况
            if isinstance(string, bytes):
                return string
            else:
                return string.encode('utf-8')