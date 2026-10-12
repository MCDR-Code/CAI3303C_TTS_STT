# Command-line version of the demo (no web page).
#   .\Run-CLI.ps1 -Text "What is Sky?" -NoTts     quick check, nothing else needed
#   .\Run-CLI.ps1                                  record 5 seconds from the microphone
#   .\Run-CLI.ps1 -Audio C:\path\question.wav      use a recording
param(
    [string]$Text,
    [string]$Audio,
    [switch]$NoTts,
    [double]$Seconds = 5,
    [string]$Voice = 'default'
)
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '_tts_env.ps1')
$demoArgs = @((Join-Path $PSScriptRoot 'sky_voice_demo.py'), '--seconds', "$Seconds", '--voice', $Voice)
if ($Text) { $demoArgs += @('--text', $Text) }
if ($Audio) { $demoArgs += @('--audio', $Audio) }
if ($NoTts) { $demoArgs += '--no-tts' }
if (!$NoTts -and !(Test-TtsServer)) { throw 'Start the TTS server first (TTS\Start-TTS.ps1), or add -NoTts.' }
& $TtsPython @demoArgs
if ($LASTEXITCODE -ne 0) { throw 'The Sky demo failed. See the message above.' }
