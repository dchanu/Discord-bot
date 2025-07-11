# 🤖 Discord Bot Project

บอท Discord เขียนด้วย Python ใช้งานง่าย ปรับแต่งได้ตามใจ!

## 🚀 ฟีเจอร์
- ส่งข้อความอัตโนมัติ
- รองรับคำสั่ง custom
- ปรับแต่งได้ตามต้องการ
- ใช้ Discord API ผ่าน `discord.py`
- เขียนโค้ดสะอาด เข้าใจง่าย

## 📦 ติดตั้ง
### 1. Clone โปรเจกต์
```bash
git clone https://github.com/dchanu/Discord-bot.git
cd Discord-bot

(โครงสร้างของ File)
Discord-bot/
├── main.py
├── README.md
└── requirements.txt
ถ้าไฟล์ requirements.txt ไม่สามารถใช้งานได้ ให้ติดตั้ง Dependencies ตามที่ระบุด้านล่าง
discord.py
requests
Flask
ใช้คำสั่ง pip install เช่น
pip install discord.py requests Flask

### 2. การตั้งค่า Token ของ Discord และ API จากโมเดล AI ที่ต้องการ
2.1 Discord token
- ไปที่ discord developer (เข้าสู่ระบบของท่านก่อน)
- ไปที่ application
- กด New application มุมขวาบน
- ไปที่เมนู Bot เพื่อรับโทเคน ถ้าไม่มี Token ปรากฏ ให้กดปุ่ม Reset token
หมายเหตุ ** ถ้าต้องการใช้โมเดล AI กับบอทให้ไปต่อข้อ 2.2
2.2 API ของโมเดล AI หรือบอทที่ท่านต้องการ (ในตัวอย่างเช่น Openrouter)
- ไปที่เว็บไซต์ Openrouter (ล็อคอินให้เรียบร้อย)
- คลิกโปรไฟล์มุมขวาบน กดที่ Keys เพื่อสร้าง Keys
