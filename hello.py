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
    return render_template('login.html')

@app.route('/welcome')
def build():
    return render_template('welcome.html')

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
        return hello_world()

@app.route("/registeraction", methods=['post'])
def Register():
    user = request.form.get('username')
    password = request.form.get('password')

    if user == "admin":
        return Register()
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()
    pwd_encry = getEncrytion(password)
    if checkExist(cursor, user):
        print("user %s is exist.", user)
        db.close()
        return Register()
    else:
        insertUser(cursor, user, pwd_encry)
        return Login()

def getEncrytion(password):
    bpwd = bytes(password, encoding='utf-8')

    m = hashlib.md5()
    m.update(bpwd)

    md5_pwd = m.hexdigest()
    return md5_pwd

def checkAuth(user, password):
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    cursor = db.cursor()

    sql = "SELECT PASSWORD FROM EDU_USER \
           WHERE NAME = %s" % (user)
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
                db.close()
                return False
    except:
        print("Error: unable to fetch data")
        db.close()
        return False

def checkExist(cursor, user):
    sql = "SELECT PASSWORD FROM EDU_USER \
           WHERE NAME = %s" % (user)
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        if results != None:
            return False
        else:
            return True
    except:
        print("Error: unable to fetch data")
        return False

def insertUser(cursor, user, password):
    sql = "INSERT INTO EDU_USER(NAME, PASSWORD) VALUES (%s, %s)" % (user, password)
    try:
        # 执行SQL语句
        cursor.execute(sql)
    except:
        print("Error: unable to insert data")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)
