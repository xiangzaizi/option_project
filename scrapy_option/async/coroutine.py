# -*- coding:utf-8 -*-
"""面向对象的最好的解释
1. 需要的时候就继承父类
2. 不需要就pass
3. 共有方法apply_async方法的复用 协程 线程
"""
from gevent.pool import Pool as BasePool
from gevent.monkey import patch_all
patch_all()  # 当遇到IO 阻塞自动切换－－>monkey

# path_all将python底层的网络库改为异步的库
# scoket，当遇到网络IO阻塞的时候,会自动切换协程执行

# 协程池重写


class Pool(BasePool):
    """继承gevent的Pool"""
    def apply_async(self, func, args=None,kwds=None, callback=None):
        # 当程序调用apply_async方法时, 默认返回父类的apply_async方法处理
        return BasePool().apply_async(func=func, args=args, kwds=kwds, callback=callback)

        # Python3 可以用super() 来表示父类, py2不支持super()
        # return super().apply_async(func = func, args = args, kwds = kwds, callback = callback)

    def close(self):
        # 当程序调用close方法自动略过, 这样就避免了与多线程中close方法起冲突了
        # 在选择使用协程的时候碰到close方法就会略过了
        pass



