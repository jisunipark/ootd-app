from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# 회원가입
@auth.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        name = request.form['name']
        nickname = request.form['nickname']
        username = request.form['username']
        email = request.form['email']
        gender = request.form['gender']
        password = generate_password_hash(request.form['password'])

        # 이메일 중복 확인
        if User.query.filter_by(email=email).first():
            return '이미 사용 중인 이메일입니다. 다른 이메일을 사용해주세요.'

        new_user = User(name=name, nickname=nickname, username=username, password=password, email=email, gender=gender)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            return f"Error: {str(e)}"

    return render_template('join.html')


# 로그인
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user is None:
            return '해당 사용자가 존재하지 않습니다.', 'error'

        if check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect('/')
        else:
            return '아이디 또는 비밀번호가 잘못되었습니다.', 'error'

    return render_template('login.html')


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return render_template('logout.html')