# Giving Sky a Voice — TTS + STT team project

CAI3303C Natural Language Processing, Fall 2026 — team project demo.

Sky is Miami Dade College's planned virtual concierge (described by Professor Gabb in class). This project is a small working model of Sky's voice loop:

    microphone or recording -> Whisper (speech to text) -> FAQ answer (TF-IDF + cosine similarity) -> F5-TTS (text to speech) -> speaker

## What you need

The demo runs on your own Windows computer; there is no hosted version. It uses two repositories that work together:

| Repository | What it is |
| --- | --- |
| [CAI3303C_F5-TTS](https://github.com/MCDR-Code/CAI3303C_F5-TTS) | The class exercise: the fixed F5-TTS server (`imv_api.py`). It makes the voice and runs on port 5000. It also holds the shared Python environment. |
| CAI3303C_TTS_STT (this repository) | The team project: Whisper speech recognition, the FAQ "brain" and the web page. It runs on port 5001 and asks the TTS server for each spoken answer. |

Requirements:

- Windows 10 or 11, and about 10 GB of free disk space
- **Python 3.12**. Check in PowerShell with `python --version`. If it is missing, install it from python.org and tick **"Add python.exe to PATH"**, or run `winget install Python.Python.3.12`.
- **Git**: `winget install Git.Git`
- **ffmpeg** (Whisper uses it to read recordings): `winget install Gyan.FFmpeg`
- A microphone, to speak to Sky (optional: you can also type or upload a recording)
- **Recommended: an NVIDIA graphics card.** Each new spoken answer takes about 20 seconds on an RTX 2080 Super, but several minutes on a CPU.

After installing anything with winget, close PowerShell and open a new window so it finds the new programs.

## Install (once, about 20 to 30 minutes)

Open PowerShell in the folder where you keep projects and run these steps in order.

1. **Allow the setup scripts to run** (once per Windows account):

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

2. **Download both repositories into the same folder.** Use `git clone`, not "Download ZIP": the ZIP leaves out the F5-TTS source, which is linked as a submodule.

   ```powershell
   git clone --recurse-submodules https://github.com/MCDR-Code/CAI3303C_F5-TTS.git
   git clone https://github.com/MCDR-Code/CAI3303C_TTS_STT.git
   ```

3. **Set up the TTS server** (creates the Python environment and installs F5-TTS):

   ```powershell
   cd CAI3303C_F5-TTS
   .\Setup-TTS.ps1
   ```

4. **Only with an NVIDIA graphics card:** switch PyTorch to the graphics-card build (about 2 GB):

   ```powershell
   .\Enable-GPU.ps1
   ```

   It should end with `graphics card in use: True`.

5. **Set up the Sky demo** (adds Whisper and the demo's packages, downloads the Whisper model):

   ```powershell
   cd ..\CAI3303C_TTS_STT
   .\Setup-Demo.ps1
   ```

## Run the demo

```powershell
.\Start-Demo.ps1
```

It opens the TTS server in a second window, then starts the demo. Open **http://localhost:5001** in Chrome or Edge. Leave both windows open while you use it; Ctrl+C in each window stops them.

The **first** spoken answer downloads the F5-TTS model (about 1.3 GB) and can take several minutes. After that, a new answer takes about 20 seconds on a graphics card. Ask one practice question before showing it to anyone.

## Using the page

- **Ask:** type a question in English and press **Ask Sky**, click one of the six topic buttons, press **Record a question** (press again to stop and send), or upload a recording. Spoken and uploaded questions can be in many languages: Whisper writes down what you said and translates it to English to find the answer.
- **The answer** appears first as text, with **"Behind the answer"**: the closest FAQ question, the similarity score, the language heard and the timings. Below the 0.5 threshold, Sky says it does not know instead of guessing.
- **The voice:** **F5-TTS (model)** is the default. While it is being made, **Stop, wrong question** cancels it. **Browser voice (not the model)** uses Windows' built-in voice instead; it is instant but it is not F5-TTS.
- **Save this answer's voice** keeps the WAV, so the next time that answer comes up it plays instantly. **Clear saved answers** removes them, so F5-TTS makes every answer live again.

Good questions to try: "What is Sky?" (typed), "¿Hablas criollo?" (spoken; Sky understands Spanish and answers in English), and "How much is tuition?" (outside the FAQ, so Sky says it does not know).

## Without an NVIDIA graphics card

Everything works, but each new voice takes several minutes on the CPU. To keep the demo moving, save the answers once (**Save this answer's voice**) before presenting, or choose **Browser voice** and say that it is not the model.

## Troubleshooting

| Problem | Fix |
| --- | --- |
| "running scripts is disabled on this system" | Run step 1 again, or start a script with `powershell -ExecutionPolicy Bypass -File .\Start-Demo.ps1` |
| `python` is not recognized, or the version is not 3.12 | Install Python 3.12 with "Add python.exe to PATH", then open a new PowerShell |
| Setup-TTS fails at the F5-TTS step, or the `F5-TTS` folder is empty | The repository was downloaded as a ZIP. Delete it and use `git clone --recurse-submodules` (step 2) |
| "The TTS environment was not found" | Keep both repositories in the same parent folder, or set `SKY_TTS_ROOT` to the CAI3303C_F5-TTS folder |
| Recordings fail with an ffmpeg error | Install ffmpeg (`winget install Gyan.FFmpeg`) and open a new PowerShell |
| The microphone button does nothing | Use http://localhost:5001 (not the PC's IP address) and allow microphone access in the browser |
| Voice takes minutes | PyTorch is on the CPU. Run `.\Enable-GPU.ps1` in CAI3303C_F5-TTS (NVIDIA cards only) |
| "TTS server at http://localhost:5000 is not reachable" | Start it with `.\Start-TTS.ps1` in CAI3303C_F5-TTS, or just run `.\Start-Demo.ps1` again |
| Page looks old after an update | Refresh with Ctrl+F5 |

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
| `WHISPER_MODEL` | `base` | Whisper size. Whisper's translation can miss short questions: both `base` and `small` turned "¿Quién te creó?" into "Who do you think?" |
| `SKY_TTS_ROOT` | `..\CAI3303C_F5-TTS`, or `..\..\TTS` | Location of the TTS project folder |

## Scope

Six FAQ topics; matching uses TF-IDF with a 0.5 threshold. Spoken non-English questions are translated to English by Whisper for matching, and all answers are in English for now, because the F5-TTS base model was trained on English and Chinese speech only. This is a school prototype, not an official Miami Dade College service, and the FAQ answers are presentation content.

See [docs/THIRD_PARTY.md](docs/THIRD_PARTY.md) for credits and licenses.
