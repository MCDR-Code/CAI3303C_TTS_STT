# Shared helper: locates the TTS assignment folder and its Python environment.
# Looks in SKY_TTS_ROOT, then next to this folder (two cloned repositories),
# then the course folder layout (01_Assignments\TTS).
$candidates = @($env:SKY_TTS_ROOT, (Join-Path $PSScriptRoot '..\CAI3303C_F5-TTS'), (Join-Path $PSScriptRoot '..\..\TTS')) | Where-Object { $_ }
$script:TtsRoot = $null
foreach ($candidate in $candidates) {
    if (Test-Path -LiteralPath (Join-Path $candidate '.venv\Scripts\python.exe')) { $script:TtsRoot = [IO.Path]::GetFullPath($candidate); break }
}
if (!$script:TtsRoot) { $script:TtsRoot = [IO.Path]::GetFullPath($candidates[0]) }
$script:TtsPython = Join-Path $script:TtsRoot '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $script:TtsPython)) {
    throw "The TTS environment was not found at $script:TtsPython. Set up the TTS project first (Setup-TTS.ps1 in CAI3303C_F5-TTS), or set SKY_TTS_ROOT to its folder."
}
function Test-TtsServer {
    try { Invoke-RestMethod 'http://localhost:5000/health' -TimeoutSec 3 | Out-Null; return $true }
    catch { return $false }
}
