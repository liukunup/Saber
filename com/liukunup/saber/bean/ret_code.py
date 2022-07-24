# -*- coding: UTF-8 -*-
# Return Code List

import typing as t

from com.liukunup.saber.bean.custom_type import Int
from enum import Enum, unique


@unique
class Code(Enum):

    class RetCode:
        """ 类的内部类: 响应返回码 """

        def __init__(self, message: t.Text, code: Int):
            """
            :param message: 响应消息
            :param code:    响应码
            """
            self._message = message
            self._code = code

        @property
        def message(self):
            return self._message

        @property
        def code(self):
            return self._code

    """ 返回码列表 """
    # 默认返回码
    FAILED = RetCode("failed", -1)
    SUCCESS = RetCode("success", 200)
    UNKNOWN = RetCode("unknown", 10000)
    # 参数异常类
    INVALID_PARAM = RetCode("无效或非法参数", 10001)
    INVALID_TIMESTAMP = RetCode("无效时间戳", 10002)
    NO_SUCH_OBJECT = RetCode("无法找到这样的对象", 10003)
    # 请求类
    REQUEST_EXPIRE = RetCode("请求已过期", 10011)
    REQUEST_DIFF_SIGN = RetCode("签名值不一致", 10012)
    REQUEST_NO_PERM = RetCode("不具备相关权限", 10013)
