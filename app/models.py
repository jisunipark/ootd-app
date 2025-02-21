from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    nickname = db.Column(db.String(50), nullable=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

class Writing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.String(50))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    tags = db.Column(db.String(200))
    
    # 댓글과 관계 설정
    comments = db.relationship('Comment', backref='writing', lazy=True)


    def __repr__(self):
        return f"<Writing {self.id}>"



class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writing_id = db.Column(db.Integer, db.ForeignKey('writing.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # User 모델과의 관계
    content = db.Column(db.Text)
    writing = db.relationship('Writing', backref=db.backref('comments', lazy=True))
    user = db.relationship('User', backref=db.backref('comments', lazy=True))  # User와의 관계

    def __repr__(self):
        return f"<Comment {self.user.username}>"  


