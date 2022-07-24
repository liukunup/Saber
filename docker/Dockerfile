# 基础镜像
FROM python:3.9-alpine

# FLASK
ENV FLASK_APP main.py
ENV FLASK_CONFIG docker
# 超级管理员
ENV SUPER_ADMIN Administrator
# 数据库
ENV MYSQL_HOST 127.0.0.1
ENV MYSQL_PORT 3306
ENV MYSQL_USERNAME username
ENV MYSQL_PASSWORD password
ENV MYSQL_DATABASE saber
# 对象存储
ENV MINIO_USERNAME username
ENV MINIO_PASSWORD password
ENV MINIO_BUCKET saber

# 专有用户
RUN adduser -D flaskr
USER flaskr
# 工作路径
WORKDIR /home/flaskr

# 环境部署
COPY requirements requirements
RUN python -m venv venv
RUN venv/bin/pip install -r requirements/docker.txt

# 拷贝源文件
COPY app app
COPY migrations migrations
COPY main.py run.sh ./

# 端口暴露
EXPOSE 5000

# 程序入口
ENTRYPOINT ["./run.sh"]
