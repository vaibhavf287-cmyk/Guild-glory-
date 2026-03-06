import asyncio, aiohttp, urllib3, os
from flask import Flask
from threading import Thread
from packet import *

urllib3.disable_warnings()

app = Flask('')
@app.route('/')
def home(): return "Bot is Online and Active!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
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
        # India Server list
        self.ips = ["203.116.201.71", "103.213.236.141", "203.116.201.12"]

    async def Start_Bot(self):
        print("🚀 Glory Bot starting...")
        while True:
            for ip in self.ips:
                try:
                    print(f"📡 Trying to connect to {ip}...")
                    # Connection with timeout to avoid long hanging
                    self.reader, self.writer = await asyncio.wait_for(
                        asyncio.open_connection(ip, 10008), timeout=10
                    )
                    print(f"✅ Bot Connected Successfully to {ip}!")
                    
                    while True:
                        # 1. Switch Mode
                        self.writer.write(await SwitchLoneWolf(self.key, self.iv))
                        await self.writer.drain()
                        
                        # 2. Invite
                        print(f"📨 Inviting {TARGET_UID}...")
                        self.writer.write(await InvitePlayer(TARGET_UID, self.key, self.iv))
                        await self.writer.drain()
                        
                        await asyncio.sleep(15)
                        
                        # 3. Start
                        print("🎮 Starting Match...")
                        self.writer.write(await StartGame(BOT_UID, self.key, self.iv))
                        await self.writer.drain()
                        
                        await asyncio.sleep(20)
                        
                        # 4. Exit
                        print("🚪 Exiting for Glory...")
                        self.writer.write(await ExitMatch(self.key, self.iv))
                        await self.writer.drain()
                        
                        await asyncio.sleep(10)
                        
                except Exception as e:
                    print(f"❌ Connection failed on {ip}: {e}")
                    await asyncio.sleep(5)
                    continue # Try next IP

if __name__ == "__main__":
    keep_alive()
    asyncio.run(GloryBot().Start_Bot())
