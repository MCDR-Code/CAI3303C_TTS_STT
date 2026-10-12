# Giving Sky a Voice — TTS + STT team project

CAI3303C Natural Language Processing, Fall 2026 — team project demo.

Sky is Miami Dade College's planned virtual concierge (described by Professor Gabb in class). This project is a small working model of Sky's voice loop:

    microphone or recording -> Whisper (speech to text) -> FAQ answer (TF-IDF + cosine similarity) -> F5-TTS (text to speech) -> speaker

## How this project relates to the TTS assignment

| Folder | What it is |
| --- | --- |
| `01_Assignments\TTS` | The class exercise: the fixed F5-TTS server (`imv_api.py`), the Java clients and the Python environment. It runs on port 5000. |
| `01_Assignments\Class_Project\TTS_STT` (this folder) | The team project. It adds speech recognition, the FAQ "brain" and the web page, and runs on port 5001. |

This project contains no copy of the TTS code. It sends each answer to the TTS server over HTTP (`POST http://localhost:5000/tts`) and plays the WAV that comes back. It also uses the TTS folder's Python environment (`..\..\TTS\.venv`), so PyTorch is installed only once.

## Setup (once)

1. Set up the TTS assignment first (`TTS\Setup-TTS.ps1`). For speed on CLOCKTOWER, install the CUDA (graphics card) build of PyTorch in that environment; see the TTS README.
2. In this folder, run `.\Setup-Demo.ps1`. It adds Whisper and the other demo packages to the shared environment, downloads the Whisper model, and reports whether the graphics card is in use.

## Run the web demo

```powershell
.\Start-Demo.ps1
```

Open **http://localhost:5001**. If the TTS server isn't running, the script starts it in its own window first.

- Type **What is Sky?** to show a known answer.
- Type **How much is tuition?** to show the fallback. The demo tells the person to ask a staff member; it does not transfer anyone.
- To show Spanish, **speak or upload** the question (for example "¿Hablas criollo?"). Typed questions are matched as English.
- Voice output: **Browser voice (fast)** uses the browser's built-in voice, not F5-TTS. Say so if you use it. **F5-TTS (model)** asks the TTS server to generate the audio.

## Run the command-line version

```powershell
.\Run-CLI.ps1 -Text "What is Sky?" -NoTts     # quick check, no servers needed
.\Run-CLI.ps1 -Text "What is Sky?"            # spoken answer (TTS server must be running)
.\Run-CLI.ps1                                 # record 5 seconds from the microphone
.\Run-CLI.ps1 -Audio C:\path\question.wav     # use a recording
```

It prints what Whisper heard, the matched FAQ question and score, and the time each step took.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Web server: page, Whisper transcription, FAQ answers, forwards voice requests to the TTS server |
| `sky_voice_demo.py` | The loop's building blocks, plus the command-line demo |
| `faq.json` | Six FAQ topics, each with several rewordings, answers in English and Spanish |
| `index.html` | The browser page |
| `Setup-Demo.ps1`, `Start-Demo.ps1`, `Run-CLI.ps1`, `_tts_env.ps1` | Windows scripts |
| `tests/` | Automated checks (no models needed) |
| `docs/` | Classroom demo guide, credits, screenshot |

## Settings

| Variable | Default | Meaning |
| --- | --- | --- |
| `TTS_URL` | `http://localhost:5000` | Where the TTS server is |
| `SKY_PORT` | `5001` | Port for this demo |
| `SKY_HOST` | `127.0.0.1` | Only this PC can open the demo. Use `0.0.0.0` to allow other devices on the network |
| `WHISPER_MODEL` | `base` | Whisper size. `small` is more accurate and fine on the graphics card |
| `SKY_TTS_ROOT` | `..\..\TTS` | Location of the TTS assignment folder |

## Scope

Six FAQ topics; matching uses TF-IDF with a 0.5 threshold. Spoken non-English questions are translated to English by Whisper for matching, and Spanish questions get Spanish answers. Haitian Creole is understood but answered in English. This is a school prototype, not an official Miami Dade College service, and the FAQ answers are presentation content.

See [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md) for credits and licenses.
