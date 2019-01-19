from _operator import or_

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from sqlalchemy import func,or_

app = Flask(__name__)

#先在mysql中创建一个库----create database flask05 default charset utf8 collate utf8_general_ci;
#配置连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask05'
#配置app的启动模式为调试模式
app.config['DEBUG']= True
#配置自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

#创建数据库的实例
db = SQLAlchemy(app)

#创建Manger对象并指定要管理哪个应用
manager = Manager(app)

#创建Migrate对象并指定要关联的app和db
migrate = Migrate(app,db)
#为manager增加命令:允许做数据表迁移的命令
manager.add_command('db',MigrateCommand)


def __repr__(self):
    return "<User:%s>" % self.uname
class Users(db.Model):
    __tablename__ = "users"
    id =db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    age = db.Column(db.Integer,nullable=True)
    email = db.Column(db.String(200),unique=True)
    birth = db.Column(db.Date)
    isActive = db.Column(db.Boolean,default=True)


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer,primary_key=True)
    sname = db.Column(db.String(30))
    sage = db.Column(db.Integer)
    isActive = db.Column(db.Boolean,default=True)


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer,primary_key=True)
    tname = db.Column(db.String(30),nullable=True)
    tage = db.Column(db.Integer,nullable=False)
    #增加对Course("一"表)类的引用
    course_id = db.Column(db.Integer,db.ForeignKey('course.id'))
    #增加对多对多
    students = db.relationship('Student',
                               secondary='teacher_student',
                               lazy='dynamic',
                               backref=db.backref('teachers',lazy='dynamic'))

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(50),nullable=True)
    #增加关联属性和反向引用关系属性
    teachers = db.relationship('Teacher',
                               backref='course',
                               lazy='dynamic'
    )

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True)
    uname = db.Column(db.String(50))
    uage = db.Column(db.Integer)
    uemail = db.Column(db.String(200))
    isActive = db.Column(db.Boolean,default=True)
    #增加关联属性和反向引用关系属性
    wife = db.relationship('Wife',backref='user',uselist=False)

#创建Wife实体类
class Wife(db.Model):
    __tablename__ = 'wife'
    id = db.Column(db.Integer,primary_key=True)
    wname = db.Column(db.String(30))
    Wage = db.Column(db.Integer)
    #增加一对一的引用关系:引用自user中的主键id
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'),unique=True)
    def __repr__(self):
        return "<Wife:%r>" % self.wname

