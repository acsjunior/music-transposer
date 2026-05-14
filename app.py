import tempfile
import os
import streamlit as st
import yt_dlp
from pedalboard import Pedalboard, PitchShift
from pedalboard.io import AudioFile

st.title("Music Transposer — PoC")

url = st.text_input("Link do YouTube")
semitones = st.slider("Semitons", min_value=-12, max_value=12, value=0)

if st.button("Processar") and url:
    tmp = tempfile.mkdtemp()
    input_path = os.path.join(tmp, "audio.wav")
    output_path = os.path.join(tmp, "output.wav")

    with st.spinner("Baixando áudio..."):
        yt_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tmp, "audio.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
            "quiet": True,
        }
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([url])

    with st.spinner("Processando..."):
        with AudioFile(input_path) as f:
            audio = f.read(f.frames)
            sr = f.samplerate

        board = Pedalboard([PitchShift(semitones=semitones)])
        processed = board(audio, sr)

        with AudioFile(output_path, "w", sr, processed.shape[0]) as f:
            f.write(processed)

    st.audio(output_path)
