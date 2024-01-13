from pytube import YouTube
import discord

class Song:
    def __init__(self, url):
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()

        self.title = yt.title
        self.source = discord.FFmpegPCMAudio(audio_stream.url)
