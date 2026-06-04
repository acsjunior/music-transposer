import os
import yt_dlp


def is_valid_youtube_url(url: str) -> bool:
    return "youtube.com/watch" in url or "youtu.be/" in url


def download_audio(url: str, tmp_dir: str) -> tuple[str, str]:
    yt_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmp_dir, "audio.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "quiet": True,
        "noplaylist": True,
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "")
    return os.path.join(tmp_dir, "audio.wav"), title
