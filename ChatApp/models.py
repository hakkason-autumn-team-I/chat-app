from flask import abort
from util.DB import DB
import datetime

class dbconnect:

    #ユーザー作成
    def create_user(uid,name,email,password):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO users (id,user_name,email,password) VALUES (%s, %s, %s, %s);"
            cur.execute(sql,(uid,name,email,password))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()

    #ユーザー取得
    def get_user(email):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM users WHERE email = %s"
            cur.execute(sql,(email))
            user = cur.fetchone()
            return user
        except Exception as e:
            print(f'エラーが発生:{e}')
        finally:
            cur.close()

    #チャンネルを追加
    def create_channel(id,channel_name,event_date,url,image_place,uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO channels (id,channel_name,event_date,url,image_place,uid) VALUES (%s, %s, %s, %s, %s, %s);"
            cur.execute(sql,(id,channel_name,event_date,url,image_place,uid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()

    #チャンネルメンバー追加
    def add_channelmembers(uid_list,cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            for uid in uid_list:
                sql = "INSERT INTO channelmembers (uid,cid) VALUES (%s,%s);"
                cur.execute(sql,(uid,cid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()

    #チャンネルにチェックをつける
    def check_star(uid,cid,star_boolean):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channelmembers set starred = %s WHERE uid = %s AND cid = %s;"
            cur.execute(sql,(star_boolean,uid,cid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
        finally:
            cur.close()

    #チャンネル一覧を取得
    def get_all_channels(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM  channels as ch INNER JOIN channelmembers as ch_member on ch.id = ch_member.cid WHERE ch_member.uid= %s and ch.event_date > %s ORDER BY ch.event_date ASC ;"
            cur.execute(sql,(uid,datetime.datetime.now()))
            user = cur.fetchall()          
            return user
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()

    #チャンネル一覧（終了したイベント）を取得
    def get_finished_channels(uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM  channels as ch INNER JOIN channelmembers as ch_member on ch.id = ch_member.cid WHERE ch_member.uid= %s and ch.event_date < %s ORDER BY ch.event_date ASC ;"
            cur.execute(sql,(uid,datetime.datetime.now()))
            user = cur.fetchall()          
            return user
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()
    
    #チェンネル編集する際にチャンネル情報を取得
    def get_channel(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * FROM  channels where id=%s;"
            cur.execute(sql,(cid))
            Ch = cur.fetchone()         
            return Ch
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()
    
    #チャンネル編集でチャンネル内容を変更
    def edit_channel(cid,channel_name,event_date,url,image_place,uid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "UPDATE channels set channel_name = %s,event_date = %s,url = %s,image_place = %s Where id =  %s and uid = %s;"
            cur.execute(sql,(channel_name,event_date,url,image_place,cid,uid))
            conn.commit()           
        except Exception as e:
            print(f"エラーが発生:{e}")
        finally:
            cur.close()

    #指定したチェンネルのメッセージを取得
    def get_all_messages(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "SELECT * from messages INNER JOIN users on messages.uid = users.id WHERE messages.cid = %s ORDER BY posted_at ASC;"
            cur.execute(sql,(cid))
            message = cur.fetchall()
            return message
        except Exception as e:
               print(f"エラエラーが発生ーが発生してます:{e}")
        finally:
            cur.close()

    #チャンネルにチャット欄にメッセージを取得
    def add_message(message,posted_at,uid,cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = "INSERT INTO messages (message,posted_at,uid,cid) VALUES (%s, %s, %s, %s);"
            cur.execute(sql,(message,posted_at,uid,cid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()

    #指定したチャンネルのアルバムを取得
    def get_all_albums(cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'SELECT * FROM albums WHERE cid = %s;'
            cur.execute(sql,(cid))
            all_albums = cur.fetchall()
            return all_albums
        except Exception as e:
            print(f'エラーが発生:{e}')
            abort(500)
        finally:
            cur.close()
            
    #指定したチャンネルのアルバム内容を追加
    def add_albums(album_place,created_at,album_title,album_discription,uid,cid):
        try:
            conn = DB.getConnection()
            cur = conn.cursor()
            sql = 'INSERT INTO albums (album_place,created_at,album_title,album_discription,uid,cid) VALUES (%s,%s,%s,%s,%s,%s);'
            cur.execute(sql,(album_place,created_at,album_title,album_discription,uid,cid))
            conn.commit()
        except Exception as e:
            print(f'エラーが発生:{e}')
        finally:
            cur.close()
    



    
    


