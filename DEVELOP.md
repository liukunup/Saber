# Saber 测试开发双向框架 开发指南

## 开发环境配置

1. 虚拟环境

```shell
# 切换到此目录
cd Saber
# 创建虚拟环境
python3 -m venv venv
# 激活虚拟环境
. venv/bin/activate
# 更新pip工具
venv/bin/python3 -m pip install --upgrade pip
# 安装依赖库 (按需选择哟)
venv/bin/pip3 install -r requirements/1_development.txt
```

## 环境变量设置

在当前项目目录下新建`.env`文档,配置以下环境变量

```dotenv
# FLASK框架配置
FLASK_APP=main.py
FLASK_ENV=development
FLASK_CONFIG=development
# 设置超级管理员
SUPER_ADMIN=Administrator
# 数据库配置
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USERNAME=root
MYSQL_PASSWORD=123456
MYSQL_DATABASE=db
# 数据库管理密码
MYSQL_ROOT_PASSWORD=123456
# 数据库版本
MYSQL_VERSION=5.7
```

## 数据库迁移

首次使用时需要先新建数据库

```shell
# 数据库初始化
flask db init
# 数据库迁移
flask db migrate -m 'Init'
# 部署数据
flask deploy
# 启动服务
flask run
```














## 安装部署

### 镜像构建

```shell
docker build -t liukunup/flaskr:v1.0.0 -f Dockerfile .
```

## FAQ

- 5000端口被占用

```text
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> Sharing.
```

解决方案一（推荐）

查找哪个程序在占用当前端口，然后杀掉对应的进程即可。

```shell
lsof -i :5000
kill -5 pid
```

解决方案二

启动时设置Port参数，使用其他端口。

```shell
flask run --port=8080
```
