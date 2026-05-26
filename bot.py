import os
import asyncio
from pyrogram import Client, filters
from aiohttp import web

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 7860))

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

async def handle_stream(request):
    chat_id = int(request.match_info.get('chat_id'))
    msg_id = int(request.match_info.get('msg_id'))
    msg = await app.get_messages(chat_id, msg_id)
    
    response = web.StreamResponse(status=200, headers={"Content-Type": "video/mp4", "Accept-Ranges": "bytes"})
    await response.prepare(request)
    async for chunk in app.stream_media(msg, chunk_size=1024 * 1024):
        await response.write(chunk)
    return response

@app.on_message(filters.video | filters.document)
async def start(client, message):
    link = f"https://your-huggingface-space-url/stream/{message.chat.id}/{message.id}"
    await message.reply(f"লিংক: `{link}`")

async def init():
    app_web = web.Application()
    app_web.router.add_get("/stream/{chat_id}/{msg_id}", handle_stream)
    runner = web.AppRunner(app_web)
    await runner.setup()
    await web.TCPSite(runner, "0.0.0.0", PORT).start()
    await app.start()
    print("Bot is ready!")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(init())
