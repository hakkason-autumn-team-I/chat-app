from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import datetime
import re
import hashlib
import os

app = Flask(__name__)

@app.route("/edit-channel/<cid>",methods=["GET","POST"])
def update_channel(cid):

     if request.method=="GET":
          #チャンネル情報を取得
          channels= dbconnect.get_channel(cid)
     	#ログインしているユーザー以外のユーザーを取得
          uids = dbconnect.all_get_other_user(uid)

          return render_template('edit_channel.html',channels=channels,uids=uids)
     
     if request.method=="POST":
          #画像保存
          channel_name = request.form.get('channnel_Name')
          event_date = request.form.get('event_date')         
          url = request.form.get('url')
          uid = session.get("uid")
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

