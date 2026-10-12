# Shared helper: locates the TTS assignment folder and its Python environment.
$script:TtsRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\TTS'))
if ($env:SKY_TTS_ROOT) { $script:TtsRoot = $env:SKY_TTS_ROOT }
$script:TtsPython = Join-Path $script:TtsRoot '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $script:TtsPython)) {
    throw "The TTS environment was not found at $script:TtsPython. Set up the TTS assignment first (TTS\Setup-TTS.ps1), or set SKY_TTS_ROOT to its folder."
}
function Test-TtsServer {
    try { Invoke-RestMethod 'http://localhost:5000/health' -TimeoutSec 3 | Out-Null; return $true }
    catch { return $false }
}
