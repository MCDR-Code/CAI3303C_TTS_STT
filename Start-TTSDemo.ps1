# Starts the Topic Presentation screen on port 5002 for local and router access.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_tts_env.ps1')

if (!(Test-TtsServer)) {
    Write-Host 'Starting the TTS server in its own window...'
    $startTts = Join-Path $TtsRoot 'Start-TTS.ps1'
    Start-Process powershell -ArgumentList '-NoExit', '-ExecutionPolicy', 'Bypass', '-File', "`"$startTts`""
    $waited = 0
    while (!(Test-TtsServer) -and $waited -lt 90) {
        Start-Sleep -Seconds 3
        $waited += 3
    }
    if (!(Test-TtsServer)) {
        throw 'The TTS server is not ready. Run Start-TTS.ps1 in the TTS project to check its output, then try again.'
    }
}

$topicUrl = 'http://localhost:5002/topic'
$existingPage = $null
try { $existingPage = Invoke-WebRequest $topicUrl -UseBasicParsing -TimeoutSec 3 } catch { }
if ($existingPage -and $existingPage.Content.Contains('<title>Giving Sky a Voice - Topic Presentation</title>')) {
    $networkListener = Get-NetTCPConnection -State Listen -LocalPort 5002 -ErrorAction SilentlyContinue | Where-Object { $_.LocalAddress -eq '0.0.0.0' }
    if (!$networkListener) {
        throw 'The existing demo only accepts localhost connections. Stop it with Ctrl+C, then run Start-TTSDemo.ps1 again to enable router access.'
    }
    Write-Host "The TTS demo is already running. Open $topicUrl"
    return
}
if (Get-NetTCPConnection -State Listen -LocalPort 5002 -ErrorAction SilentlyContinue) {
    throw 'Port 5002 is already in use by another server. Stop that server before starting the TTS demo.'
}

$previousPort = $env:SKY_PORT
$previousHost = $env:SKY_HOST
$env:SKY_PORT = '5002'
$env:SKY_HOST = '0.0.0.0'
Write-Host "Starting the TTS demo. Open $topicUrl"
Write-Host 'Leave this window open. Ctrl+C stops the demo.'
Push-Location $PSScriptRoot
try {
    & $TtsPython (Join-Path $PSScriptRoot 'app.py')
    if ($LASTEXITCODE -ne 0) { throw 'The TTS demo stopped with an error.' }
} finally {
    Pop-Location
    $env:SKY_PORT = $previousPort
    $env:SKY_HOST = $previousHost
}
