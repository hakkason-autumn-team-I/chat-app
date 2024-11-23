from flask import Flask,request,redirect,render_template
from flask import Flask,request,redirect,render_template,flash,session
import uuid
from datetime import timedelta
from models import dbconnect
import re
import hashlib
import os

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def get_all_channels():
     #ユーザーのid取得
     uid = session.get("uid")

     #チャンネル情報取得
     channels = dbconnect.get_all_channels(uid)

     return render_template('index.html',channels=channels)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

