from pytube import YouTube
import discord

class Song:
    def __init__(self, url):
        self._url = url

        yt = YouTube(url)
        self.title = yt.title

    def get_stream(self):
        yt = YouTube(self._url)
        stream = yt.streams.filter(only_audio=True).first()
        discord_stream = discord.FFmpegPCMAudio(stream.url)
        discord_stream.read()
        return discord_stream
