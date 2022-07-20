# -*- coding: UTF-8 -*-
# 服务: 武器库

import typing as t
import functools


class Excalibur:
    """ 誓约胜利之剑 """

    def __init__(self, name: t.Text, desc: t.Text, owner: t.Optional[t.Text] = None, date: t.Optional[t.Text] = None):
        """
        初始化
        :param name:  用例名称
        :param desc:  用例描述
        :param owner: 编写人员
        :param date:  编写时间
        """
        self._name = name
        self._desc = desc
        self._owner = owner
        self._date = date

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



