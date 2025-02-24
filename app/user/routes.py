from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required
from app.models import Writing, User

user = Blueprint("user", __name__)

@user.route('/user/<int:user_id>')
def userpage(user_id):
    if user_id == current_user.id:
        return redirect(url_for("user.mypage")) # 자신의 유저페이지일 경우 mypage로 이동
    username = User.query.get(user_id).username
    user_posts = Writing.query.filter(Writing.user_id == user_id).all()
    return render_template("user.html", username=username, writings=user_posts)

@login_required
@user.route("/mypage")
def mypage():
    user_id = current_user.id
    username = current_user.username
    my_posts = Writing.query.filter(Writing.user_id == user_id).all()
    return render_template("user.html", username=username, writings=my_posts)
