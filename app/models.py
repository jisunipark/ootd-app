from app import db, login_manager
from flask_login import UserMixin


# User 모델 수정: UserMixin 상속
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    # Flask-Login의 user_loader 사용 시 객체 식별에 사용됨
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User {self.username}>"


# Flask-Login의 사용자 로더 함수 추가
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Writing 모델 (back_populates 추가하여 경고 해결)
class Writing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    weather = db.Column(db.String(50))
    date = db.Column(db.String(10), nullable=False)  # 날짜 (YYYY-MM-DD)
    time = db.Column(db.String(5), nullable=False)  # 시간 (HH:MM)
    content = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    tags = db.Column(db.String(200))

    # ✅ `back_populates`로 관계 명시 (경고 해결)
    comments = db.relationship("Comment", back_populates="writing", lazy=True)

    def __repr__(self):
        return f"<Writing {self.id}>"

    # tags를 리스트로 변환하는 메소드
    def get_tags(self):
        return self.tags.split(",") if self.tags else []

    # tags 리스트를 문자열로 변환하는 메소드
    def set_tags(self, tags_list):
        self.tags = ",".join(tags_list)


# Comment 모델 (back_populates 추가하여 경고 해결)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writing_id = db.Column(db.Integer, db.ForeignKey("writing.id"), nullable=False)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False
    )  # User 모델과의 관계
    content = db.Column(db.Text)

    # `back_populates` 추가하여 경고 해결
    writing = db.relationship("Writing", back_populates="comments", lazy=True)
    user = db.relationship("User", lazy=True)

    def __repr__(self):
        return f"<Comment {self.user.username}>"
