from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import datetime
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
    
@app.route('/')
def get_all_channels():
     #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     #チャンネル情報取得
     channels = dbconnect.get_all_channels(uid)
     return render_template('index.html',channels=channels)
  
@app.route('/create-channel',methods=['GET','POST'])
def create_channel():
     #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')

     if request.method == 'POST':
          #チャンネルのidを生成
          cid = uuid.uuid4()

          #htmlで入力された情報を取得
          channel_name = request.form.get('channel_Name')
          event_date = request.form.get('event_date')         
          url = request.form.get('url')         
          uids = request.form.getlist('uids')

          #画像保存
          image = request.files['image_place']
          image_id = uuid.uuid4()
          image_place = os.path.join("static/user-img",str(image_id)) + ".jpg"
          image.save(image_place)

          #チャンネル情報追加
          dbconnect.create_channel(cid,channel_name,event_date,url,image_place,uid)
          dbconnect.add_channelmembers(uids,uid,cid)
          return redirect('/')
     #ログインしているユーザー以外のユーザーを取得
     uids = dbconnect.all_get_other_user(uid)
     return render_template('create-channel.html',uids=uids)
     
@app.route("/edit-channel/<cid>",methods=["GET","POST"])
def update_channel(cid):
     #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     if request.method=="GET":
          #チャンネル情報を取得
          channels= dbconnect.get_channel(cid)
     	#ログインしているユーザー以外のユーザーを取得
          uids = dbconnect.all_get_other_user(uid)
          #共有しているユーザー一覧を取得
          checked_uids = dbconnect.get_channelmembers(cid,uid)
          return render_template('edit-channel.html',channels=channels,uids=uids,checked_uids=checked_uids)

     
     if request.method=="POST":
          #画像保存
          channel_name = request.form.get('channnel_Name')
          event_date = request.form.get('event_date')         
          url = request.form.get('url')
          uids = request.form.getlist('uids')

          #htmlで入力された情報を取得
          image = request.files['Event_Image']
          image_id = uuid.uuid4()
          image_place = os.path.join("static/user-img",str(image_id)) + ".jpg"
          image.save(image_place) 
          
          #チャンネル情報更新
          dbconnect.edit_channel(cid,channel_name,event_date,url,image_place,uid)
          dbconnect.delete_channelmembers(cid)
          dbconnect.add_channelmembers(uids,cid)
          return redirect('/')
        
#アルバム一覧画面
@app.route('/album/<cid>',methods = ["GET"])
def album(cid):
     #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     albums = dbconnect.get_all_albums(cid)
     return render_template('album.html',albums=albums,cid=cid) 

#アルバム追加画面
@app.route('/create-image/<cid>',methods =["GET","POST"])
def create_image(cid):
     #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     if request.method  == "POST":
          #画像保存
          image = request.files['image']
          if 'image' in request.files['image']:
               flash('ファイルを選択して下さい')
               return render_template('create-image.html')
          image_id = uuid.uuid4()
          image_place = os.path.join("static/user-img",str(image_id)) + ".jpg"
          image.save(image_place)

          #htmlで入力された情報を取得
          created_at = datetime.datetime.now()
          album_title = request.form.get('album_title')
          album_discription = request.form.get('album_discription')
          uid = session.get("uid")
          #画像追加
          dbconnect.add_albums(image_place,created_at,album_title,album_discription,uid,cid)
          albums = dbconnect.get_all_albums(cid)
          return render_template('album.html',albums=albums,cid=cid)     
     return render_template('create-image.html')
  
#メッセージ表示
@app.route('/detail/<cid>')  
def detail(cid):
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     else:
          cid = cid
          channel = dbconnect.get_channel(cid)
          messages = dbconnect.get_all_messages(cid)
          return render_template('detail.html', messages=messages,channel=channel, uid=uid)

#メッセージ投稿
@app.route('/message', methods=['POST'])
def message():
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
                 
     message = request.form.get('message')
     posted_at = datetime.datetime.now()
     print(posted_at)
     cid = request.form.get('cid')

     dbconnect.add_message(message,posted_at,uid,cid)
     return redirect('/detail/{cid}'.format(cid = cid))

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



