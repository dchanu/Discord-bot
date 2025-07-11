import discord
from discord.ext import commands
import requests
from flask import Flask
from threading import Thread

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

DISCORD_TOKEN = ('') # <<-- ใส่ Token Discord ตรงนี้
OPENROUTER_API_KEY = ("") # <<-- ใส่ API ของคุณตรงนี้ เช่น OPENROUTER หรือ OpenAI
print("TOKEN:", DISCORD_TOKEN)
print("API:", OPENROUTER_API_KEY)


# ==== INTENTS สำหรับให้บอทอ่านข้อความ ====
intents = discord.Intents.all()
intents.message_content = True

# ==== สร้างบอท ====
bot = commands.Bot(command_prefix="/", intents=intents)

chat_history = {}

def ask_claude(Message_From_User, user_id):
    # ดึงประวัติเดิมของผู้ใช้ หรือเริ่มใหม่ถ้ายังไม่มี
    history = chat_history.get(user_id, [])
    history.append({"role": "user", "content": Message_From_User})

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "anthropic/claude-3-haiku:beta",
        "messages": history,  # <<-- ส่งประวัติให้โมเดลจำ
        "max_tokens": 1000
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            answer = result["choices"][0]["message"]["content"]

            # เพิ่มคำตอบของ Claude ลงใน history
            history.append({"role": "assistant", "content": answer})

            # เก็บไว้ในตัวแปร global โดยเก็บแค่บทสนทนา 10 อันล่าสุด
            chat_history[user_id] = history[-10:]

            return answer
        else:
            return f"❌ Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"

# ==== บอทพร้อมทำงาน ====
@bot.event
async def on_ready():
    print(f"✅ บอท {bot.user} พร้อมทำงานแล้ว!")
    channel_id = 1390567025558163569 # <<-- ใส่ไอดีห้องแชทของ Discord ที่ต้องการใช้บอทส่งข้อความไป
    channel = bot.get_channel(channel_id)
    embed = discord.Embed(
        title="👋 ยินดีต้อนรับสู่เซิร์ฟเวอร์!",
        description="คำแนะนำเบื้องต้นสำหรับใช้งานบอท 🤖\n")
    embed.add_field(name="🔧 ฟีเจอร์ของบอท", value="• ตอบคำถามด้วย AI\n• มี Slash Commands ให้พิมพ์ / เพื่อดูคำสั่งลัด \n• พิมพ์ !reset เพื่อล้างความจำ", inline=False)
    embed.add_field(name="📎 ลิงก์สำคัญ", value="[GitHub](https://github.com/dchanu)", inline=False)
    embed.set_footer(text="บอทโดย Charlotte ✨")
    await channel.send(embed=embed)

  #Bot event member join
@bot.event
async def on_member_join(member):
    channel = bot.get_channel(1390567025558163569) # <<-- ใส่ไอดีห้องแชทของ Discord ที่ต้องการใช้บอทส่งข้อความไป
    text = f"ยินดีต้อนรับ✨🙌, {member.mention}!"
    await channel.send(text)

   #Bot event member left
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(1390567025558163569) # <<-- ใส่ไอดีห้องแชทของ Discord ที่ต้องการใช้บอทส่งข้อความไป
    text = f"{member.mention} ออกจากห้อง!"
    await channel.send(text)

# ==== เมื่อมีข้อความส่งมา ====
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    user_id = str(message.author.id)
    Message_From_User = message.content.strip()
    if Message_From_User == "!reset":
        chat_history.pop(user_id, None)
        await message.channel.send("🧠 ความจำถูกรีเซ็ตแล้ว!")
    else:
        response = await bot.loop.run_in_executor(None, ask_claude, Message_From_User, user_id)
        await message.channel.send(response)
        
    # ส่งไปถาม API แบบ async เพื่อไม่ให้บล็อก
    await bot.process_commands(message)

# === SLASH COMMAND
@bot.tree.command(name="resume", description="ดูเรซูเม่ของ Chanuphap")
async def show_resume(interaction: discord.Interaction):

    embed = discord.Embed(
        title="👨‍💻 My resume",
        description="รวมทักษะและประสบการณ์",
        color=discord.Color.green()
    )
    embed.add_field(name="🛠️ ทักษะ", value="• Python, C, C++\n• Numpy, pandas\n", inline=False)
    embed.add_field(name="📌 ประสบการณ์", value="• ทำ Discord bot \n • ทำ Line bot ", inline=False)
    embed.add_field(name="🎓 การศึกษา", value="• มหาวิทยาลัยรามคำแหง\n คณะวิทยาการณ์คอมพิวเตอร์ (กำลังศึกษาชั้นปี 1)", inline=False)
    embed.add_field(name="📎 Link เรซูเม่", value="[GitHub](https://github.com/dchanu)", inline=False)
    embed.set_image(url="https://i.postimg.cc/mgqHmgxz/Chanuphap-Raisungnoen.png")
    embed.set_footer(text="อัปเดตล่าสุด: ก.ค. 2025")
    await interaction.response.send_message(embed=embed, ephemeral=False)


# ==== เริ่มรันบอท ====
keep_alive()
bot.run(DISCORD_TOKEN)
