# Flask 객체 생성
# 애플리케이션 로직 담당

from flask import Blueprint, render_template
import requests

# 블루프린트 객체 생성
main = Blueprint('main',__name__)

# 날씨 API 설정
API_KEY = "e1648fab34b6e6bcb4fff4b045d40ba3" # OpenWeatherMap API키(유나계정)
CITY = "Banpobondong,KR"  # 방배동 날씨 조회
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=kr"

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

