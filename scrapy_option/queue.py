# coding:utf-8
"""为了重复使用schedule中队列的put和get减少代码的修改量
lpush存   rpop 取
queue.py---->实现了所有队列的方法，但是是用来和redis操作
"""
from scrapy_option.conf.default_settings import *
import time
import pickle
import redis
from six.moves import queue as BaseQueue

# 利用redis实现一个Queue，使其接口同python的内置队列接口一致
# 可以实现无缝转换


class Queue(object):
    """
    A Queue like message built over redis
    """

    Empty = BaseQueue.Empty
    Full = BaseQueue.Full
    max_timeout = 0.3  # 超时时间

    def __init__(self, maxsize=0, name=REDIS_QUEUE_NAME, host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT, db=REDIS_QUEUE_DB,
                lazy_limit=True):  # , password=None redis没有密码删除此处位置密码
        """
        Constructor for RedisQueue
        maxsize:    an integer that sets the upperbound limit on the number of
                    items that can be placed in the queue.
        lazy_limit: redis queue is shared via instance, a lazy size limit is used
                    for better performance.
        """
        self.name = name
        self.redis = redis.StrictRedis(host=host, port=port, db=db)
        self.maxsize = maxsize  # 最大的保存的数值
        self.lazy_limit = lazy_limit
        self.last_qsize = 0

    def qsize(self):
        self.last_qsize = self.redis.llen(self.name)
        return self.last_qsize

    def empty(self):
        if self.qsize() == 0:
            return True
        else:
            return False

    def full(self):
        if self.maxsize and self.qsize() >= self.maxsize:
            return True
        else:
            return False

    def put_nowait(self, obj):
        if self.lazy_limit and self.last_qsize < self.maxsize:
            pass
        elif self.full():
            raise self.Full
        self.last_qsize = self.redis.rpush(self.name, pickle.dumps(obj))
        return True

    def put(self, obj, block=True, timeout=None):
        if not block:
            return self.put_nowait(obj)

        start_time = time.time()
        while True:
            try:
                return self.put_nowait(obj)
            except self.Full:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)

    def get_nowait(self):
        ret = self.redis.lpop(self.name)
        if ret is None:
            raise self.Empty
        return pickle.loads(ret)

    def get(self, block=True, timeout=None):
        if not block:
            return self.get_nowait()

        start_time = time.time()
        while True:
            try:
                return self.get_nowait()
            except self.Empty:
                if timeout:
                    lasted = time.time() - start_time
                    if timeout > lasted:
                        time.sleep(min(self.max_timeout, timeout - lasted))
                    else:
                        raise
                else:
                    time.sleep(self.max_timeout)
