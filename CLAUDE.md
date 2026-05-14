# Music Transposer — Guia para o Claude

## O que é este projeto

Aplicação web em Streamlit que permite baixar áudio do YouTube e aplicar transposição de tom (pitch shift) e/ou ajuste de velocidade (time stretch) para apoiar o estudo musical. Público-alvo: alunos do Conservatório de MPB de Curitiba.

## Ambiente

- **Python**: 3.12+
- **Gerenciador de pacotes e venv**: `uv` — use sempre `uv add` para adicionar dependências e `uv run` para executar scripts
- **Nunca** use `pip install` diretamente

### Comandos frequentes

```bash
# Criar ambiente e instalar dependências
uv sync

# Rodar a aplicação localmente
uv run streamlit run app.py

# Adicionar dependência
uv add <pacote>

# Adicionar dependência de dev
uv add --dev <pacote>
```

## Estrutura do projeto

```
music-transposer/
├── app.py              # Ponto de entrada Streamlit — UI e orquestração
├── audio/
│   ├── downloader.py   # Download de áudio via yt-dlp
│   └── processor.py    # Pitch shift e time stretch via librosa/pyrubberband
├── pyproject.toml      # Dependências gerenciadas pelo uv
├── PRD.md
└── CLAUDE.md
```

## Decisões de arquitetura

### Separação de responsabilidades
- `app.py` contém apenas lógica de UI Streamlit (estado, sliders, player)
- `audio/downloader.py` isola o yt-dlp e retorna um caminho de arquivo temporário
- `audio/processor.py` recebe um arquivo de áudio + parâmetros e retorna bytes ou caminho do arquivo processado

### Processamento de áudio
- **Pitch shift**: `librosa.effects.pitch_shift(y, sr=sr, n_steps=semitons)` — usa pyrubberband automaticamente quando instalado
- **Time stretch**: `librosa.effects.time_stretch(y, rate=fator)` — rate > 1.0 acelera, < 1.0 desacelera
- Aplicar pitch shift **antes** do time stretch quando ambos forem solicitados
- Salvar resultado em arquivo temporário (`.wav`) e passar para `st.audio()`

### Arquivos temporários
- Usar `tempfile.TemporaryDirectory()` com context manager para garantir limpeza
- No Streamlit Cloud, usar `/tmp` — é o único diretório gravável

### Estado no Streamlit
- Usar `st.session_state` para armazenar o caminho do áudio baixado e evitar re-download ao ajustar sliders
- Reprocessar o áudio somente ao clicar em "Processar", não em cada mudança de slider

## Dependências principais

```toml
[project]
dependencies = [
    "streamlit>=1.35",
    "yt-dlp>=2024.0",
    "librosa>=0.10",
    "pyrubberband>=0.3",
    "soundfile>=0.12",
    "numpy>=1.26",
]
```

> `pyrubberband` requer o binário `rubberband-cli` no sistema. No Streamlit Cloud, instalar via `packages.txt` com `rubberband-cli`.

## Arquivo packages.txt (Streamlit Cloud)

```
rubberband-cli
ffmpeg
```

> `ffmpeg` é necessário para yt-dlp converter o áudio baixado para WAV/MP3.

## Padrões de código

- Sem comentários óbvios — código auto-explicativo via nomes de funções e variáveis
- Funções puras em `audio/` — recebem parâmetros, retornam valores, sem efeitos colaterais globais
- Tratar erros de download (URL inválida, vídeo privado) com `st.error()` — nunca deixar exceção não tratada vazar para a UI
- Exibir `st.spinner()` durante download e processamento — operações podem levar vários segundos

## Escopo da v1

Apenas estas funcionalidades:
1. Input de URL do YouTube
2. Slider de semitons (-12 a +12)
3. Slider de velocidade (0.5× a 2.0×, passo 0.05)
4. Botão "Processar"
5. Player de áudio (`st.audio`)

**Não implementar** na v1: upload de arquivos locais, loop de trecho, detecção de tom, histórico, autenticação, download do resultado.
