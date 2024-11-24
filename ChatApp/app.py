from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import re
import hashlib
import os

app = Flask(__name__)
#セッション情報の暗号化にsecret_keyが必要で、今回はuuidを16進数化することを利用して、ランダムなstrかbytes列を作る。
#app.config['SECRET_KEY']ともかける。appの属性を設定するこの書き方でもオブジェクトに値が送られるので、以下のように書いても良い。
app.secret_key = uuid.uuid4().hex
app.permanent_session_lifetime = timedelta(days = 25)
salt = os.urandom(32)

#サインアップ画面表示
@app.route('/signup', methods = ["GET"])
def signup():
     return render_template('/registration/signup.html')

#サインアップ処理
@app.route('/signup', methods = ["POST"])
def signup_user():
     id = uuid.uuid4()
     name = request.form.get("user_name")
     email = request.form.get("email")
     password1 = request.form.get("password1")
     password2 = request.form.get("password2")

     pattern = "^(\w.*)@(\w.*).(\w.*)$"
     pattern_pass = "^[A-Za-z0-9_@&%.*]{8,16}$"

     if name == "" or email == "" or password1 == "" or password2 == "":
          flash('空欄があります。')
          print("form_check")

     elif re.match(pattern,email) is None:
          print("email_re_check")
          flash('Emailの形式で入力をお願いします。')

     elif password1 != password2:
          print("passcheck")
          flash("パスワードは、同じパスワードを入れてください。")

     elif len(email) > 80:
          print("email_lengthcheck")
          flash('利用可能なEmailを入力してください。')

     elif re.match(pattern_pass,password1) is None:
          print("pass_patterncheck")
          flash("パスワードは8文字以上16文字以下の英数字混合(_,%,@,&含む)で入力してください")

     else:
          uid = uuid.uuid4()
          original_password = password1
          password = hashlib.sha256(salt + original_password.encode()).hexdigest()
          DB_user = dbconnect.get_user(email)
          if DB_user != None:
               flash("すでに登録済みのEmailです。")
          else:
               dbconnect.create_user(uid,name,email,password)
               session["uid"]= str(uid)
               flash("登録ありがとうございます！")
               return redirect("/")
     return redirect('/signup')

#ログインページ表示
@app.route('/login',methods = ["GET"])
def login():
     return render_template("registration/login.html")

#ログイン処理
@app.route('/login',methods = ["POST"])
def login_user():
     email = request.form.get("email")
     password = request.form.get("password")
     hashed_pass = hashlib.sha256(salt + password.encode()).hexdigest()
     print(hashed_pass)
     if email == "" or password == "":
          flash("空のフォームがあります。")
     else:
          DB_user = dbconnect.get_user(email)
          if DB_user is None:
              flash("登録されていないようです。登録をお願いします。")
              return redirect("/login")
          else:
              db_password = DB_user['password']
              print(DB_user)
              if hashed_pass == db_password:
                  uid = DB_user['id']
                  session['uid']= str(uid)
                  return redirect("/")
              else:
                  flash("パスワードがちがいます。")
                  return redirect('/login')
     return redirect('/login')

#ログアウト処理
@app.route('/logout')
def logout():
     session.clear()
     return redirect('/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)