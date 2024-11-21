from flask import Flask,request,redirect,render_template

app = Flask(__name__)

@app.route('/test')
def test():
     return render_template('registration/signup.html')

@app.route('/testa')
def testa():
     return render_template('create-channel.html')

@app.route('/testi')
def testi():
     return render_template('create-image.html')

@app.route('/testu')
def testu():
     return render_template('edit-channel.html')

@app.route('/teste')
def teste():
     return render_template('update-profile.html')

@app.route('/')
def Hello():
     return render_template('index.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)