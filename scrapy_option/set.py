#coding:utf-8


from scrapy_option.conf.default_settings import *
import redis


class BaseFilterSet(object):  # 基础去重类
    def _add_fp(self, fp):  # 添加指纹
        pass

    def _is_filter(self, fp):  # 判断指纹--->去重
        pass


class NormalFilterSet(BaseFilterSet):  # 非分布式
    def __init__(self):
        self._filter_set = set()

    def add_fp(self, fp):
        self._filter_set.add(fp)

    def is_filter(self, fp):
        # if fp in self._filter_set:
        #     return True
        # else:
        #     return False
        return True if fp in self._filter_set else False


class RedisFilterSet(BaseFilterSet):  # redis分布式
    def __init__(self):
        self._filter_set = redis.Redis(
            host=REDIS_SET_HOST,
            port=REDIS_SET_PORT,
            db=REDIS_SET_DB
            )
        self._name = REDIS_SET_NAME

    def add_fp(self, fp):
        self._filter_set.sadd(self._name, fp)

    def is_filter(self, fp):
        return self._filter_set.sismember(self._name, fp)




