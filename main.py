import asyncio, aiohttp, urllib3, os
from flask import Flask
from threading import Thread
from packet import * # Ensure packet.py is in the same folder

urllib3.disable_warnings()

# --- WEB SERVER (Render keep-alive) ---
app = Flask('')
@app.route('/')
def home(): 
    return "<h1>Guild Glory Bot is Running!</h1>"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# --- BOT LOGIC ---
TARGET_UID = "13613551627" 
BOT_UID = "4394953577" 
BOT_PW = "76A2A700373750BA73DCB8A26CDC056A2C8F8F79AFB3B36F18282B46828311D3"

class GloryBot:
    def __init__(self):
        self.key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
        self.iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
        self.ip = "203.116.201.71" # IND Server IP

    async def Start_Bot(self):
        print("--- BOT INITIALIZING ---")
        while True:
            try:
                print(f"📡 Attempting connection to Garena: {self.ip}")
                # Connection with timeout
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(self.ip, 10008), timeout=15
                )
                print(f"✅ SUCCESS: Bot Connected (UID: {BOT_UID})")
                
                while True:
                    # 1. Invite
                    print(f"📨 ACTION: Inviting {TARGET_UID}...")
                    writer.write(await InvitePlayer(TARGET_UID, self.key, self.iv))
                    await writer.drain()
                    await asyncio.sleep(15) 
                    
                    # 2. Start
                    print("🎮 ACTION: Starting Match...")
                    writer.write(await StartGame(BOT_UID, self.key, self.iv))
                    await writer.drain()
                    await asyncio.sleep(20) 
                    
                    # 3. Exit
                    print("🚪 ACTION: Auto-Exit for Glory...")
                    writer.write(await ExitMatch(self.key, self.iv))
                    await writer.drain()
                    await asyncio.sleep(10)

            except Exception as e:
                print(f"❌ CONNECTION ERROR: {e}. Retrying in 10s...")
                await asyncio.sleep(10)

def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(GloryBot().Start_Bot())

if __name__ == "__main__":
    # Start Bot in background thread
    Thread(target=start_bot_thread).start()
    # Start Flask Web Server
    run_web()
