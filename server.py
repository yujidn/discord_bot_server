import json
import os
import asyncio
import discord

# BotのトークンとチャンネルIDを設定
TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.none()
intents.message_content = True
intents.guilds = True
client = discord.Client(intents=intents)

# socket通信用の設定
HOST = "localhost"
PORT = 12345

async def post_message(reader, writer):
    while True:
        data = await reader.read(4096)
        if not data:
            break

        print(f'受信データ: {data.decode("utf-8")}')

        data = json.loads(data.decode())
        ch_id = data["id"]
        content = data["data"]
        prefix = data.get("prefix", "")

        content = json.dumps(content, indent=2, ensure_ascii=False)

        channel = client.get_channel(ch_id)
        await channel.send(f"{prefix}\n{txt}")

    writer.close()
    await writer.wait_closed()


async def start_server():
    server = await asyncio.start_server(
        post_message, HOST, PORT
    )

    async with server:
        await server.serve_forever()


# Botが起動したときに実行されるイベント
@client.event
async def on_ready():
    print(f"{client.user} がオンラインです！")
    client.loop.create_task(start_server())


# Botを実行
client.run(TOKEN)
