# Giving Sky a Voice — TTS + STT team project

CAI3303C Natural Language Processing, Fall 2026 — team project demo.

Sky is Miami Dade College's planned virtual concierge (described by Professor Gabb in class). This project is a small working model of Sky's voice loop:

    microphone or recording -> Whisper (speech to text) -> FAQ answer (TF-IDF + cosine similarity) -> F5-TTS (text to speech) -> speaker

## How to try it

There is no hosted version. The demo runs on your own Windows computer, together with the TTS server from the class exercise. A recorded walkthrough was made for the class presentation.

You need Windows 10/11, Python 3.12, Git, ffmpeg, about 10 GB of free disk space, and a microphone if you want to speak to Sky. An NVIDIA graphics card is strongly recommended: Sky's spoken answer takes about 23 seconds on an RTX 2080 Super, and several minutes on a CPU.

## How this project relates to the TTS assignment

| Repository | What it is |
| --- | --- |
| [CAI3303C_F5-TTS](https://github.com/MCDR-Code/CAI3303C_F5-TTS) | The class exercise: the fixed F5-TTS server (`imv_api.py`), the Java clients and the Python environment. It runs on port 5000. |
| CAI3303C_TTS_STT (this repository) | The team project. It adds speech recognition, the FAQ "brain" and the web page, and runs on port 5001. |

This project contains no copy of the TTS code. It sends each answer to the TTS server over HTTP (`POST http://localhost:5000/tts`) and plays the WAV that comes back. It also uses the TTS project's Python environment (its `.venv` folder), so PyTorch is installed only once.

## Setup (once)

1. Clone both repositories into the same parent folder:

   ```text
   git clone --recurse-submodules https://github.com/MCDR-Code/CAI3303C_F5-TTS.git
   git clone https://github.com/MCDR-Code/CAI3303C_TTS_STT.git
   ```

   The demo looks for the TTS project next to it (`..\CAI3303C_F5-TTS`). If you keep it somewhere else, set `SKY_TTS_ROOT` to its folder.
2. Set up the TTS project first: in `CAI3303C_F5-TTS`, run `.\Setup-TTS.ps1`. If you have an NVIDIA graphics card, also install the CUDA build of PyTorch as its README explains.
3. In this folder, run `.\Setup-Demo.ps1`. It adds Whisper and the other demo packages to the shared environment, downloads the Whisper model, and reports whether the graphics card is in use.

## Run the web demo

```powershell
.\Start-Demo.ps1
```

Open **http://localhost:5001**. If the TTS server isn't running, the script starts it in its own window first.

- Type **What is Sky?** to show a known answer.
- Type **How much is tuition?** to show the fallback. The demo tells the person to ask a staff member; it does not transfer anyone.
- To show another language, **speak or upload** the question (for example "¿Hablas criollo?"). Whisper translates it to English and Sky answers in English. Typed questions must be in English.
- Voice output: **Browser voice (fast)** uses the browser's built-in voice, not F5-TTS. Say so if you use it. **F5-TTS (model)** asks the TTS server to generate the audio.

## Saved answers (faster replies)

F5-TTS takes about 20 seconds to speak a new answer. Because Sky's six FAQ answers are fixed, the page offers **Save this answer's voice** after F5-TTS makes one. The next time any question leads to that answer, the saved WAV plays right away. **Clear saved answers** removes them so F5-TTS makes every answer live again. Saved files go in `saved_answers/`, which is not uploaded to GitHub.

This only works because the answers never change. If Sky looked answers up on the college website or used an LLM, every answer would be new text, and the voice would have to be made live each time.

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
| `faq.json` | Six FAQ topics, each with several rewordings, answers in English (Spanish answers are kept for a future Spanish voice model) |
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
| `SKY_TTS_ROOT` | `..\CAI3303C_F5-TTS`, or `..\..\TTS` | Location of the TTS project folder |

## Scope

Six FAQ topics; matching uses TF-IDF with a 0.5 threshold. Spoken non-English questions are translated to English by Whisper for matching, and all answers are in English for now, because the F5-TTS base model was trained on English and Chinese speech only. This is a school prototype, not an official Miami Dade College service, and the FAQ answers are presentation content.

See [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md) for credits and licenses.
