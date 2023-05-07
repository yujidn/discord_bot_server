import json
import os
import socket

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
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
# クライアントからの接続をリッスン
server_socket.listen(5)


async def post_message():
    while True:
        # クライアントからの接続を受け付ける
        client_socket, _ = server_socket.accept()

        while True:
            # クライアントからのデータを受信
            data = client_socket.recv(4096)
            print(f'受信データ: {data.decode("utf-8")}')

            # データがない場合、接続を閉じる
            if not data:
                break

            # 受信データをデコードして表示
            data = json.loads(data.decode())
            ch_id = data["id"]
            content = data["data"]
            prefix = data.get("prefix", "")

            content = json.dumps(content, indent=2, ensure_ascii=False)

            channel = client.get_channel(ch_id)
            await channel.send(f"{prefix}\n{content}")

        # ソケットを閉じる
        client_socket.close()


# Botが起動したときに実行されるイベント
@client.event
async def on_ready():
    print(f"{client.user} がオンラインです！")
    client.loop.create_task(post_message())


# Botを実行
client.run(TOKEN)
