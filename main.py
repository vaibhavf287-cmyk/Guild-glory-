import random, aiohttp, asyncio, os, urllib3
from packet import *
from cfonts import render

urllib3.disable_warnings()

# --- CONFIGURATION ---
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

    async def Connect(self):
        try:
            token = await self.Get_Token()
            if not token: return False
            # India Server IP
            self.reader, self.writer = await asyncio.open_connection("203.116.201.71", 10008)
            print(f"✅ Bot Online: {BOT_UID}")
            return True
        except: return False

    async def Send(self, data):
        if self.writer:
            self.writer.write(data)
            await self.writer.drain()

    async def Start_Loop(self):
        print(f"🚀 Glory Farming for {TARGET_UID} Started!")
        while True:
            try:
                await self.Send(await SwitchLoneWolf(self.key, self.iv))
                print("📨 Sending Invite...")
                await self.Send(await InvitePlayer(TARGET_UID, self.key, self.iv))
                
                await asyncio.sleep(10) # 10 sec wait for you to join
                
                print("🎮 Starting Match...")
                await self.Send(await StartGame(BOT_UID, self.key, self.iv))
                
                await asyncio.sleep(12) # Loading time
                
                print("🚪 Auto-Exiting for Glory...")
                await self.Send(await ExitMatch(self.key, self.iv))
                
                await asyncio.sleep(15) # Wait for lobby
            except Exception as e:
                print(f"Error: {e}"); await asyncio.sleep(5)

async def run():
    print(render('GLORY-BOT', colors=['white', 'cyan'], align='center'))
    bot = GloryBot()
    if await bot.Connect():
        await bot.Start_Loop()

if __name__ == "__main__":
    asyncio.run(run())
