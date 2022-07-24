# -*- coding: UTF-8 -*-
# 支持的注解类
# 1. 操作审计
# 2. 接口鉴权
# 3. 签名校验

__all__ = ['audit', 'auth', 'sign', 'qps']

from com.liukunup.saber.service.audit import AuditService
from com.liukunup.saber.service.auth import AuthenticateService
from com.liukunup.saber.service.sign import SignatureService
from com.liukunup.saber.service.qps import TokenBucketService

audit = AuditService
auth = AuthenticateService
sign = SignatureService
qps = TokenBucketService
