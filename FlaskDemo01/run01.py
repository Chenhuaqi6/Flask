from flask import Flask

#将当前运行的主程序构建成Flask应用,以便接收用户(request)的请求给出响应(response)
app = Flask(__name__)


#@app.route() 定义Falsk中的路由,就是访问路径,'/'表示的是整个网站的根路径
#index()表示的是匹配上路由之后的处理程序-视图函数,所有的视图必须要有一个return用于表示响应的内容
# @app.route('/')
# def index():
#     print("这是在终端输出的")
#     return "This is my first flask demo"

#http://localhost:5000/login
@app.route('/login')
def login():
    return "<h1>欢迎来到登录页面</h1>"

@app.route('/register')
def register():
    return '<h1>欢迎来到注册界面</h1>'

#参数1 : 基本带参数路由的体现
@app.route('/show/<name>')
def show(name):
    return "传递进来的参数为:"+name
#参数2: 带多个参数的路由实现
@app.route('/show1/<name>/<age>')
def show1(name,age):
    return "姓名:%s,年龄:%s" % (name,age)

#参数3:使用类型转换器实现参数的类型转换
@app.route('/calc/<int:num1>/<int:num2>')
def calc(num1,num2):
    #num1和num2全部都是整型的
    return "%d+%d=%d" % (num1,num2,num1+num2)

#定义多url的路由匹配
@app.route('/')
@app.route('/index')
@app.route('/<int:page>')
@app.route('/index/<int:page>')
def index_views(page=None):
    if page is None:
        page = 1
    return "您当前看的页数为%d" % page


@app.route('/post',methods=['POST','GET'])
def post():
    return "该方法允许接受post和GET请求"


if __name__ == "__main__":
    #运行Falsk应用(启动Flask服务),启动之后允许通过http://localhost:5000的方式来访问当前项目
    #debug = true 显示错误在页面上
    app.run(debug=True)



