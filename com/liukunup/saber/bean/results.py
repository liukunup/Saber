# -*- coding: UTF-8 -*-
# API Result Wrapper

import typing as t

from enum import Enum, unique

# 封装系统内置的基础类型
Int = t.TypeVar("Int", bound=int)
Float = t.TypeVar("Float", bound=float)


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
    OBJECT_NOT_EXIST = RetCode("无法找到这样的对象", 10003)
    # 请求类
    REQUEST_EXPIRE = RetCode("请求已过期", 10011)
    REQUEST_DIFF_SIGN = RetCode("签名值不一致", 10012)
    REQUEST_NO_PERM = RetCode("不具备相关权限", 10013)
    # 其他类
    ADMIN_EXIST = RetCode("超级管理员已存在", 100099)


class ApiResult(object):
    """ 接口响应返回封装 """

    def __init__(self, message: t.Optional[t.Text] = None, code: t.Optional[Int] = None,
                 e_code: t.Optional[Code] = None, payload: t.Any = None, latency: t.Optional[Float] = None):
        """
        :param message: 响应消息
        :param code:    响应码
        :param e_code:  响应码(枚举类型)
        :param payload: 响应数据
        :param latency: 响应时间
        """
        # 直接设置 message+code
        self.message = message
        self.code = code
        # (高优先级) 通过枚举类型设置 message+code
        if e_code:
            self.message = e_code.value.message
            self.code = e_code.value.code
        # 数据+耗时
        self.payload = payload
        self.latency = latency

    def json(self):
        """
        返回字典格式的响应对象
        :return 响应结果
        """
        response = {
            "code": self.code,
            "message": self.message,
        }
        if self.payload:
            response.update({"data": self.payload})
        if self.payload:
            response.update({"latency": self.latency})
        return response


class Success(ApiResult):
    """ 默认响应类型: 成功 """

    def __init__(self, payload: t.Any = None, latency: t.Optional[Float] = None):
        """
        成功
        :param payload: 响应数据
        :param latency: 响应时间
        """
        super().__init__(e_code=Code.SUCCESS, payload=payload, latency=latency)


class Failed(ApiResult):
    """ 默认响应类型: 失败 """

    def __init__(self, payload: t.Any = None, latency: t.Optional[Float] = None):
        """
        失败
        :param payload: 响应数据
        :param latency: 响应时间
        """
        super().__init__(e_code=Code.FAILED, payload=payload, latency=latency)


class CustomException(ApiResult, Exception):
    """ 默认响应类型: 自定义异常 """

    def __init__(self, e_code: Code, payload: t.Any = None, latency: t.Optional[Float] = None):
        """
        自定义异常
        :param e_code:  响应码(枚举类型)
        :param payload: 响应数据
        :param latency: 响应时间
        """
        super().__init__(e_code=e_code, payload=payload, latency=latency)
