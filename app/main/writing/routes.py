from flask import request, redirect, url_for

@app.route('/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form['content']
    new_comment = Comment(content=content, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('view_post', post_id=post.id))


@app.route('/post/<int:post_id>/tag', methods=['POST'])
def add_tag(post_id):
    # 태그 값 가져오기
    tag = request.form['tag']
    
    # 해당 게시글을 데이터베이스에서 찾기
    post = Post.query.get(post_id)
    
    # 게시글에 태그 추가 (예시: 태그 리스트에 추가)
    if tag:
        post.tags.append(tag)  # 'tags'는 게시글과 연결된 태그 리스트
    
    # 데이터베이스 저장
    db.session.commit()
    
    # 게시글 상세 페이지로 리다이렉트
    return redirect(url_for('view_post', post_id=post.id))





from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

# 예시 데이터
posts = [
    {
        'id': 1,
        'content': '오늘의 OOTD!',
        'image_url': 'image.jpg',
        'tags': ['패션', '봄', 'OOTD'],
        'comments': ['멋져요!', '좋은 아이템이네요!']
    }
]

@app.route('/post/<int:post_id>/tag', methods=['POST'])
def add_tag(post_id):
    new_tag = request.form['tag']
    # 해당 게시글에 태그 추가
    post = next((p for p in posts if p['id'] == post_id), None)
    if post:
        post['tags'].append(new_tag)
    return redirect(url_for('view_post', post_id=post_id))

@app.route('/post/<int:post_id>')
def view_post(post_id):
    post = next((p for p in posts if p['id'] == post_id), None)
    return render_template('view_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)
