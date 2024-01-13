from pytube import YouTube
import discord


def get_url_audio_source(url: str):
    yt = YouTube(url)

    audio_stream = yt.streams.filter(only_audio=True).first()
    source = discord.FFmpegPCMAudio(audio_stream.url)

    return source