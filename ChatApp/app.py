from flask import Flask,request,redirect,render_template

app = Flask(__name__)

@app.route('/test')
def test():
     return render_template('registration/signup.html')

@app.route('/')
def Hello():
     return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=False)