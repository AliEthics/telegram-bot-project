# main.py
import os
from flask import Flask, request
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")  # set in Render later
if not TELEGRAM_TOKEN:
    raise RuntimeError("Set TELEGRAM_TOKEN environment variable")

API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
app = Flask(__name__)

def send_message(chat_id, text):
    requests.post(f"{API_URL}/sendMessage", json={"chat_id": chat_id, "text": text})

def handle_command(chat_id, text):
    # Safe echo bot
    reply = f"Echo: {text}"
    return reply

@app.route("/", methods=["GET"])
def index():
    return "Bot is running", 200

@app.route(f"/webhook/{TELEGRAM_TOKEN}", methods=["POST"])
def webhook():
    update = request.get_json(force=True)
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")
        reply = handle_command(chat_id, text)
        send_message(chat_id, reply)
    return {"ok": True}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
