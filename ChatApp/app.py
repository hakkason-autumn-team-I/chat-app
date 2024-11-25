from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import datetime
import re
import hashlib
import os
import datetime

app = Flask(__name__)
     
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

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)



