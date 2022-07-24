# -*- coding: UTF-8 -*-
# 支持的注解类
# 1. 操作审计 @audit
# 2. 接口鉴权 @required_perm, @required_admin
# 3. 签名校验 @required_sign

__all__ = ['audit', 'required_perm', 'required_admin', 'required_sign', 'rate_limiter']

from com.liukunup.saber.service.audit import AuditService
from com.liukunup.saber.service.authenticate import AuthenticateService
from com.liukunup.saber.service.signature import SignatureService
from com.liukunup.saber.service.token_bucket import TokenBucketService
from com.liukunup.saber.repository import Permission


def audit(func):
    """ 审计记录 """
    return AuditService()(func)


def required_perm(perm):
    """ 校验指定权限 """

    # 双层装饰器 看懂没,哈哈哈～
    def dual_layer_decorator(func):
        return AuthenticateService()(func, perm)

    return dual_layer_decorator


def required_admin(func):
    """ 校验超级管理员权限 """
    return required_perm(Permission.ADMIN)(func)


def required_sign(func):
    """ 校验接口签名 """
    return SignatureService()(func)


def rate_limiter(tokens=1):
    """ 流量控制 """
    # 双层装饰器
    def dual_layer_decorator(func):
        return TokenBucketService(rate=5, capacity=30)(func, tokens)
    return dual_layer_decorator
