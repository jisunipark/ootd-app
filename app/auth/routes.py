from flask import Blueprint, render_template, request, url_for, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required
from app.models import User
from app import db, app
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
        profile_img_url = '/static/images/default-profile.png'
        bio = f"안녕하세요, {nickname}입니다."

        # 이메일 중복 확인
        if User.query.filter_by(email=email).first():
            return jsonify({"message": "이미 사용 중인 이메일입니다.", "status": "error"}), 400

        new_user = User(name=name, nickname=nickname, username=username, password=password, email=email, gender=gender, profile_img_url=profile_img_url, bio=bio)

        try:
            db.session.add(new_user)
            db.session.commit()

            # 회원가입 완료 시 바로 로그인
            login_user(new_user)

            return jsonify({"message": "회원가입 되었습니다", "redirect": url_for('auth.login'), "status": "success"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"message": f"Error: {str(e)}", "status": "error"}), 500

    return render_template('join.html')


# 로그인
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
                login_user(user)  # ✅ 로그인 처리
                return jsonify({"message": "로그인 성공", "redirect": url_for('main.index'), "status": "success"}), 200
            else:
                return jsonify({"message": "아이디 또는 비밀번호가 잘못되었습니다.", "status": "error"}), 400

        except Exception as e:
            print(f"⚠️ 서버 오류 발생: {str(e)}")
            return jsonify({"message": "서버 오류가 발생했습니다.", "status": "error"}), 500

    return render_template('login.html')


# 로그아웃
@auth.route('/logout')
@login_required
def logout():
    logout_user()  # 로그아웃 처리
    return render_template('logout.html')
