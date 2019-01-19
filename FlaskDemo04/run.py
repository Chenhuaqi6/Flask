from flask import Flask, request, render_template
import os
import datetime
app = Flask(__name__)

@app.route('/01-file',methods=['GET','POST'])
def file_views():
    if request.method == 'GET':
        basedir = os.path.dirname(__file__)
        print(basedir)
        return  render_template('01-file.html')
    else:
        uname = request.form.get('uname')
        print('用户名:'+uname)

        #获取文件: uimg
        f = request.files['uimg']

        #保存路径 : static/upload/xxx.jpg'
        ftime = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        ext = f.filename.split('.')[-1]
        #组合新的文件名
        filename = ftime+ '.' +ext
        print('文件名为:'+filename)
        #获取绝对路径
        basedir = os.path.dirname(__file__)
        #绝对路径+保存目录+文件
        uplaod_path = os.path.join(basedir,'static/upload',filename)
        print('上传的路径:'+uplaod_path)
        f.save(uplaod_path)

        return '获取文件成功'


if __name__ == '__main__':
    app.run(debug=True,port=3000)