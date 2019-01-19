from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flask'
#为Flask的程序实例指定SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    tname = db.Column(db.String(30))
    tage = db.Column(db.Integer)

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True)
    cname = db.Column(db.String(50),nullable=True)

db.create_all()


if __name__ == '__main__':
    app.run(debug=True)