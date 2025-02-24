import os
import secrets  # 👈 랜덤 시크릿 키를 생성하는 모듈
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask 앱 생성
app = Flask(__name__, template_folder="templates", static_folder="static")

# ✅ **앱 시작 시마다 secret_key를 새로 생성 (세션 초기화 효과)**
app.secret_key = secrets.token_hex(16)  # 16바이트 랜덤 문자열 (32자)

# 데이터베이스 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance/users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB 초기화
db = SQLAlchemy(app)

# 블루프린트 등록
from app.auth.routes import auth as auth_blueprint
from app.main.routes import main as main_blueprint

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(main_blueprint)

# ✅ **앱 실행 시마다 데이터베이스 초기화**
with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        print("✅ 데이터베이스가 초기화되었습니다!")
    except Exception as e:
        print(f"⚠️ 초기화 중 오류 발생: {str(e)}")
