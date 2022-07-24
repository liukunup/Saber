# -*- coding: UTF-8 -*-
# 服务: 对象存储
# see http://docs.minio.org.cn/docs/master/python-client-api-reference

import typing as t

from minio import Minio
from .progress import Progress


class MinioService(object):
    """ 对象存储 """

    # 客户端实例
    __client = None

    def __init__(self, endpoint: t.Text, access_key: t.Text, secret_key: t.Text):
        # 初始化客户端
        self.__client = Minio(endpoint, access_key=access_key, secret_key=secret_key)

    def push(self, filename: t.Text, bucket: t.Text, obj: t.Text):
        """ 上传 """
        assert self.__client is not None
        self.__client.fput_object(bucket, obj, filename, progress=Progress())

    def pull(self, bucket: t.Text, obj: t.Text, filename: t.Text):
        """ 下载 """
        assert self.__client is not None
        self.__client.fget_object(bucket, obj, filename)

    def remove(self, bucket: t.Text, obj: t.Text):
        """ 删除 """
        assert self.__client is not None
        self.__client.remove_object(bucket, obj)

    def list(self, bucket: t.Text, prefix: t.Text, recursive: bool = True):
        """ 列举 """
        assert self.__client is not None
        return self.__client.list_objects(bucket, prefix=prefix, recursive=recursive)

    def exists(self, bucket: t.Text):
        """ 判断桶是否存在 """
        assert self.__client is not None
        return self.__client.bucket_exists(bucket)

    def create(self, bucket: t.Text):
        """ 创建桶 """
        assert self.__client is not None
        self.__client.make_bucket(bucket)

    def destroy(self, bucket: t.Text):
        """ 销毁桶 """
        assert self.__client is not None
        self.__client.remove_bucket(bucket)
