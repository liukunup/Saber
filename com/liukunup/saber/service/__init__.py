# -*- coding: UTF-8 -*-
# 支持的注解类
# 1. 操作审计
# 2. 接口鉴权
# 3. 签名校验

__all__ = ['audit', 'auth', 'sign', 'qps']

from com.liukunup.saber.service.audit import Audit
from com.liukunup.saber.service.auth import Authentication
from com.liukunup.saber.service.sign import Signature
from com.liukunup.saber.service.qps import QPS

audit = Audit
auth = Authentication
sign = Signature
qps = QPS
