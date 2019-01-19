#与users业务相关的路由和视图处理函数
from flask import render_template, request

from . import user
from .. import db
from ..models import *

@user.route('/users')
def user_index():
    return "这是users应用中的首页程序"


