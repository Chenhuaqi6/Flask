from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/ajax'
db =SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    loginname = db.Column(db.String(30))
    loginpwd = db.Column(db.String(30))
    username = db.Column(db.String(30))

    def to_dict(self):
        dic = {
            'id':self.id,
            'loginname':self.loginname,
            'loginpwd':self.loginpwd,
            'username':self.username
        }
        return dic

db.create_all()


@app.route('/02-server')
def server01_views():
    return '这是我的第一个ajax的响应'

@app.route('/03-server')
def server03_views():
    #接收前端传递过来的数据
    uname = request.args['uname']
    return '欢迎:'+uname

@app.route('/04-post')
def post():
    return render_template('04-post.html')

@app.route('/04-server',methods=['POST'])
def server04():
    uname = request.form['uname']
    age = request.form['age']
    return "姓名:%s,年龄:%s" % (uname,age)


@app.route('/02-form',methods=['GET','POST'])
def form():
    if request.method == 'GET':
        return render_template('02-form.html')
    else:
        uname = request.form['uname']
        uage = request.form['uage']
        return '传递过来的uname值为:%s,uage值为:%s' % (uname,uage)

#注册
@app.route('/06-register')
def register_views():
    return render_template('06-register.html')
#注册的服务,判断有无 returnn的值就是 requestText
@app.route('/06-server')
def server06():
    #接收前端传递过来的参数 - lname
    lname = request.args['lname']
    #以 lname作为条件,通过Users实体类查询数据
    user = Users.query.filter_by(loginname=lname).first()
    #如果查询出来了数据的话说明登录名称已存在,否则通过
    if user:
        return '用户名称已存在'
    else:
        return '用户名可用'


@app.route('/07-getlogin')
def getlogin():
    return render_template('03-getlogin.html')
@app.route('/07-server')
def server03():
    logins = Users.query.all()
    str1 = ''
    for login in logins:
        str1 += str(login.id)
        str1 += login.loginname
        str1 += login.loginpwd
        str1 += login.username
    return str1

@app.route('/04-json')
def json_views():
    return  render_template('04-json.html')


@app.route('/04-server')
def server_04():
    # list = ["王老师","Rapwang",'隔壁老王']
    #将list转换为json格式的字符串
    # dic = {
    #     'name':'TeacherWang',
    #     'age':35,
    #     'gender': 'Male'
    # }
    # jsonStr = json.dumps(dic)
    list = [{
        "name":"wangwc",
        "age":35,
        "gender":"male"
    },
        {
            "name":"Rapwang",
            "age":40,
            "gender":"Female"
        }]
    jsonStr = json.dumps(list)
    return  jsonStr


@app.route('/05-json-login')
def json_login():
    return render_template('05-json-login.html')

@app.route('/05-server')
def server05():
    #得到id为1 的login的信息
    login = Users.query.filter_by(id = 1).first()
    jsonStr = json.dumps(login.to_dict())
    return jsonStr

if __name__ == '__main__':
    app.run(debug=True)