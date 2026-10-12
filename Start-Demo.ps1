# Starts the Sky web demo on http://localhost:5001.
# If the TTS server (port 5000) is not running, it is started in its own window.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_tts_env.ps1')
if (!(Test-TtsServer)) {
    Write-Host 'Starting the TTS server in a new window...'
    $startTts = Join-Path $TtsRoot 'Start-TTS.ps1'
    Start-Process powershell -ArgumentList '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', "`"$startTts`""
    $waited = 0
    while (!(Test-TtsServer) -and $waited -lt 90) { Start-Sleep -Seconds 3; $waited += 3 }
    if (Test-TtsServer) { Write-Host 'TTS server is ready.' }
    else { Write-Warning 'TTS server is not answering yet. Typed and spoken questions still work; voice output will work once it is up.' }
}
Write-Host 'Starting the Sky demo. Open http://localhost:5001 (Ctrl+C stops it).'
Push-Location $PSScriptRoot
try {
    & $TtsPython (Join-Path $PSScriptRoot 'app.py')
} finally {
    Pop-Location
}
