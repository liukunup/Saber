# -*- coding: UTF-8 -*-
# 配置: 区分环境配置

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class AbstractConfig:
    """ 抽象配置基类 """

    # USE_TALISMAN
    USE_TALISMAN = False
    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    # The Super Administrator
    SUPER_ADMIN = os.environ.get("SUPER_ADMIN")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(AbstractConfig):
    """ 开发环境 """

    # 日志等级设置到DEBUG
    DEBUG = True
    # 回显SQL语句
    SQLALCHEMY_ECHO = True
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEV_DATABASE_URL") or \
        "sqlite:///" + os.path.join(basedir, "saber-dev.sqlite")
    # MinIO
    MINIO_USERNAME = None
    MINIO_PASSWORD = None
    MINIO_BUCKET = None


class TestingConfig(AbstractConfig):
    """ 测试环境 """

    # 测试标识
    TESTING = True
    # 数据库参数
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "saber-testing"
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/" \
                              f"{MYSQL_DATABASE}"
    # MinIO
    MINIO_USERNAME = os.environ.get("MINIO_USERNAME") or "username"
    MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD") or "password"
    MINIO_BUCKET = os.environ.get("MINIO_BUCKET") or "bucket-testing"


class GrayConfig(AbstractConfig):
    """ 灰度环境 """

    # 数据库参数
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "saber-gray"
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/" \
                              f"{MYSQL_DATABASE}"
    # MinIO
    MINIO_USERNAME = os.environ.get("MINIO_USERNAME") or "username"
    MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD") or "password"
    MINIO_BUCKET = os.environ.get("MINIO_BUCKET") or "bucket-gray"


class ProductionConfig(AbstractConfig):
    """ 生产环境 """

    # 数据库参数
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "127.0.0.1"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
    MYSQL_USERNAME = os.environ.get("MYSQL_USERNAME") or "root"
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "123456"
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "saber-prod"
    # 数据库链接
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/" \
                              f"{MYSQL_DATABASE}"
    # MinIO
    MINIO_USERNAME = os.environ.get("MINIO_USERNAME") or "username"
    MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD") or "password"
    MINIO_BUCKET = os.environ.get("MINIO_BUCKET") or "bucket-prod"


class DockerConfig(ProductionConfig):
    """
    Docker 生产环境
    """
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to stderr
        import logging
        from logging import StreamHandler
        stream_handler = StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


class UnixConfig(ProductionConfig):
    """
    Unix 生产环境
    """
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.INFO)
        app.logger.addHandler(syslog_handler)
