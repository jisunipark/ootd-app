import os
import secrets
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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

# LoginManager 초기화
login_manager = LoginManager(app)
login_manager.login_view = "auth.login"  # 로그인 필요 시 이동할 페이지
login_manager.session_protection = "strong"

# 블루프린트 등록
from app.auth.routes import auth as auth_blueprint
from app.main.routes import main as main_blueprint
from app.user.routes import user as user_blueprint

app.register_blueprint(auth_blueprint, url_prefix="/auth")  # 회원가입/로그인 기능
app.register_blueprint(main_blueprint)  # 메인 페이지 기능
app.register_blueprint(user_blueprint)  # 유저 페이지 기능

# 앱 실행 시마다 데이터베이스 초기화
with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("데이터베이스가 초기화되었습니다!")
    except Exception as e:
        print(f"⚠️ 초기화 중 오류 발생: {str(e)}")
