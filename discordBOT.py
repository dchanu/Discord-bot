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

# ==== บอทพร้อมทำงาน ====
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมทำงานแล้ว!")

  #Bot event member join
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1390567025558163569)
    text = f"ยินดีต้อนรับ✨🙌, {member.mention}!"
    await channel.send(text)

# ==== เมื่อมีข้อความส่งมา ====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    prompt = message.content.strip()

    # ส่งไปถาม API แบบ async เพื่อไม่ให้บล็อก
    response = await bot.loop.run_in_executor(None, ask_claude, prompt)

    await message.channel.send(response)
    await bot.process_commands(message)

# === SLASH COMMAND
@bot.tree.command(name="resume", description="ดูเรซูเม่")
async def show_resume(interaction: discord.Interaction):

    embed = discord.Embed(
        title="👨‍💻 My resume",
        description="รวมทักษะและประสบการณ์",
        color=discord.Color.green()
    )

    embed.add_field(name="🛠️ ทักษะ", value="• Python (Expert)\n• Discord Bot\n• AI/ML\n• Web Dev", inline=False)
    embed.add_field(name="📌 ประสบการณ์", value="• Freelance Dev\n• ทำ Dashboard / Bot ให้บริษัท\n• ฝึกงานสาย AI", inline=False)
    embed.set_footer(text="อัปเดตล่าสุด: ก.ค. 2025")

    await interaction.response.send_message(embed=embed, ephemeral=False)


# ==== เริ่มรันบอท ====
keep_alive()
bot.run(DISCORD_TOKEN)
