# One-time setup: adds the demo's packages to the shared TTS environment
# and downloads the Whisper model.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_tts_env.ps1')
& $TtsPython -m pip install -r (Join-Path $PSScriptRoot 'requirements.txt')
if ($LASTEXITCODE -ne 0) { throw 'Installing the demo packages failed.' }
& $TtsPython -c "import whisper; whisper.load_model('base'); print('Whisper base model is ready.')"
if ($LASTEXITCODE -ne 0) { throw 'Whisper model download failed.' }
& $TtsPython -c "import torch; print('PyTorch', torch.__version__, '| graphics card in use:', torch.cuda.is_available())"
Push-Location $PSScriptRoot
& $TtsPython -c "import sky_voice_demo as s; print('ffmpeg for recordings: ' + ('ready' if s.ensure_ffmpeg() else 'MISSING - install it (winget install Gyan.FFmpeg)'))"
Pop-Location
Write-Host 'Setup complete. Run .\Start-Demo.ps1'
