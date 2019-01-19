#导包
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

#导入 pymysql 并当成 MySQLdb取运作
# import pymysql
# pymysql.install_as_MySQLdb()



#创建Flask的程序实例
app = Flask(__name__)
#为Flask的程序实例指定数据库的配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask'
app.config['DEBUG'] = True
#通过Flask的程序实例创建数据库的应用实例
db = SQLAlchemy(app)

#创建Manger管理的app
manager = Manager(app)

#管理Manager 和 db
migrate = Migrate(app,db)

#为manager增加命令
manager.add_command('db',MigrateCommand)

#创建一个实体类 -- Users
# 映射到数据库中表名叫:users
#创建字段:id,主键,自增
#创建字段:username,长度为80的字符串,不允许为空,值要唯一
#创建字段:age,整数,允许为空,
#创建字段:email,长度为200的字符串,唯一
#创建字段:birth,日期类型
#创建字段:isActive,布尔类型,默认值为true

class Users(db.Model):
    __tablename__ = "users"
    id =db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer,nullable=True)
    email = db.Column(db.String(200),unique=True)
    birth = db.Column(db.Date)
    isActive = db.Column(db.Boolean,default=True)

#将创建好的实体类映射回数据库
db.create_all()



@app.route('/')
def index():
    print(db) #能打印输出则说明db创建成功
    return '程序访问成功'


if __name__ == '__main__':
    # app.run(debug=True,port=3000)
    manager.run()