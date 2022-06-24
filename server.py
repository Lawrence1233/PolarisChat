#coding:gbk
from flask import Flask, render_template, request, redirect,make_response
import time
app = Flask(__name__)

mark={'0.0.0.0':0}

message=[]
user_list=[]
app.secret_key = '309128904890123kjlkjlkefu298foi32jiej23jeri9j329irj32j4klj32lk4dn23lmnlkjkldj23lkjdkl23jr2lcjnrlk23ncc24jelk23'
@app.route('/',methods=["POST","GET"])
def index():
    if request.method == 'GET':
        h="""
        <!doctype html>
        Polaris Chat Server<br/>
        这个网站是Polaris Studio制作的Polaris Chat的服务器<br/>
        您需要使用POST方法访问该网站<br/>
        """
        return h
    return 'server_is_online',200

@app.route('/upload',methods=["POST","GET"])
def upload():
    if request.method == 'GET':
        return redirect('/')
    global message
    name = request.cookies.get('username')
    if name not in user_list:
        return "401 Unauthorized",401
    content=request.form.get('xxx')
    message.append("%s:%s"%(name,content))
    return 'OK',200

@app.route('/get_message',methods=["POST","GET"])
def get_message():
    if request.method == 'GET':
        return redirect('/')
    global message

    if request.headers.get('X-Forwarded-For') in mark:
        if time.time()-mark[request.headers.get('X-Forwarded-For')] < 50:
            return '403 Forbidden',403

    name = request.cookies.get('username')
    if name not in user_list:
        return "401 Unauthorized",401
    return str(message[-1]),200

@app.route('/get_all_message',methods=["POST","GET"])
def get_all_message():
    if request.method == 'GET':
        return redirect('/')
    global message

    if request.headers.get('X-Forwarded-For') in mark:
        if time.time()-mark[request.headers.get('X-Forwarded-For')] < 50:
            return '403 Forbidden',403

    name = request.cookies.get('username')
    print(name)
    if name not in user_list:
        return "401 Unauthorized",401
    return str(message),200

@app.route('/join',methods=["POST","GET"])
def join_user():
    global user_list
    temp='user%s'%int(time.time())
    user_list.append(temp)
    res=make_response('OK')
    res.set_cookie('username',temp,max_age=86400)
    return res,200

@app.route('/sign_out')
def sign_out():
    global user_list
    name = request.cookies.get('username')
    if name in user_list:
        user_list.remove(name)
        res.set_cookie('username','undefined')
        return 'OK',200
    else:
        return 'FAIL:Nonexistent user',401

@app.before_request
def bf():
    print(request.headers)


app.run(host='localhost',port=8445)