# PRD — Music Transposer

## Problema

Músicos que estudam por repertório precisam tocar a mesma música em tons diferentes — seja para adaptar ao seu instrumento, à voz de um cantor, ou para praticar em todas as tonalidades. Hoje, a única opção prática é buscar uma versão diferente no YouTube ou usar softwares pesados e não intuitivos.

## Usuários-alvo

Alunos do Conservatório de MPB de Curitiba — especialmente violonistas e guitarristas que precisam acompanhar músicas do YouTube em tons diferentes durante o estudo.

---

## Versão 1 — Escopo

### Funcionalidades

| # | Funcionalidade | Descrição |
|---|---------------|-----------|
| 1 | **Entrada por link do YouTube** | Usuário cola a URL de uma música do YouTube |
| 2 | **Transposição de tom (pitch shift)** | Ajuste em semitons (+12 a -12) sem alterar o andamento |
| 3 | **Player de áudio** | Reprodução do áudio processado direto no browser |

### Fluxo principal

```
1. Usuário cola link do YouTube
2. App faz download do áudio (yt-dlp)
3. Usuário ajusta slider de semitons
4. Usuário clica em "Processar"
5. App aplica pitch shift (pedalboard)
6. Player de áudio aparece na tela para reprodução imediata
```

### Interface

- **Framework**: Streamlit
- **Layout**: Uma página única, inputs no topo, player na parte inferior
- **Controles**:
  - Campo de texto para URL do YouTube
  - Slider de semitons: -12 a +12, valor padrão 0
  - Botão "Processar"
  - Player de áudio nativo do Streamlit (`st.audio`)

### Deploy

- **Plataforma**: Streamlit Community Cloud
- **Acesso**: URL pública compartilhada com os colegas
- **Autenticação**: Nenhuma na v1

---

## Stack técnica

| Componente | Tecnologia |
|-----------|------------|
| Linguagem | Python 3.12+ |
| Gerenciamento de ambiente | `uv` |
| Interface | Streamlit |
| Download de áudio | `yt-dlp` |
| Processamento de áudio | `pedalboard` (Spotify) |
| Deploy | Streamlit Community Cloud |

### Por que pedalboard?

- Qualidade de nível profissional (JUCE/phase vocoder), mantido pela Spotify
- Sem dependências de sistema — instala como wheel puro, sem binários C++
- Compatível com Streamlit Cloud sem configuração adicional

---

## Fora do escopo — v1

- Carregamento de arquivos MP3 locais
- Loop de trecho
- Detecção automática do tom original
- Histórico de músicas
- Autenticação de usuários
- Download do áudio processado

---

## Roadmap futuro

| Versão | Funcionalidade |
|--------|---------------|
| v1.1 | Suporte a upload de arquivos MP3/WAV |
| v1.2 | Loop de trecho (definir início e fim em segundos) |
| v1.3 | Ajuste de velocidade (time stretch sem alterar o tom) |
| v2.0 | Detecção automática do tom original |
| v2.0 | Histórico de músicas e configurações por sessão |

---

## Restrições e riscos

| Item | Detalhe |
|------|---------|
| **ToS do YouTube** | Download via yt-dlp pode violar os termos de serviço do YouTube. Uso educacional e pessoal minimiza o risco, mas não o elimina. |
| **Limites do Streamlit Cloud** | O plano gratuito tem limite de RAM (~1 GB) e CPU. Músicas longas podem falhar no processamento. |
| **Tempo de processamento** | Pitch shift com qualidade alta é custoso. Para músicas longas, pode levar vários segundos. |
| **Armazenamento temporário** | Arquivos de áudio são gerados em `/tmp` e descartados ao reiniciar o servidor. |
