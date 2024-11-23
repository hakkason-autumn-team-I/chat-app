from flask import Flask,request,redirect,render_template
from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import re
import hashlib
import os

app = Flask(__name__)

@app.route('/create-channel',methods=['GET','POST'])
def create_channel():
     uid = session.get("uid")
     if request.method == 'POST':
          #チェンネルのidを生成
          cid = uuid.uuid4()

          #htmlで入力された情報を取得
          channel_name = request.form.get('channnel_Name')
          event_date = request.form.get('event_date')         
          url = request.form.get('url')         
          uids = request.form.getlist('uids')

          #画像保存
          image = request.files['Event_Image']
          image_id = uuid.uuid4()
          image_place = os.path.join("static/user-img",str(image_id)) + ".jpg"
          image.save(image_place)

          #チャンネル情報追加
          dbconnect.create_channel(cid,channel_name,event_date,url,image_place,uid)
          dbconnect.add_channelmembers(uids,cid)

          return redirect('/')
     
     #ログインしているユーザー以外のユーザーを取得
     uids = dbconnect.all_get_other_user(uid)

     return render_template('create-channel.html',uids=uids)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

