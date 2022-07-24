# Saber 测试开发双向框架 开发指南

作为测试框架时,支持服务;

作为开发框架时,支持测试;

![AC](images/saber.jpeg)

---

## 开发环境配置

代码下载

```shell
git clone https://github.com/liukunup/Saber.git
```

### 环境配置(2选1)

1. 虚拟环境

```shell
# 切换到此目录
cd Saber
# 创建环境
python3 -m venv venv
# 激活环境
. venv/bin/activate
# 更新pip工具
venv/bin/python3 -m pip install --upgrade pip
# 安装依赖库 (按需选择哟)
venv/bin/pip3 install -r requirements/1_development.txt
```

2. Miniconda or Anaconda

```shell
# 切换到此目录
cd Saber
# 创建环境
conda create -n saber python=3.9
# 激活环境
conda activate saber
# 安装依赖库 (按需选择哟)
conda install -r requirements/1_development.txt
```

### 环境变量

在当前项目(即Saber)目录下新建`.env`文档, 配置以下环境变量

```dotenv
# Flask
FLASK_APP=com.liukunup.saber.application.py
FLASK_CONFIG=development
# Administrator
SUPER_ADMIN=Administrator
# MySQL
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USERNAME=username
MYSQL_PASSWORD=password
MYSQL_DATABASE=saber
# MinIO
MINIO_USERNAME=username
MINIO_PASSWORD=password
MINIO_BUCKET=saber
```

### 数据迁移

首次使用前, 需要先进行数据迁移

如果是开发环境, 使用sqlite数据库情况, 直接执行以下命令即可;

如果是其他环境, 使用mysql数据库情况, 请先创建数据库;

执行迁移 or 执行部署 2选1即可, 建议是执行部署。

```shell
# 初始化配置
flask db init
# 生成迁移脚本
flask db migrate -m 'Init'
# 执行迁移(仅升级)
flask db upgrade
# 执行部署(升级+导入数据)
flask deploy
# 启动服务
flask run
```

---

## 安装部署

### 镜像构建

建议使用三段式版本号,即 v`大版本`.`小版本`.`补丁版本`

```shell
docker build -f docker/Dockerfile -t liukunup/saber:v1.0.0 .
```

Tips: 注意别漏掉最后的点号

### Docker方式部署

```shell
docker run -d \
    -p 5000:5000 \
    -e MYSQL_HOST=127.0.0.1 \
    -e MYSQL_PORT=3306 \
    -e MYSQL_USERNAME=username \
    -e MYSQL_PASSWORD=password \
    -e MYSQL_DATABASE=saber \
    -e MINIO_USERNAME=username \
    -e MINIO_PASSWORD=password \
    -e MINIO_BUCKET=saber \
    -e MINIO_ROOT_USER=LehXBoVThyyDU3vZ \
    -e MINIO_ROOT_PASSWORD=Ggi057AOL8ZRrvxv \
    --name=saber \
    liukunup/saber:v1.0.0
```

### Docker-Compose方式部署

```shell
docker-compose up -f docker/docker-compose.yaml -d 
```

---

## FAQ

- 5000端口被占用

```text
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> Sharing.
```

原因: 端口被其他应用占用; 没有通过Ctrl+C终止命令行

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
