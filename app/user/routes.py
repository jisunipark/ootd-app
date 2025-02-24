from flask import Blueprint, render_template
from flask_login import current_user, login_required
from app.models import Writing, User

user = Blueprint("user", __name__)

@user.route('/user/<int:user_id>')
def user_page(user_id):
    username = User.query.get(user_id).username
    user_posts = Writing.query.filter(Writing.user_id == user_id).all()
    return render_template("user.html", username=username, writings=user_posts)

@login_required
@user.route("/mypage")
def my_page():
    user_id = current_user.id
    username = current_user.username
    my_posts = Writing.query.filter(Writing.user_id == user_id).all()
    return render_template("user.html", username=username, writings=my_posts)

