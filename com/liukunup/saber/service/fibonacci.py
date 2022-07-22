# -*- coding: UTF-8 -*-
# 服务: 求斐波那契数列前N项


class Fibonacci(object):
    """ 斐波那契数列迭代器 """

    def __init__(self, n: int):
        """
        :param n:int 生成数列的个数
        """
        self.n = n
        self.current, self.a, self.b = 0, 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.n:
            self.a, self.b = self.b, self.a + self.b
            self.current += 1
            return self.a
        raise StopIteration()
