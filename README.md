# write only discord bot server

discordへの投稿を仲介するためのbot serverです。
socket通信のlistenerを起動し、ほかのプログラムからの通信をもとにdiscordへの投稿を行います。

"rss feederなど" -> [socket connection] -> "bot server" -> [channel id + message] -> "discordへ投稿"

# how to use

```
poetry install
python server.py
```
