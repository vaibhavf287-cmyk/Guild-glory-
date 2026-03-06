import asyncio, aiohttp, urllib3, os
from flask import Flask
from threading import Thread
from packet import *
from cfonts import render

urllib3.disable_warnings()

# --- WEB SERVER FOR RENDER (Keep Alive) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# --- BOT CONFIGURATION ---
TARGET_UID = "13613551627" 
BOT_UID = "4394953577" 
BOT_PW = "76A2A700373750BA73DCB8A26CDC056A2C8F8F79AFB3B36F18282B46828311D3"

class GloryBot:
    def __init__(self):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        self.writer = None

    async def Get_Token(self):
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        data = {"uid": BOT_UID, "password": BOT_PW, "response_type": "token", "client_type": "2", "client_id": "100067"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                res = await resp.json()
                return res.get("access_token")

    async def Start_Bot(self):
        print(render('RENDER-BOT', colors=['white', 'blue'], align='center'))
        token = await self.Get_Token()
        if not token:
            print("❌ Login Fail!"); return

        try:
            self.reader, self.writer = await asyncio.open_connection("203.116.201.71", 10008)
            print(f"✅ Bot Online: {BOT_UID}")
            
            while True:
                await self.writer.write(await SwitchLoneWolf(self.key, self.iv))
                print(f"📩 Inviting {TARGET_UID}...")
                await self.writer.write(await InvitePlayer(TARGET_UID, self.key, self.iv))
                
                await asyncio.sleep(12) # Wait for you to join
                
                print("🎮 Starting...")
                await self.writer.write(await StartGame(BOT_UID, self.key, self.iv))
                await asyncio.sleep(15) # Match loading
                
                print("🚪 Exiting for Glory...")
                await self.writer.write(await ExitMatch(self.key, self.iv))
                await asyncio.sleep(10) # Return to lobby
        except Exception as e:
            print(f"Error: {e}"); await asyncio.sleep(5)

if __name__ == "__main__":
    keep_alive() # Starts Flask Web Server
    asyncio.run(GloryBot().Start_Bot())
