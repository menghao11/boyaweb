from flask import Flask, render_template, request, redirect
import requests
import json
import sys

app = Flask(__name__)
sys.path.append('../')

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route('/welcome/')
def build():
    return render_template('welcome.html')

@app.route("/loginaction", methods=['post'])
def Login():
    user = request.form.get('username')
    password = request.form.get('password')
    if user == 'admin' and password == 'root':
        return redirect("/welcome/")
    else:
        return hello_world()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
