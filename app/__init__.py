import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Flask 앱 생성
app = Flask(__name__, template_folder="templates", static_folder="static")

# 데이터베이스 경로 설정
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance/users.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'

# 데이터베이스 초기화
db = SQLAlchemy(app)

# 블루프린트 등록
from app.auth.routes import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 테이블 자동 생성
with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ 데이터베이스 테이블 생성 완료")
