# -*- coding: UTF-8 -*-
# 服务: 流控服务

import time
import functools

from com.liukunup.saber.bean import Int, Float


class TokenBucketService:
    """ 限流算法: 令牌桶服务 """

    def __init__(self, rate: Float, capacity: Int):
        """
        :param rate:     令牌生成速率（N unit per second）
        :param capacity: 桶容量
        """
        self.__rate = rate
        self.__capacity = capacity
        # 当前令牌总数
        self.__current_amount = 0
        # 上次消费时间
        self.__last_consume_time = int(time.time())

    def consume(self, token_num: Int = 1):
        """
        生产->消费
        :param token_num: 消费数量
        :return: 是否消费成功
        """
        # 计算从上次消费到这次消费,所需新发放的令牌数量
        increment = (int(time.time()) - self.__last_consume_time) * self.__rate
        # 总令牌数不能超过桶容量
        self.__current_amount = min(increment + self.__current_amount, self.__capacity)
        # 判断所需消费的令牌数是否足够
        if self.__current_amount < token_num:
            return False
        # 可消费才会记录消费时间并执行
        self.__last_consume_time = int(time.time())
        self.__current_amount -= token_num
        return True

    def __call__(self, func):
        """
        通过函数装饰器进行
        :param func: 函数
        :return: 装饰器对象
        """
        # 签名校验函数
        consume_func = self.consume

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            consume_func()
            return func(*args, **kwargs)

        return decorator
