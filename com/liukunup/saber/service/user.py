# -*- coding: UTF-8 -*-
# 服务: 用户CRUD

import typing as t

from com.liukunup.saber import db
from com.liukunup.saber.repository import User


class UserService:
    """ User服务 """

    @staticmethod
    def select(user_id: int) -> t.Optional[User]:
        """
        根据 id 查询 User对象
        :param user_id: 用户ID
        :return: User对象
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def insert(dat: t.Dict) -> User:
        """
        新增用户
        :param dat: 字典格式的用户信息
        :return: 已新增的User对象
        """
        user = User.from_json(dat)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def remove(user_id: int) -> t.NoReturn:
        """
        删除用户
        :param user_id: 用户ID
        :return: 无返回值
        """
        db.session.query(User).filter(User.id == user_id).delete()
        db.session.commit()
