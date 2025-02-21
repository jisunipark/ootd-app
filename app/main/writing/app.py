import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# SQLite 데이터베이스 설정 (db.sqlite3라는 파일로 저장)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

# Writing 모델 정의
class Writing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    weather = db.Column(db.String(50))
    date = db.Column(db.String(20))
    time = db.Column(db.String(20))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    tags = db.Column(db.String(200))
    comments = db.Column(db.Text)

    def __repr__(self):
        return f"<Writing {self.id}>"

# Comment 모델 정의   
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    writing_id = db.Column(db.Integer, db.ForeignKey('writing.id'), nullable=False)
    content = db.Column(db.Text)
    writing = db.relationship('Writing', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"<Comment {self.id}>"



# 데이터베이스 초기화
with app.app_context():
    db.create_all()    # 테이블을 생성

@app.route("/writing", methods=["GET", "POST"])
def writing():
    if request.method == "POST":
        # 사용자가 입력한 데이터를 가져옵니다.
        new_writing = Writing(
            weather=request.form["weather"],
            date=request.form["date"],
            time=request.form["time"],
            content=request.form["content"],
            image_url=request.form.get("image_url", ""),
            tags=request.form.get("tags", "")
        )
        
        
        # 데이터베이스에 저장
        db.session.add(new_writing)
        db.session.commit()

        # 저장 후 리다이렉트하여 같은 글을 다시 보여줌
        return redirect(url_for('show_writing', writing_id=new_writing.id))

    return render_template("writing.html", writing=None)

# 작성된 글을 보여주는 라우트
@app.route("/writing/<int:writing_id>")
def show_writing(writing_id):
    writing = Writing.query.get_or_404(writing_id)
    return render_template("writing.html", writing=writing)

# 댓글 추가 라우트
@app.route("/writing/<int:writing_id>/comment", methods=["POST"])
def add_comment(writing_id):
    writing = Writing.query.get_or_404(writing_id)
    comment_content = request.form['content']
    
    # 새로운 댓글을 Comment 테이블에 추가
    new_comment = Comment(
        writing_id=writing.id,
        content=comment_content
    )
    
    # 댓글을 데이터베이스에 저장
    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('show_writing', writing_id=writing.id))

# 플라스트 앱 직접 실행
if __name__ == "__main__":
    app.run(debug=True)

