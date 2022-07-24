# -*- coding: UTF-8 -*-
# Demo Controller

from flask import jsonify
from com.liukunup.saber.controller import api
from com.liukunup.saber.bean import Success


@api.route("/demo", methods=["GET"])
def demo():
    return jsonify(Success(None).json())


@api.route("/demo/<int:with_param>", methods=["GET"])
def demo_with_param(with_param):
    return jsonify(Success(with_param).json())
