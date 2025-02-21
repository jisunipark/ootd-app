# Flask 객체 생성
# 애플리케이션 로직 담당

import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, current_app
import requests
from app import db
from app.models import Writing, Comment
from datetime import datetime

# 블루프린트 객체 생성
main = Blueprint('main',__name__)

# 날씨 API 설정
API_KEY = "e1648fab34b6e6bcb4fff4b045d40ba3" # OpenWeatherMap API키(유나계정)
CITY = "Banpobondong,KR"  # 방배동 날씨 조회
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"


# 업로드 디렉토리 설정
UPLOAD_FOLDER = 'app/static/uploads'  # 업로드된 파일을 저장할 폴더
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 허용할 파일 확장자

# 'UPLOAD_FOLDER' 설정을 current_app.config를 사용해서 설정
@main.before_app_request
def setup():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    current_app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 최대 업로드 파일 크기 16MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@main.route("/")
def index(): #메인 페이지 렌더링하는 함수
    weather_info = {}  # 딕셔너리 초기화 (키에러 방지)

    try:
        response = requests.get(URL)
        data = response.json()
        
        # 🔥 터미널에 API 응답 출력 (확인용)
        print("🔥 API 응답 상태 코드:", response.status_code)
        print("🔥 API 응답 데이터:", data)

        if response.status_code == 200 and "main" in data:
            weather_info = {
                "temperature": data["main"].get("temp", "N/A"),
                "humidity": data["main"].get("humidity", "N/A"),
                "wind":data["wind"].get("speed","N/A"),
                "description": data["weather"][0].get("description", "N/A") if "weather" in data else "정보 없음", #날씨 설명(ex.맑음,비,눈..)
                "city": data.get("name", "알 수 없음"),
                "icon" : data["weather"][0].get("icon","N/A") #날씨 아이콘
            }
        else:
            weather_info["error"] = f"❌ API 오류: {data.get('message', '알 수 없음')}"
    except Exception as e:
        weather_info["error"] = f"🚨 API 요청 중 오류 발생: {e}" 

    return render_template("index.html", weather=weather_info)


# 글 작성 라우트
@main.route("/writing", methods=["GET", "POST"])
def writing():
    weather_info = {}  # 날씨 정보를 저장할 딕셔너리

    try:
        response = requests.get(URL)
        data = response.json()

        if response.status_code == 200 and "main" in data:
            weather_info = {
                "temperature": data["main"].get("temp", "N/A"),
                "description": data["weather"][0].get("description", "N/A"),
                "city": data.get("name", "알 수 없음"),
                "icon": data["weather"][0].get("icon", "N/A"),
            }
        else:
            weather_info["error"] = f"❌ API 오류: {data.get('message', '알 수 없음')}"
    except Exception as e:
        weather_info["error"] = f"🚨 API 요청 중 오류 발생: {e}"

    if request.method == "POST":
        # 사용자가 입력한 데이터를 가져옵니다.
        weather = request.form["weather"]
        content = request.form["content"]
        image_url = ""
        tags = request.form.get("tags", "")

        # 이미지 파일 처리
        if 'image_url' in request.files:
            image_file = request.files['image_url']
            if image_file.filename != '' and allowed_file(image_file.filename):
                # 파일 이름을 안전하게 처리하고 저장 경로 설정
                filename = secure_filename(image_file.filename)
                image_url = os.path.join(UPLOAD_FOLDER, filename)
                # 업로드 폴더가 없으면 생성
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                image_file.save(image_url)  # 파일 저장

        # 현재 날짜와 시간을 자동으로 가져옵니다.
        now = datetime.now()
        date = now.strftime('%Y-%m-%d')  # 현재 날짜
        time = now.strftime('%H:%M')  # 현재 시간

        # 새로운 글 객체 생성
        new_writing = Writing(
            weather=weather,
            date=date,
            time=time,
            content=content,
            image_url=image_url,
            tags=tags
        )

        # 데이터베이스에 저장
        db.session.add(new_writing)
        db.session.commit()

        # 저장 후 리다이렉트하여 같은 글을 다시 보여줌
        return redirect(url_for('main.show_writing', writing_id=new_writing.id))

    return render_template("writing.html", writing=None, weather_info=weather_info)

# 작성된 글을 보여주는 라우트
@main.route("/writing/<int:writing_id>")
def show_writing(writing_id):
    writing = Writing.query.get_or_404(writing_id)
    return render_template("writing.html", writing=writing)

# 댓글 추가 라우트
@main.route("/writing/<int:writing_id>/comment", methods=["POST"])
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

    return redirect(url_for('main.show_writing', writing_id=writing.id))
