import random, aiohttp, ssl, time, os, urllib3, asyncio, json
from packet import *
from cfonts import render
from datetime import datetime
import traceback

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- FIXED CONFIGURATION FOR GITHUB ---
TARGET_UID = "13613551627" 
BOT_UID = '4394953577'
BOT_PW = '76A2A700373750BA73DCB8A26CDC056A2C8F8F79AFB3B36F18282B46828311D3'
# ---------------------------------------

LoginUrl, ReleaseVersion, version, Version = "https://loginbp.ggpolarbear.com", "OB51", "1.118.1", "2019118695"
Hr = {'Connection': "Keep-Alive", 'Content-Type': "application/x-www-form-urlencoded", 'ReleaseVersion': ReleaseVersion}

async def GeNeRaTeAccEss(Uid, Password):
    url = "https://100067.connect.garena.com/oauth/guest/token/grant"
    data = {"uid": Uid, "password": Password, "response_type": "token", "client_type": "2", "client_id": "100067"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            if response.status != 200: return None, None
            res = await response.json()
            return res.get("open_id"), res.get("access_token")

async def MajorLogin(Payload):
    url = f"{LoginUrl}/MajorLogin"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=Payload, headers=Hr, ssl=False) as response:
            return await response.read() if response.status == 200 else None

class FF_CLIENT:
    def __init__(self):
        self.key = None
        self.iv = None
        self.InvitePlayerId = TARGET_UID
        self.StatusData = None
        self.online_writer = None

    async def SendPacket(self, Packet):
        if self.online_writer:
            self.online_writer.write(Packet)
            await self.online_writer.drain()

    async def SlwdLoop(self):
        print(f"🚀 Starting Glory Loop for {self.InvitePlayerId}")
        while True:
            try:
                # 1. Lone Wolf Switch
                await self.SendPacket(await SwitchLoneWolf(self.key, self.iv))
                await asyncio.sleep(2)
                
                # 2. Invite Player
                print("📩 Sending Invite...")
                await self.SendPacket(await InvitePlayer(self.InvitePlayerId, self.key, self.iv))
                await asyncio.sleep(10) # Wait for accept
                
                # 3. Start Match
                print("🎮 Match Starting...")
                await self.SendPacket(await StartGame(BOT_UID, self.key, self.iv))
                
                # 4. Auto-Exit Logic for Glory
                await asyncio.sleep(15)
                print("🚪 Exiting for Glory...")
                await self.SendPacket(await LeaveTeam(BOT_UID, self.key, self.iv))
                
                await asyncio.sleep(10)
            except Exception as e:
                print(f"Loop Error: {e}"); await asyncio.sleep(5)

    async def Main(self):
        print(render('GLORY-BOT', colors=['white', 'red'], align='center'))
        open_id, access_token = await GeNeRaTeAccEss(BOT_UID, BOT_PW)
        if not open_id: print("❌ Invalid Bot Token!"); return

        # Simplified login for GitHub Actions
        # Note: In a real scenario, you'd need the full protobuf encryption here
        print(f"✅ Bot Online. Target: {self.InvitePlayerId}")
        await self.SlwdLoop()

async def Starting():
    client = FF_CLIENT()
    while True:
        try:
            await client.Main()
        except Exception as e:
            print(f"Restarting due to: {e}")
            await asyncio.sleep(5)

if __name__ == '__main__':
    asyncio.run(Starting())
