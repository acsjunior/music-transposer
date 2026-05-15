# Music Transposer

Aplicação web para estudo musical que permite transpor o tom de músicas para praticar em qualquer tonalidade.

Desenvolvida para os alunos do Conservatório de MPB de Curitiba.

## Funcionalidades (v1)

- Entrada via link do YouTube ou upload de arquivo (MP3, WAV, OGG)
- Transposição de tom em semitons (-12 a +12)
- Player de áudio integrado no browser

## Modos de uso

O comportamento do app é controlado pela variável de ambiente `YOUTUBE_ENABLED`:

| Valor | Comportamento |
|---|---|
| `true` (padrão) | Exibe aba de link do YouTube e aba de upload de arquivo |
| `false` | Exibe apenas upload de arquivo |

### Uso local (YouTube + upload)

```bash
uv run streamlit run app.py
```

### Uso local somente com upload

```bash
YOUTUBE_ENABLED=false uv run streamlit run app.py
```

### Produção (Streamlit Cloud)

Defina `YOUTUBE_ENABLED = "false"` em **Settings → Secrets** no painel do Streamlit Cloud.

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
git clone https://github.com/acsjunior/music-transposer.git
cd music-transposer
uv sync
```

## Stack

| Componente | Tecnologia |
|---|---|
| Interface | Streamlit |
| Download de áudio | yt-dlp |
| Processamento de áudio | pedalboard (Spotify) |
| Gerenciamento de ambiente | uv |
