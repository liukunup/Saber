# -*- coding: UTF-8 -*-
# Custom Type

import typing as t

# 封装基础类型
Int = t.TypeVar("Int", bound=int)
Float = t.TypeVar("Float", bound=float)
