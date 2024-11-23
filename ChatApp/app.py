from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import datetime
import re
import hashlib
import os

app = Flask(__name__)

@app.route('/album/<cid>',methods = ["GET"])
def album(cid):
    #ユーザーのid取得
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
     
     albums = dbconnect.get_all_albums(cid)

     return render_template('album.html',albums=albums,cid=cid) 

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

