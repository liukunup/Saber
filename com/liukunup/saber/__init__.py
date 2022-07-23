#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_talisman import Talisman
# 可选配置项
from com.liukunup.saber.configuration import config

# The Python SQL Toolkit and Object Relational Mapper
db = SQLAlchemy()
# Talisman: HTTP security headers for Flask
talisman = Talisman()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)

    if app.config['USE_TALISMAN']:
        talisman.init_app(app)

    from .controller import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/saber")

    return app
