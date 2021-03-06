# -*- coding:utf-8 -*-
"""对下载组件进行封装"""

from scrapy_option.http.response import Response
import requests
from scrapy_option.utils.log import logger


class Downloader(object):

    def get_response(self, request):
        # 1. 根据请求的对象, 发起请求

        if request.method.upper() == "GET":
            res = requests.get(
                request.url,
                # request.meta,
                headers=request.headers,
                params=request.params
            )
        elif request.method.upper() == "POST":
            res = request.post(
                request.url,
                # request.meta,
                headers=request.headers,
                params=request.params,
                data=request.data  # 对应post请求提交进来时的数据
            )
        else:
            raise Exception("Error: 不支持该请求的方法")

        # 获取到响应
        logger.info(u"[{}] <{}>".format(res.status_code, res.url))

        # 2. 构建响应的对象, 并返回
        return Response(
            res.url,
            res.status_code,
            res.headers,
            res.content,
            # res.meta
        )