#创建TeacherStudent实体类 第三张表
class TeacherStudent(db.Model):
    __tablename__ = 'teacher_student'
    id = db.Column(db.Integer,primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    student_id = db.Column(db.Integer,db.ForeignKey('student.id'))

#创建goods表,表示商品
class Goods(db.Model):
    __tablename__ = 'goods'
    id = db.Column(db.Integer,primary_key=True)
    gname = db.Column(db.String(50))
    price = db.Column(db.Float)
    #增加对user(多)的关联关系(多对多)
    users = db.relationship('User',secondary='Shoppingcart',lazy='dynamic',backref=db.backref('goods',lazy='dynamic'))



#创建ShoppingCart表,表示购物车
class ShoppingCart(db.Model):
    __tablename__ = 'Shoppingcart'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    goods_id = db.Column(db.Integer,db.ForeignKey('goods.id'))
    count = db.Column(db.Integer,nullable=False)

@app.route('/')
def index():
    return "This is my first page"

@app.route('/01-adduser')
def addUser_views():
    #1.创建User的实体对象
    user = User()
    user.uname = 'Wangwc'
    user.uage = 28
    user.uemail = 'wangwc@163.com'
    #2.通过db.session.add() 保存实体对象
    db.session.add(user)
    #33.提交回数据库
    # db.session.commit()
    return '提交数据成功'

@app.route('/02-query')
def query_virews():
    #1.测试db.session.query()的作用
    #查询User表中所有的列
    # query = db.session.query(User)
    #查询User表中id和uname列
    # query = db.session.q|uery(User.id,User.uname)
    #查询user表和student表中连接后的所有数据
    # query = db.session.query(User,Student)
    # print(type(query))
    # print(query)
    ##2.测试查询执行函数
    #####################
    ##2.1 db.session.query().all()
    # users = db.session.query(User).all()
    # for u in users:
    #     print('id:%d,uname:%s,uage:%d,uemail:%s' % (u.id,u.uname,u.uage,u.uemail))

    ##2.2 查询user表中所有数据的id和uname俩个列的值并输出在终端上
    # users = db.session.query(User.id,User.uname).all()
    # for u in users:
    #     print('id:%d,uname:%s' % (u.id,u.uname))

    ##2.3 查询user表中的第一条数据
    # u = db.session.query(User).first()
    #
    # print('id:%d,uname:%s,uage:%d,uemail:%s' % (u.id,u.uname,u.uage,u.uemail))
    #
    # ##2.4 查询user中共有多少条数据
    # count = db.session.query(User).count()
    # print('user表中共有%d条数据' % count)

    ###########################
    ###3.测试filter()函数
    ############################

    ###3.1 查询年龄大于17 的user表中的信息
    # users = db.session.query(User).filter(User.uage > 17).all()
    # print(users)

    ###3.2 年龄大于17并且id>1的user信息
    # users = db.session.query(User).filter(User.uage > 17,User.id > 2).all()
    # print(users)\

    ###3.3 查询年龄大于17或者id大于1的user的信息
    # users = db.session.query(User).filter(or_(User.uage > 17,User.id>1)).all()
    # print(users)

    ###3.4 查询id等于2 的user信息
    # user = db.session.query(User).filter(User.id == 2).first()
    # print(user)

    ##3.5 查询uemail中包含w字符的user的信息
    # users = db.session.query(User).filter(User.uemail.like('%CH%')).all()
    # print(users)

    #4.1测试 filter_by()
    # users = db.session.query(User).filter_by(id=1).first()
    # print(users)

    ###############
    #5.测试limit() / offset()函数
    ######################
    # users = db.session.query(User).limit(1).all()
    # print(users)

    #跳过前3条,取一条数据
    # users = db.session.query(User).limit(1).offset(3).all()
    # print(users)

    ################
    #6.测试order_by()函数
    #################
    # users = db.session.query(User).order_by('id desc').all()
    # print(users)
    #升序ac可省略
    users = db.session.query(User).order_by('uage,id desc').all()
    print(users)
    return '<script> alert("查询成功");</script>'

@app.route('/03-queryall')
def queryall_views():
    users = db.session.query(User).all()


    return render_template('03-queryall.html',users=users)

@app.route('/04-update',methods=['GET','POST'])
def update_views():
    if request.method == 'GET':
        #接收前端传递过来的用户id
        id = request.args['id']
        user = db.session.query(User).filter_by(id=id).first()
        #根据id将对应的用户的信息读取出来
        #将读取出来的实体对象发送到04-update.html上显示出来
        return render_template('04-update.html',user = user)
    else:
        # 接收前端传递过来的四个值（id，username，uage，uemail）
        id = request.form['id']
        print(id)
        uname = request.form['uname']
        uage = request.form['uage']
        uemail = request.form['uemail']
        # 根据id查询出对应的user的信息
        user = User.query.filter_by(id=id).first()
        # 将user的信息保存回数据库
        user.uname = uname
        user.uage = uage
        user.uemail = uemail
        # 将user的信息保存回数据库
        db.session.add(user)
        # 响应：重定向回/03-queryall
        return redirect('/03-queryall')


@app.route('/05-query')
def query05_views():
    ###############
    ##1.聚合函数的使用
    ##1.1 查询user表中所有的年龄的平均值
    # result = db.session.query(func.avg(User.uage)).first()
    # print(result[0])
    # print(type(result))
    ##1.2 在user表中按uage进行分组,求每组中的年龄的平均值,以及uage的总和
    # result = db.session.query(User.uage,func.avg(User.uage),func.sum(User.uage)).group_by('uage').all()
    # # print(result)
    # for r in result:
    #     print("组:",r[0],'平均年龄:',r[1],'总年龄:',r[2])

    result = db.session.query(User.isActive,func.count(User.isActive)).group_by('isActive').all()
    for r in result:
        print(r[0],'的数量为:',r[1])

    return "<script>alert('查询成功');</script>"

@app.route('/06-delete')
def delete_views():
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    return redirect('/03-queryall')


@app.route("/07-update")
def update06_views():
    #修改id为4的用户的信息
    user=User.query.filter_by(id=2).first()
    print(user)
    user.uname = "Zhexue Lv"
    user.uage = 30
    user.uemail = "Lvze@162.com"
    user.isActive = True
    db.session.add(user)

    return "<script>alert('修改成功');</script>"
@app.route('/08-addteacher')
def addteacher_views():
    # 解析:
    # 每个teacher对象中都有一个属性course_id(手动添加)
    # 每个teacher对象中都有一个属性course(通过反向引用添加)
    #
    # 方式1:通过反向引用关系属性增加数据
    # 1.1 获取id为1的课程(course)对象
    course = Course.query.filter_by(id=4).first()
    #1.2 创建teacher对象并指定
    teacher = Teacher()
    teacher.tname = '陈'
    teacher.tage = 21
    #1.3 为teacher对象指定关联的course对象
    teacher.course = course
    print(teacher.course)
    #1.4 将teacher保存会数据库
    db.session.add(teacher)
    # return '增加数据成功'
    #方式2:通过外键列的方式增加数据
    # teacher = Teacher()
    # teacher.tname = '王老师'
    # teacher.tage = 31
    # #通过外键列增加数据
    # teacher.course_id = 1
    # db.session.add(teacher)
    return '增加数据成功'

@app.route('/09-regteacher',methods=['POST','GET'])
def regteacher_views():
    if request.method == 'GET':
        #查询所有的课程
        courses = Course.query.all()
        return render_template('09-regteacher.html',courses=courses)


    else:
        teacher = Teacher()
        teacher.tname = request.form['tname']
        teacher.tage = request.form['tage']
        teacher.course_id = request.form['course_id']
        db.session.add(teacher)
        return redirect('/05-showTea')
@app.route('/05-showTea')
def showTea():
    teachers = Teacher.query.all()
    return render_template('05-showTea.html',teachers = teachers)

#通过course获取teachers
#通过teacher获取course
@app.route('/10-getcourse')
def getcourse_views():
    #通过course获取teachers
    #1.获取id为1 的course的信息
    # course = Course.query.filter_by(id = 1).first()
    # #2.获取关联的teachers
    # teaList = course.teachers.all()
    # for tea in teaList:
    #     print('姓名:%s,年龄:%d' % (tea.tname,tea.tage))
    # return '获取数据成功'

    #通过teacher得到对应的course
    #1.获取id为1的老师的信息
    teacher = Teacher.query.filter_by(id = 1).first()
    print('教师姓名:',teacher.tname)
    #2.再通过反向引用查找对应的course
    course = teacher.course
    print('教授课程:',course.cname)
    return '数据获取成功'


@app.route('/11-showteachers')
def showteacher_views():
    courses = Course.query.all()
    #1.判断是否有参数,如果没有参数或参数为-1 则查询所有的老师们的信息
    if 'id' not in request.args or request.args['id'] == "-1":
        teachers = Teacher.query.all()
    else:
        id = request.args['id']
        course = Course.query.filter_by(id = id).first()
        teachers = course.teachers.all()
    return render_template('11-showteachers.html',params = locals())

@app.route('/12-addwife')
def addwife_views():
    #1.通过外键属性user_id关联user与wife
    # wife = Wife()
    # wife.wname = 'WC夫人'
    # wife.wage = 38
    # wife.user_id = 6
    # db.session.add(wife)
    #2.通过反向引用关系属性关联user与wife
    user = User.query.filter_by(id=7).first()
    wife = Wife()
    wife.wname = '王夫人'
    wife.wage = 46
    wife.user = user
    db.session.add(wife)
    return '添加成功'

@app.route('/13-queryuser')
def query_views():
    #判断请求中是否包含参数-uname
    if 'uname' in request.args:
        #获取参数
        uname = request.args['uname']
        #按照参数构造条件并查询数据
        users = User.query.filter(User.uname.like('%'+uname+'%')).all()
    else:
        users = User.query.all()
    return render_template('13-queryuser.html',params=locals())

@app.route('/14-regstudent')
def regstudent_views():
    #查询id为1 的Teacher的信息
    tea = Teacher.query.filter_by(id=1).first()
    #查询id为1 的Student的信息
    stu = Student.query.filter_by(id=1).first()


    tea.students.append(stu)
    return '增加关联数据成功'
@app.route('/15-queryteacher')
def queryteacher_views():
    #查询0id为1的老师对应学生的信息
    tea = Teacher.query.filter_by(id = 1).first()
    students = tea.students.all()
    for stu in students:
        print('姓名:%s,年龄:%s' % (stu.sname,stu.sage))
    return '查询成功'
if __name__ == '__main__':
    #通过manager管理启动程序
    manager.run()