import tempfile
import os
import streamlit as st
import yt_dlp
from pedalboard import Pedalboard, PitchShift
from pedalboard.io import AudioFile


def is_valid_youtube_url(url: str) -> bool:
    return "youtube.com/watch" in url or "youtu.be/" in url


def download_audio(url: str, tmp_dir: str) -> str:
    yt_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(tmp_dir, "audio.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
        "quiet": True,
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([url])
    return os.path.join(tmp_dir, "audio.wav")


def process_audio(input_path: str, output_path: str, semitones: int) -> None:
    with AudioFile(input_path) as f:
        audio = f.read(f.frames)
        sr = f.samplerate
    board = Pedalboard([PitchShift(semitones=semitones)])
    processed = board(audio, sr)
    with AudioFile(output_path, "w", sr, processed.shape[0]) as f:
        f.write(processed)


if "downloaded_url" not in st.session_state:
    st.session_state.downloaded_url = None
    st.session_state.input_path = None
    st.session_state.tmp_dir = None

st.title("Music Transposer")

url = st.text_input("Link do YouTube")
semitones = st.slider("Semitons", min_value=-12, max_value=12, value=0)

if st.button("Processar"):
    if not url:
        st.error("Cole um link do YouTube antes de processar.")
        st.stop()

    if not is_valid_youtube_url(url):
        st.error("Link inválido. Use um link do YouTube (youtube.com ou youtu.be).")
        st.stop()

    if url != st.session_state.downloaded_url:
        st.session_state.tmp_dir = tempfile.mkdtemp()
        with st.spinner("Baixando áudio..."):
            try:
                st.session_state.input_path = download_audio(url, st.session_state.tmp_dir)
                st.session_state.downloaded_url = url
            except Exception:
                st.error("Não foi possível baixar o vídeo. Verifique se o link está correto e se o vídeo é público.")
                st.stop()

    output_path = os.path.join(st.session_state.tmp_dir, "output.wav")
    with st.spinner("Processando..."):
        try:
            process_audio(st.session_state.input_path, output_path, semitones)
        except Exception:
            st.error("Erro ao processar o áudio. Tente novamente.")
            st.stop()

    st.audio(output_path)
