# -*- coding: UTF-8 -*-
# 角色/用户

import random
import string

from datetime import datetime
from flask import current_app, url_for
from com.liukunup.saber.bean import Code, CustomException
from com.liukunup.saber import db


class Permission:
    """ 权限类型 """
    # 可读
    READ = 1
    # 可写
    WRITE = 2
    # 可更新
    UPDATE = 4
    # 可删除
    DELETE = 8
    # 可管理
    ADMIN = 16


class Role(db.Model):
    """ 角色 """

    # 表名称
    __tablename__ = "role"

    # 表字段
    id = db.Column(db.BigInteger, comment="记录编号", primary_key=True)
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    name = db.Column(db.String(16), comment="角色", unique=True)
    default = db.Column(db.Boolean, comment="是否为默认角色", default=False, index=True)
    permissions = db.Column(db.Integer, comment="权限")
    users = db.relationship("User", backref="role", lazy="dynamic")
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            "Follower": [Permission.READ],
            "Executor": [Permission.READ, Permission.WRITE],
            "Owner": [Permission.READ, Permission.WRITE, Permission.UPDATE, Permission.DELETE],
            "Administrator": [Permission.READ, Permission.WRITE, Permission.UPDATE, Permission.DELETE, Permission.ADMIN]
        }
        default_role = "Follower"
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return "<Role %r>" % self.name


class User(db.Model):
    """ 用户 """

    # 表名称
    __tablename__ = "user"

    # 表字段
    id = db.Column(db.BigInteger, comment="记录编号", primary_key=True)
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    name = db.Column(db.String(256), comment="名称", nullable=False, unique=True)
    desc = db.Column(db.String(256), comment="描述")
    access_key = db.Column(db.String(32), comment="公钥", nullable=False, unique=True, index=True)
    secret_key = db.Column(db.String(32), comment="私钥", nullable=False)
    role_id = db.Column(db.BigInteger, db.ForeignKey("role.id"), comment="角色ID")
    owner = db.Column(db.String(256), comment="所有者(工号或昵称)", nullable=False)
    is_enabled = db.Column(db.Boolean, comment="是否已被启用", nullable=False, default=False)
    audits = db.relationship("Audit", backref="user", lazy="dynamic")
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def add_super_administrator(name, desc, owner):
        # 检查是否已存在超级管理员
        for user in User.query.all():
            if user.name == name:
                print("Warning: 超级管理员已存在!")
        # 创建超级管理员
        user = User(name=name, desc=desc, owner=owner, is_enabled=True)
        db.session.add(user)
        db.session.commit()

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        # 设置用户的角色
        if self.role is None:
            if self.name == current_app.config["SUPER_ADMIN"]:
                self.role = Role.query.filter_by(name="Administrator").first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
        # 自动生成32位AK+SK
        if self.access_key is None:
            self.access_key = "".join(random.sample(string.digits + string.ascii_letters, 32))
        if self.secret_key is None:
            self.secret_key = "".join(random.sample(string.digits + string.ascii_letters, 32))
        # 参数检查
        if self.name is None or self.name == "" or len(self.name) > 256:
            raise CustomException(Code.INVALID_PARAM, payload="允许最长256个字符的非空字符串作为name")
        if self.desc is not None and len(self.desc) > 256:
            raise CustomException(Code.INVALID_PARAM, payload="允许最长256个字符的字符串作为desc")
        if self.owner is None or self.owner == "" or len(self.owner) > 256:
            raise CustomException(Code.INVALID_PARAM, payload="允许最长256个字符的非空字符串作为owner")

    def can(self, perm):
        """ 是否具备权限 """
        return self.role is not None and self.role.has_permission(perm)

    def json(self):
        return {
            "url": url_for("api.get_user", user_id=self.id),
            "id": self.id,
            "name": self.name,
            "desc": self.desc,
            "access_key": self.access_key,
            "role_id": self.role_id,
            "owner": self.owner,
            "is_enabled": self.is_enabled,
            "create_time": self.create_time,
            "update_time": self.update_time,
        }

    @staticmethod
    def from_json(obj):
        return User(name=obj.get("name"), desc=obj.get("desc"),
                    access_key=obj.get("access_key"), secret_key=obj.get("secret_key"),
                    role_id=obj.get("role_id"), owner=obj.get("owner"),
                    is_enabled=obj.get("is_enabled"))

    def __repr__(self):
        return "<User %r>" % self.name


class Audit(db.Model):
    """ 审计日志 """

    # 表名称
    __tablename__ = "audit"

    # 表字段
    id = db.Column(db.BigInteger, comment="记录编号", primary_key=True)
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    user_id = db.Column(db.BigInteger, db.ForeignKey("user.id"), comment="用户ID")
    event = db.Column(db.String(256), comment="事件", nullable=False)
    args = db.Column(db.JSON, comment="参数")
    # ---------------------------------------------------- 业务字段 ----------------------------------------------------
    create_time = db.Column(db.DateTime(), comment="创建时间", default=datetime.utcnow)
    update_time = db.Column(db.DateTime(), comment="更新时间", default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Audit, self).__init__(**kwargs)
