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
