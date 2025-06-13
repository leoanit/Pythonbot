import os
import requests
import time
import hmac
import hashlib
import json
from datetime import datetime
from threading import Thread
from flask import Flask

# === CONFIG ===
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CHECK_INTERVAL = 10  # seconds

# === MESSAGES ===
WELCOME_MESSAGE = "Hello! 👋 Thanks for choosing to trade with me."
BANK_DETAILS = """Please send payment to:
🏦 Bank: Equity Bank
👤 Name: Maureen Beauttah
💳 Acc No: 1234567890"""

# === HMAC SIGNATURE ===
def sign_request(secret, method, path, timestamp, body=''):
    message = f'{timestamp}{method}{path}{body}'
    return hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()

# === API CALL WRAPPER ===
def call_api(method, path, body_dict=None):
    url = f'https://api.noones.com{path}'
    timestamp = str(int(time.time()))
    body = json.dumps(body_dict) if body_dict else ''
    signature = sign_request(API_SECRET, method.upper(), path, timestamp, body)

    headers = {
        'API-Key': API_KEY,
        'API-Sign': signature,
        'API-Timestamp': timestamp,
        'Content-Type': 'application/json'
    }

    response = requests.request(method, url, headers=headers, data=body)
    return response.json()

# === TELEGRAM NOTIFY ===
def notify_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {'chat_id': TELEGRAM_CHAT_ID, 'text': msg}
    requests.post(url, data=data)

# === MESSAGE TO TRADE ===
def send_message(trade_id, message):
    path = f"/api/v1/trades/{trade_id}/message"
    call_api('POST', path, {"message": message})
    print(f"[{datetime.now()}] Sent to {trade_id}: {message[:30]}...")

# === MAIN BOT LOOP ===
seen_trades = set()

def auto_trade_bot():
    print("🚀 Bot started. Monitoring for new trades...")
    while True:
        try:
            trades = call_api('GET', '/api/v1/trades')
            for trade in trades.get('data', []):
                trade_id = trade['trade_id']
                status = trade['status']
                buyer = trade['buyer']['username']

                if status == 'ACTIVE' and trade_id not in seen_trades:
                    print(f"[{datetime.now()}] 🔔 New trade from {buyer} (ID: {trade_id})")
                    send_message(trade_id, WELCOME_MESSAGE)
                    send_message(trade_id, BANK_DETAILS)
                    notify_telegram(f"📥 New trade opened by @{buyer}\nTrade ID: {trade_id}")
                    seen_trades.add(trade_id)

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(CHECK_INTERVAL)

# === FLASK APP ===
app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Noones Bot is running."

# === START EVERYTHING ===
if __name__ == '__main__':
    Thread(target=auto_trade_bot).start()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))