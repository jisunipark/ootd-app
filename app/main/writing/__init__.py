from flask import Flask, render_template
from models import db, Post, Comment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)  # 게시글 ID로 찾기
    return render_template('view_post.html', post=post)
