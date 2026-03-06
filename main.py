import asyncio, aiohttp, urllib3, os
from flask import Flask
from threading import Thread
from packet import *
from cfonts import render

urllib3.disable_warnings()

# --- KEEP ALIVE SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run_web():
    # Render automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- CONFIG ---
TARGET_UID = "13613551627" 
BOT_UID = "4394953577" 
BOT_PW = "76A2A700373750BA73DCB8A26CDC056A2C8F8F79AFB3B36F18282B46828311D3"

class GloryBot:
    def __init__(self):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

    async def Start_Bot(self):
        print(render('RENDER-BOT', colors=['white', 'blue'], align='center'))
        try:
            # India Server Connection
            self.reader, self.writer = await asyncio.open_connection("203.116.201.71", 10008)
            print(f"✅ Bot Connected! UID: {BOT_UID}")
            
            while True:
                await self.writer.write(await SwitchLoneWolf(self.key, self.iv))
                print(f"📨 Inviting {TARGET_UID}...")
                await self.writer.write(await InvitePlayer(TARGET_UID, self.key, self.iv))
                await asyncio.sleep(12) 
                
                print("🎮 Starting...")
                await self.writer.write(await StartGame(BOT_UID, self.key, self.iv))
                await asyncio.sleep(20) 
                
                print("🚪 Exiting Match...")
                await self.writer.write(await ExitMatch(self.key, self.iv))
                await asyncio.sleep(10)
        except Exception as e:
            print(f"Bot Error: {e}")

if __name__ == "__main__":
    keep_alive()
    asyncio.run(GloryBot().Start_Bot())
