# -*- coding: UTF-8 -*-
# Bean

__all__ = ['ApiResult', 'Success', 'Failed', 'CustomException', 'Code', 'Int', 'Float']

import typing as t

from com.liukunup.saber.bean.api_result import ApiResult, Success, Failed, CustomException
from com.liukunup.saber.bean.ret_code import Code

# 封装基础类型
Int = t.TypeVar("Int", bound=int)
Float = t.TypeVar("Float", bound=float)
