# -*- coding: UTF-8 -*-
# API Result Wrapper

import typing as t

from com.liukunup.saber.bean import Code, Int, Float


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
