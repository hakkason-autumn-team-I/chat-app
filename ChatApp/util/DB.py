import pymysql

class DB:
    def getConnection():  #データベースに接続する関数
        try:#エラーハンドリングがしやすくなる
            conn = pymysql.connect(  #pymsqlに接続  ポート番号はデフォルトに３３０６が入る
            host="db",  
            db="chatapp",
            user="testuser",  #sqlに入る時のパスワード
            password="testuser", #sqlに入る時のパスワード
            charset="utf8",  #機械語から人間語の変換するときの形式
            cursorclass=pymysql.cursors.DictCursor #データベースの実行窓口　Dictは辞書型
        )
            return conn
        except (ConnectionError):
            print("コネクションエラーです")
            conn.close()#接続を閉める