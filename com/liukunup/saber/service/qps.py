# -*- coding: UTF-8 -*-
# 服务: 流控

import typing as t
import functools


class QPS:
    """ 鉴权注解类 """

    def __call__(self, func):
        """ 类装饰器 """
        self._func = func

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            print("-" * 100)
            print(func.__doc__)
            print("-" * 100)
            print(func.__name__)
            print("-" * 100)
            return func(*args, **kwargs)

        return decorator



