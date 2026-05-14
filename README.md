# Music Transposer

Aplicação web para estudo musical que permite transpor o tom e ajustar a velocidade de músicas do YouTube.

Desenvolvida para os alunos do Conservatório de MPB de Curitiba.

## Funcionalidades (v1)

- Entrada via link do YouTube
- Transposição de tom em semitons (-12 a +12)
- Ajuste de velocidade (0.5× a 2.0×)
- Player de áudio integrado no browser

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- ffmpeg

### Instalar ffmpeg

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## Instalação

```bash
git clone https://github.com/seu-usuario/music-transposer.git
cd music-transposer
uv sync
```

## Uso

```bash
uv run streamlit run app.py
```

Acesse `http://localhost:8501` no navegador.

## Stack

| Componente | Tecnologia |
|---|---|
| Interface | Streamlit |
| Download de áudio | yt-dlp |
| Processamento de áudio | pedalboard (Spotify) |
| Gerenciamento de ambiente | uv |
