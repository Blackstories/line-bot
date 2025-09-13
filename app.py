from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# ใส่ Channel Access Token จาก LINE Developers Console
CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    for event in data['events']:
        if event['type'] == 'message' and event['message']['type'] == 'text':
            text = event['message']['text']
            reply_token = event['replyToken']
            
            # ส่งคำตอบกลับไปยังผู้ใช้
            reply_message(text, reply_token)
    
    return jsonify({"status": "ok"})

def reply_message(text, reply_token):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": f"คุณพิมพ์ว่า: {text}"}]
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print("Response from LINE:", response.status_code, response.text)
    except Exception as e:
        print("Error sending reply:", e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)