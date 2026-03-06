import random, aiohttp, ssl, asyncio, os, urllib3
from packet import *
from cfonts import render
from datetime import datetime

urllib3.disable_warnings()

# --- CONFIGURATION (YOUR DATA) ---
TARGET_UID = "13613551627" 
BOT_UID = "4394953577" 
BOT_PW = "76A2A700373750BA73DCB8A26CDC056A2C8F8F79AFB3B36F18282B46828311D3"
# ---------------------------------

class GuildGloryBot:
    def __init__(self):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        self.writer = None

    async def Get_Access(self):
        print("🔑 Getting Access Token from Garena...")
        url = "https://100067.connect.garena.com/oauth/guest/token/grant"
        data = {"uid": BOT_UID, "password": BOT_PW, "response_type": "token", "client_type": "2", "client_id": "100067"}
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=data) as resp:
                result = await resp.json()
                return result.get("access_token")

    async def Connect(self):
        try:
            token = await self.Get_Access()
            if not token: 
                print("❌ Token Error! Check BOT_PW."); return False
            
            # Note: Reality mein humein MajorLogin se IP milta hai
            # Ye IND Server ka static IP hai
            ip, port = "203.116.201.71", 10008 
            self.reader, self.writer = await asyncio.open_connection(ip, port)
            print(f"✅ Bot Online! UID: {BOT_UID}")
            return True
        except Exception as e:
            print(f"❌ Connection Failed: {e}"); return False

    async def Send(self, data):
        if self.writer:
            self.writer.write(data)
            await self.writer.drain()

    async def Run_Bot(self):
        print(f"🎯 Target Player: {TARGET_UID}")
        while True:
            try:
                # 1. Ensure mode is Lone Wolf
                await self.Send(await SwitchLoneWolf(self.key, self.iv))
                await asyncio.sleep(1)

                # 2. Invite You
                print(f"📩 Sending Invite to {TARGET_UID}...")
                await self.Send(await InvitePlayer(TARGET_UID, self.key, self.iv))
                
                # 3. Wait for you to join group
                await asyncio.sleep(10) 
                
                # 4. Start Game
                print("🎮 Starting Match...")
                await self.Send(await StartGame(BOT_UID, self.key, self.iv))
                
                # 5. Wait for Glory (Zone death/Exit)
                print("⏳ Match in progress... Waiting 40s")
                await asyncio.sleep(40) 
                
            except Exception as e:
                print(f"⚠️ Error: {e}"); await asyncio.sleep(5)

async def start_service():
    os.system('clear')
    print(render('GLORY-BOT', colors=['white', 'blue'], align='center'))
    bot = GuildGloryBot()
    if await bot.Connect():
        await bot.Run_Bot()

if __name__ == "__main__":
    asyncio.run(start_service())
