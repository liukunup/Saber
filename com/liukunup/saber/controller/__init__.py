# -*- coding: UTF-8 -*-
# Controller

from flask import Blueprint, jsonify
from com.liukunup.saber.bean import CustomException

api = Blueprint("api", __name__)

from . import user


@api.errorhandler(CustomException)
def handle_custom_exception(e):
    """ 处理捕获的所有自定义异常 """
    return jsonify(e.json())
