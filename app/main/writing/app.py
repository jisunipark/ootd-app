from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    writing = {
        "id": "혜원",
        "weather": "맑음",
        "date": "2025-02-20",
        "time": "14:00",
        "content": "오늘은 정말 좋은 날이에요!",
        "image_url": "https://via.placeholder.com/500",
        "tags": ["OOTD", "Winter", "Cozy"],
        "comments": ["멋져요!", "따뜻해 보이네요!"]
    }
    return render_template("index.html", writing=writing)

if __name__ == "__main__":
    app.run(debug=True)
