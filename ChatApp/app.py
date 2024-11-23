#メッセージ表示
@app.route('/detail/<cid>')  
def detail(cid):
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')

     cid = cid
     channel = dbConnect.getChannelById(cid)
     messages = dbConnect.getMessageAll(cid)


     return render_template('detail.html',messages = messages,uid = uid)

#メッセージ投稿
@app.route('/message', methods=['POST'])
def message():
     uid = session.get("uid")
     if uid is None:
          return redirect('/login')
                 
     message = request.form.get('message')
     posted_at = request.form.get ('posted_at')
     cid = request.form.get('cid')

     dbConnect.createMessage(uid, cid, message,posted_at)
     return redirect('/detail/{cid}'.format(cid = cid))

