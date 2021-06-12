from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, url_for, render_template, request, redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    userID = db.Column(db.String(80), unique = True)
    password = db.Column(db.String(80))

    def __init__(self, userID, password):
        self.userID = userID
        self.password = password

#홈
@app.route('/', methods=['POST','GET'])
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            return render_template('list.html')
        return render_template('list.html')

#로그인
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        userid = request.form['userID']
        passw = request.form['password']
        try:
            data = User.query.filter_by(userID = userid, password = passw).first()
            if data is not None:
                session['logged_in'] = True
                return render_template("list.html", name = userid )#redirect(url_for('list_page'))
            elif passw != User.query.filter_by(password = passw).first() or userid != User.query.filter_by(userID = userid).first():
                return "<script text='text/javascript'>alert('아이디 / 비밀번호를 확인해주세요'); history.back();</script>"
        except:
            return "<script text='text/javascript'>alert('오류가 발생했습니다. 다시 로그인'); history.back();</script>"

#회원가입
@app.route('/sign_up/', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        new_user = User(userID=request.form['userID'], password=request.form['password'])
        db.session.add(new_user)
        db.session.commit()
        return render_template('login.html')
    return render_template('sign_up.html')

#로그아웃
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

#리스트 페이지
@app.route('/list')
def list_page():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            return render_template('list.html')
        return render_template('list.html')

#게시물 추가
@app.route('/addPost', methods=['POST','GET'])
def add_post():
    if request.method == 'POST':
        return render_template('add_post.html')

@app.route('/uploader', methods=['POST','GET'])
def uploader():
    if request.method == 'POST':
        return redirect(url_for(list_page))

if __name__ == '__main__':
    db.create_all()
    app.secret_key = "123123"
    app.run(debug=True)