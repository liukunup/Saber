# -*- coding: UTF-8 -*-
# 服务: 鉴权

import functools

from flask import request
from com.liukunup.saber.bean import Code, CustomException
from com.liukunup.saber.repository import User
from com.liukunup.saber import db


class Authentication:
    """ 鉴权注解类 """

    def __init__(self, perm):
        self.permission = perm

    def __call__(self, func):
        """
        通过函数装饰器进行签名校验
        :param func: 函数
        :return: 装饰器对象
        """
        # 签名校验函数
        verify_func = self.permission_verify
        perm_arg = self.permission

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            verify_func(perm_arg)
            return func(*args, **kwargs)

        return decorator

    @staticmethod
    def permission_verify(perm):
        """
        权限验证
        当权限验证失败时,将通过异常抛出
        :param perm: 待验证的权限枚举值
        :return: 不涉及
        """
        # 获取请求头字典
        headers = dict(request.headers)

        # 检查 公钥 参数是否合法
        if "X-Access-Key" not in headers or headers["X-Access-Key"] is None or len(headers["X-Access-Key"]) != 32:
            raise CustomException(e_code=Code.INVALID_PARAM,
                                  payload="[X-Access-Key 配置错误] 格式: 1.定长32个字符; 2.已配置在数据库中.")
        # 检查 公钥 是否存在
        access_key = headers["X-Access-Key"]
        user = db.session.query(User).filter(User.access_key == access_key).first()
        if user is None:
            raise CustomException(e_code=Code.OBJECT_NOT_EXIST,
                                  payload="[X-Access-Key 不存在] 未找到对应的User对象.")

        # 检查 权限 是否允许
        if not user.can(perm):
            raise CustomException(e_code=Code.REQUEST_NO_PREM, payload=f"您的请求需要 {perm} 权限.")
