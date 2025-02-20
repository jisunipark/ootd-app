from flask import request, redirect, url_for

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    new_comment = Comment(content=content, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('view_post', post_id=post.id))
