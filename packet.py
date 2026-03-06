from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import asyncio

async def EncryptPacket(HexData, key=None, iv=None):
    DefaultKey = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
    DefaultIv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])
    cipher = AES.new(key if key else DefaultKey, AES.MODE_CBC, iv if iv else DefaultIv)
    return cipher.encrypt(pad(bytes.fromhex(HexData), AES.block_size)).hex()

async def GenPacket(HexData, Header, key, iv):
    EncData = await EncryptPacket(HexData, key, iv)
    Len = hex(len(EncData) // 2)[2:].zfill(8)
    return bytes.fromhex(f"{Header}{Len}{EncData}")

async def SwitchLoneWolf(key, iv):
    return await GenPacket("0801120a12010b182b20012a0801090a0b12191a20", '0519', key, iv)

async def InvitePlayer(PlayerId, key, iv):
    hex_id = hex(int(PlayerId))[2:]
    return await GenPacket(f"0802120b08{hex_id}12024d452001", '0519', key, iv)

async def StartGame(BotUid, key, iv):
    hex_id = hex(int(BotUid))[2:]
    return await GenPacket(f"0801120c08{hex_id}10011801202b", '0519', key, iv)

async def ExitMatch(key, iv):
    return await GenPacket("080312020801", '0519', key, iv)
