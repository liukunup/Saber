# -*- coding: UTF-8 -*-
# 服务: 签名

import datetime
import functools
import hashlib
import hmac
import typing as t

from flask import request
from com.liukunup.saber.bean import Code, CustomException
from com.liukunup.saber.repository import User
from com.liukunup.saber import db


class SignatureService:
    """ 签名校验 """

    # 分钟级过期时间
    expire_in_minute = 10

    def __call__(self, func):
        """
        通过函数装饰器进行签名校验
        :param func: 函数
        :return: 装饰器对象
        """
        # 签名校验函数
        verify_func = self.signature_verify

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            verify_func()
            return func(*args, **kwargs)

        return decorator

    def signature_verify(self):
        """
        签名验证
        当签名验证失败时,将通过异常抛出
        :return: 不涉及
        """
        # 请求头
        headers = dict(request.headers)

        # 检查 时间戳 参数是否合法
        if "X-Timestamp" not in headers or headers["X-Timestamp"] is None:
            raise CustomException(e_code=Code.INVALID_PARAM,
                                  payload="[X-Timestamp 配置错误] 格式: 1.毫秒时间戳; 2.与服务器保持时区一致.")
        # 验证时间戳是否有效
        if not self.timestamp_check(timestamp=headers["X-Timestamp"]):
            raise CustomException(e_code=Code.REQUEST_EXPIRE,
                                  payload=f"[X-Timestamp 已过期] 请求有效期: 服务器时间前后{self.expire_in_minute}分钟内.")

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

        # 检查 签名 参数是否合法
        if "X-Signature" not in headers or headers["X-Signature"] is None:
            raise CustomException(e_code=Code.INVALID_PARAM,
                                  payload="[X-Signature 配置错误] 签名方法请参考 README.md 文档.")
        # 服务端计算签名值
        local_signature = self.signature_calculate(user.access_key, user.secret_key,
                                                   dict(request.args),
                                                   dict(request.headers),
                                                   request.data)
        # 校验签名是否一致
        signature = headers["X-Signature"]
        if signature != local_signature:
            raise CustomException(e_code=Code.REQUEST_DIFF_SIGN, payload=f"服务端签名值: {local_signature}")

    @staticmethod
    def signature_calculate(access_key: t.Text, secret_key: t.Text, params: t.Optional[t.Dict] = None,
                            headers: t.Optional[t.Dict] = None, body: t.Union[t.ByteString, t.Text, t.Dict] = None):
        """
        签名计算
        请参考 README.md 文档
        :param access_key: 公钥
        :param secret_key: 私钥
        :param params:     路径参数
        :param headers:    请求头参数
        :param body:       请求体内容
        :return: 签名值
        """
        # 待计算签名值的字段值列表
        content_list = list()
        # 路径参数
        if isinstance(params, dict):
            content_list.extend([str(dat[1]) for dat in sorted(params.items(), key=lambda kv: kv[0])])
        # 请求头参数
        if not isinstance(headers, dict) or "X-Keys" not in headers or not isinstance(headers["X-Keys"], str) \
                or len(headers["X-Keys"]) <= 0:
            raise CustomException(e_code=Code.INVALID_PARAM, payload="[X-Keys 配置错误] 签名计算请参考 README.md 文档")
        for key in headers["X-Keys"].split(","):
            content_list.append(str(headers[key]))
        # 请求体内容
        if isinstance(body, bytes) and len(body) > 0:
            content_list.append(body.decode(encoding="utf-8"))
        if isinstance(body, str) and len(body) > 0:
            content_list.append(body)
        # 公钥
        content_list.append(access_key)
        # 连接成字符串
        content = ";".join(content_list)
        return hmac.new(bytes(secret_key, encoding="utf-8"), bytes(content, encoding="utf-8"),
                        digestmod=hashlib.sha256).hexdigest().lower()

    def timestamp_check(self, timestamp: t.Union[int, float]):
        """
        验证时间戳是否在有效期内
        :param timestamp: 待验证的毫秒时间戳
        :return: 是否在有效期内
        """
        try:
            # 待验证的目标时间戳
            target = datetime.datetime.fromtimestamp(int(timestamp) / 1000)
            # 当前服务器时间
            now = datetime.datetime.now()
            # 计算有效期
            start = now - datetime.timedelta(minutes=self.expire_in_minute)
            end = now + datetime.timedelta(minutes=self.expire_in_minute)
            # 判定是否在有效期内
            return start <= target <= end
        except Exception as _:
            raise CustomException(e_code=Code.INVALID_PARAM, payload="[X-Timestamp 配置错误] 签名计算请参考 README.md 文档")
