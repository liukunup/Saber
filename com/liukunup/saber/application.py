# -*- coding: UTF-8 -*-
# application.py

# -------------------------------------------------------- env --------------------------------------------------------
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# -------------------------------------------------------- app --------------------------------------------------------
import click
import unittest

from flask_migrate import Migrate, upgrade
from com.liukunup.saber import create_app, db
from com.liukunup.saber.repository import Role, User

app = create_app(os.getenv("FLASK_CONFIG") or "testing")
migrate = Migrate(app, db)


# -------------------------------------------------------- cli --------------------------------------------------------
@app.cli.command()
def deploy():
    """发布命令"""
    # 迁移数据库
    upgrade()
    # 创建角色
    Role.insert_roles()
    # 创建超级管理员
    User.add_super_administrator(os.getenv("SUPER_ADMIN") or "Administrator", "This is a super administrator.", "Admin")


@app.cli.command()
@click.argument('test_names', nargs=-1)
def test(test_names):
    if test_names:
        tests = unittest.TestLoader().loadTestsFromNames(test_names)
    else:
        tests = unittest.TestLoader().discover("com.liukunup.saber.tests")
    unittest.TextTestRunner(verbosity=2).run(tests)
