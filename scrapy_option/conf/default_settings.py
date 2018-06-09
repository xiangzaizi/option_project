# -*- coding:utf-8 -*-
"""框架中默认配置文件"""
import logging


# 抽取日志文件中的默认配置信息
# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = 'log.log'    # 默认日志文件名称


# 使用项目中的配置文件, 修改默认配置文件内容
from code.settings import *
"""
1. 此处位置不用管settings爆红, 在项目导入框架时sys.path会沿着项目settings找有就会以项目配置文件配置内容运行
2. 没有就会按照框架内部配置的文件调试
3. from code.settings import  *--->因为code项目文件夹仅是测试文件夹可以随时换,框架内不宜放变化的参数
4. import sys  print(sys.path)--->查看当前项目运行时导包的顺序验证3
"""

