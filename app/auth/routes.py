from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
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
            return jsonify({"message": "이미 사용 중인 이메일입니다. 다른 이메일을 사용해주세요.", "status": "error"}), 400

        new_user = User(name=name, nickname=nickname, username=username, password=password, email=email, gender=gender)

        try:
            db.session.add(new_user)
            db.session.commit()

            # 회원가입 완료 후 바로 세션에 로그인 정보 저장
            session['user_id'] = new_user.id
            session['username'] = new_user.username

            # 성공 메시지와 로그인 페이지로의 리다이렉트 URL 전달
            return jsonify({"message": "회원가입 되었습니다", "redirect": url_for('auth.login'), "status": "success"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500

    return render_template('join.html')


# routes.py (로그인 라우트 수정)
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter_by(username=username).first()

            if user is None:
                return jsonify({"message": "해당 사용자가 존재하지 않습니다.", "status": "error"}), 400

            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                return jsonify({"message": "로그인 성공", "redirect": url_for('main.index'), "status": "success"}), 200
            else:
                return jsonify({"message": "아이디 또는 비밀번호가 잘못되었습니다.", "status": "error"}), 400

        except Exception as e:
            print(f"⚠️ 서버 오류 발생: {str(e)}")
            return jsonify({"message": "서버 오류가 발생했습니다.", "status": "error"}), 500

    return render_template('login.html')



# 로그아웃
@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return render_template('logout.html')
