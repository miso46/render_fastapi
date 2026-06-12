from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel 
import random
from fastapi.responses import HTMLResponse

app = FastAPI()

visitor_count = 0

class PresentRequest(BaseModel):
    present: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}

@app.get("/omikuji")
def omikuji():
    omikuji_list = [
        "大吉", "中吉", "小吉", "吉", "半吉", 
        "末吉", "末小吉", "凶", "小凶", "大凶"
    ]
    return {"result" : random.choice(omikuji_list)}

@app.get("/index")
def index():
    global visitor_count
    visitor_count += 1

    html_content = f"""
    <html>
        <head>
            <title>Omikuji HP</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                    margin-top: 50px;
                }
                button {
                    padding: 10px 20px;
                    font-size: 16px;
                    cursor: pointer;
                }
                form {
                    margin-top: 20px;
                }
                input[type="text"] {
                    padding: 10px;
                    font-size: 16px;
                    width: 300px;
                }
            </style>
        </head>
        <body>
            <h1>ようこそ！</h1>
            <p>訪問回数: <span id="counter">{visitor_count}</span></p>
            <h1>今日の運勢</h1>
            <p>下のボタンを押して、今日の運勢を占いましょう！</p>
            <button onclick="fetch('/omikuji').then(response => response.json()).then(data => alert('今日の運勢は: ' + data.result))">
                今日の運勢を占う
            </button>

            <h2>プレゼントを渡す</h2>
            <p>下のフォームにプレゼントを入力して、ごはんをプレゼントしてください。</p>
            <form onsubmit="event.preventDefault(); const present = document.getElementById('present').value; fetch('/present', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({present})}).then(response => response.json()).then(data => alert(data.response));">
                <input type="text" id="present" name="present" placeholder="プレゼントを入力してください" required>
                <button type="submit">プレゼントを渡す</button>
            </form> </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/present")
async def give_present(data: PresentRequest):
    return {"response": f"サーバは{data.present}をもらいました！<br>ありがとう！"}