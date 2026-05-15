import os
import tempfile
import streamlit as st

from audio.downloader import is_valid_youtube_url, download_audio
from audio.processor import process_audio

YOUTUBE_ENABLED = os.environ.get("YOUTUBE_ENABLED", "true").lower() == "true"

st.set_page_config(page_title="Music Transposer", page_icon="🎸", layout="centered")

if "downloaded_url" not in st.session_state:
    st.session_state.downloaded_url = None
    st.session_state.input_path = None
    st.session_state.tmp_dir = None
    st.session_state.video_title = None

st.title("🎸 Music Transposer")
st.caption("Transponha músicas para estudar em qualquer tom.")
st.divider()

url = None
uploaded_file = None

if YOUTUBE_ENABLED:
    tab_yt, tab_upload = st.tabs(["Link do YouTube", "Upload de arquivo"])
    with tab_yt:
        url = st.text_input("Link do YouTube", placeholder="https://www.youtube.com/watch?v=...")
    with tab_upload:
        uploaded_file = st.file_uploader("Arquivo de áudio", type=["mp3", "wav", "ogg"])
else:
    uploaded_file = st.file_uploader("Arquivo de áudio", type=["mp3", "wav", "ogg"])

semitones = st.slider("Semitons", min_value=-12, max_value=12, value=0)
if semitones == 0:
    st.caption("Tom original")
elif semitones > 0:
    st.caption(f"+{semitones} semitom{'s' if semitones > 1 else ''} acima")
else:
    st.caption(f"{semitones} semitom{'s' if semitones < -1 else ''} abaixo")

st.divider()

if st.button("Processar", type="primary", use_container_width=True):
    if not uploaded_file and not url:
        st.error("Informe um link do YouTube ou faça upload de um arquivo de áudio.")
        st.stop()

    tmp = tempfile.mkdtemp()

    if uploaded_file:
        ext = uploaded_file.name.rsplit(".", 1)[-1]
        input_path = os.path.join(tmp, f"audio.{ext}")
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.session_state.input_path = input_path
        st.session_state.tmp_dir = tmp
        st.session_state.video_title = uploaded_file.name
        st.session_state.downloaded_url = None

    else:
        if not is_valid_youtube_url(url):
            st.error("Link inválido. Use um link do YouTube (youtube.com ou youtu.be).")
            st.stop()

        if url != st.session_state.downloaded_url:
            st.session_state.tmp_dir = tmp
            with st.spinner("Baixando áudio..."):
                try:
                    st.session_state.input_path, st.session_state.video_title = download_audio(url, st.session_state.tmp_dir)
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

    label = f"**{st.session_state.video_title}** — {semitones:+d} semitons" if semitones != 0 else f"**{st.session_state.video_title}** — tom original"
    st.success(label)
    st.audio(output_path)
