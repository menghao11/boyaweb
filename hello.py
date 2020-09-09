from flask import Flask, render_template, request, redirect
import requests
import json
import hashlib
import sys
import pymysql

app = Flask(__name__, static_folder="./static")
sys.path.append('../')

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/welcome')
def build():
    return render_template('welcome.html')

@app.route('/welcome.html')
def welcome():
    return render_template('welcome.html')

@app.route('/register.html')
def register():
    return render_template('register.html')

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route("/loginaction", methods=['post'])
def Login():
    user = request.form.get('username')
    password = request.form.get('password')

    if user == "admin" and password == "root":
        return redirect("/welcome")

    pwd_encry = getEncrytion(password)
    if checkAuth(user, pwd_encry):
        print("user %s login success.", user)
        return redirect("/welcome")
    else:
        print("user %s login failed.", user, pwd_encry)
        return hello_world()

@app.route("/registeraction", methods=['post'])
def Register():
    user = request.form.get('username')
    password = request.form.get('password')

    if user == "admin" or user == "":
        return Register()
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='TESTDB')
    cursor = db.cursor()
    pwd_encry = getEncrytion(password)
    if checkExist(cursor, user):
        print("user %s is exist.", user)
        db.close()
        return "username "+ user + "is duplicated."
    else:
        insertUser(db, user, pwd_encry)
        return Login()

def getEncrytion(password):
    bpwd = bytes(password, encoding='utf-8')

    m = hashlib.md5()
    m.update(bpwd)

    md5_pwd = m.hexdigest()
    return md5_pwd

def checkAuth(user, password):
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db='TESTDB')

    cursor = db.cursor()

    sql = "SELECT PASSWORD FROM EDU_USER WHERE NAME = '%s'" % (user)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            pwd = row[0]
            if pwd == password:
                db.close()
                return True
            else:
                print(pwd, password)
                db.close()
                return False
    except Exception as e:
        print("Error: unable to fetch data", e)
        db.close()
        return False

def checkExist(cursor, user):
    sql = "SELECT NAME FROM EDU_USER WHERE NAME = '%s'" % (user)

    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        for row in results:
            name = row[0]
            if name == user:
                return True
            else:
                return False
    except Exception as e:
        print("Error: unable to fetch data", e)
        return False

def insertUser(db, user, password):
    cursor = db.cursor()
    sql = "INSERT INTO EDU_USER(NAME, PASSWORD) VALUES ('%s', '%s')" % (user, password)
    print(sql)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        print("Error: unable to insert data", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
