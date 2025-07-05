import discord
from discord.ext import commands
import requests
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
import os

# ==== Flask เพื่อป้องกัน Replit หลับ ====
app = Flask('')
@app.route('/')
def home():
    return "บอทยังออนไลน์อยู่"
def run():
    app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

# ==== TOKEN ====
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ==== INTENTS สำหรับให้บอทอ่านข้อความ ====
intents = discord.Intents.all()
intents.message_content = True

# ==== สร้างบอท ====
bot = commands.Bot(command_prefix="!", intents=intents)

# ==== ยิง API ไปหา Claude 3 Haiku บน OpenRouter ====
def ask_claude(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "anthropic/claude-3-haiku:beta",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"
