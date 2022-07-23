# -*- coding: UTF-8 -*-
# 服务: 审计

import typing as t
import functools

from flask import request
from com.liukunup.saber.bean import Code, CustomException
from com.liukunup.saber.repository import User, Audit
from com.liukunup.saber import db


class AuditService:
    """ 审计 """

    def __call__(self, func):
        """
        通过函数装饰器进行签名校验
        :param func: 函数
        :return: 装饰器对象
        """
        # 签名校验函数
        audit_func = self.record

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            audit_func(func.__name__, *args, **kwargs)
            return func(*args, **kwargs)

        return decorator

    @staticmethod
    def record(event: t.Text, *args, **kwargs):
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

        # 插入审计日志
        audit = Audit(user=user, event=event, args=dict(args=args, kwargs=kwargs))
        db.session.add(audit)
        db.session.commit()
