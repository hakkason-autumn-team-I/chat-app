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

