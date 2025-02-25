import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, logout_user
from flask import request, make_response

# Flask 앱 생성
app = Flask(__name__, template_folder="templates", static_folder="static")

app.secret_key = "my_fixed_secret_key"  # 고정된 시크릿 키 사용

# 데이터베이스 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(BASE_DIR, 'instance/users.db')}?check_same_thread=False"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# DB 초기화
db = SQLAlchemy(app)

# **LoginManager 초기화**
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"  # 로그인 필요 시 이동할 페이지
login_manager.session_protection = "strong"

# **User 로드 함수 추가**
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login: 사용자를 로드하는 함수"""
    return User.query.get(int(user_id))  # 로그인 상태 유지


# **블루프린트 등록**
from app.auth.routes import auth as auth_blueprint
from app.main.routes import main as main_blueprint
from app.user.routes import user as user_blueprint

app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)


# **앱 실행 시마다 데이터베이스 초기화 및 세션, 로그인 상태 초기화**
with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("✅ 데이터베이스가 초기화되었습니다!")

        # **요청 컨텍스트에서 세션 삭제 및 로그인 해제**
        with app.test_request_context():
            # 로그인 상태 해제
            logout_user()

            # 세션 삭제
            session.clear()

            print("✅ 앱 시작 시 세션과 로그인 상태가 초기화되었습니다!")

    except Exception as e:
        print(f"⚠️ 초기화 중 오류 발생: {str(e)}")
