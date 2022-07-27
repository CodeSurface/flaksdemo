from http.cookiejar import Cookie
from flask import Blueprint, Flask, redirect, render_template, request, session,flash, url_for,sessions
from sqlalchemy import null
from models import User
from exts import db
from werkzeug.security import generate_password_hash,check_password_hash
bp = Blueprint("user",__name__,url_prefix="/user")

@bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            session['username'] = username
            print (username)
            return render_template("index.html",user = user)
            #return redirect(url_for('index'))
        else:
            flash("用户名或密码错误")
            return render_template("login.html")
        
        
        
@bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash("该用户名已存在")
            return render_template("register.html")
        else:
            
            hash_password = generate_password_hash(password)
            user = User(username=username,password=hash_password)
            db.session.add(user)
            db.session.commit()
            return render_template("login.html")
    
    
@bp.route('/drop',methods=['GET','POST'])
def drop():
    if request.method == 'GET':
        return render_template("drop.html")
    else:
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password,password):
            db.session.delete(user)
            db.session.commit()
            flash("删除成功")
            return render_template("login.html")
        else:
            flash("删除失败")
            return render_template("drop.html")


@bp.route('/update',methods=['GET','POST'])
def update():
    if request.method == 'GET':
        return render_template("update.html")
    else:
        #username = session['username']
        username = session['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if password == "" or password is null:
            flash( "密码不能为空")
            return render_template("update.html")
        else:
            if user:
                user.password = generate_password_hash(password)
                db.session.commit()
                flash("修改成功，请重新登录·")
                return redirect(url_for('user.login'))
            else:
                flash("请勿与原密码一致")
                return render_template("update.html")
@bp.route('/logout')
def logout():
    if request.method == 'GET':
        session.clear()
        #print (session)
        #print (Cookie)
        #print("删除后"+ session['username'])
        return render_template("index.html")
        #return redirect(url_for('user.login'))