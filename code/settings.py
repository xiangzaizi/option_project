# -*- coding:utf-8 -*-


# 修改默认配置文件名, 使用时间项目名记录日志信息
DEFAULT_LOG_FILENAME = 'baidu.log'

# 1. 多个爬虫
SPIDERS = [
    # "spiders.baidu.BaiduSpider",
    "spiders.douban.DoubanSpider",
]

# 2. 自定义的管道
PIPELINES = [
    "pipelines.BaiduPipeline",
    "pipelines.DoubanPipeline",
]

# 3. 项目添加自定义爬虫  下载中间件
SPIDER_MIDDLEWARES = [
    # "spider_middlewares.SpiderMiddlewares1",
    # "spider_middlewares.SpiderMiddlewares2",
]

DOWNLOADER_MIDDLEWARES = [
    # "downloader_middlewares.DownloaderMiddlewares1",
    # "downloader_middlewares.DownloaderMiddlewares2"
]

# 设置并发量
ASNYC_MAX_COUNT = 5

# 提供可选择的多任务
ASYNC_TYPE = 'thread'
# ASYNC_TYPE = 'coroutine'

# 配置redis服务器, 在queue中直接导入default_settings
REDIS_QUEUE_NAME = 'request_queue'
REDIS_QUEUE_HOST = 'localhost'
REDIS_QUEUE_PORT = 6379
REDIS_QUEUE_DB = 7

# 分布式
ROLE = None
# 使用了任何一个，都表示分布式模式
# 代码分布: 主机端, 客户端, 放在不同的端, 启用不同的角色配置
# ROLE = "master"
# ROLE = "slave"
