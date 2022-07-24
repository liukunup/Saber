# -*- coding: UTF-8 -*-
# User Controller

from flask import jsonify, request, url_for
from com.liukunup.saber.controller import api
from com.liukunup.saber.service.user import UserService
from com.liukunup.saber.bean import Success, Failed
from com.liukunup.saber.service import audit, required_sign, required_perm, required_admin, rate_limiter
from com.liukunup.saber.repository import Permission


@api.route("/user/<int:user_id>", methods=["GET"])
@required_sign
@required_perm(Permission.READ)
@audit
@rate_limiter
def get_user(user_id):
    user = UserService.select(user_id=user_id)
    if user is None:
        return jsonify(Failed("No such user").json())
    return jsonify(Success(user.json()).json())


@api.route("/user", methods=["POST"])
@required_sign
@required_admin
@audit
def add_user():
    user = UserService.insert(dat=request.json)
    return jsonify(Success(user.json()).json()), 201, {"Location": url_for("api.get_user", user_id=user.id)}


@api.route("/user/<int:user_id>", methods=["DELETE"])
@required_sign
@required_admin
@audit
def del_user(user_id):
    UserService.remove(user_id=user_id)
    return jsonify(Success(None).json())
