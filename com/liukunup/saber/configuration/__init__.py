# -*- coding: UTF-8 -*-
# 配置项

from com.liukunup.saber.configuration.config import *


# 按环境区分配置项
config = {
    # 环境标识: 开发/测试/灰度/生产/容器/UNIX
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "gray": GrayConfig,
    "production": ProductionConfig,
    "docker": DockerConfig,
    "unix": UnixConfig,
}
