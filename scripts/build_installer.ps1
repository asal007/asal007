#requires -version 5
<#
Buildet das Windows-Setup (Inno Setup) für MeinImmoKauf.

Voraussetzungen:
- PyInstaller-EXE existiert unter .\dist\MeinImmoKauf.exe
- Inno Setup ist installiert (ISCC.exe im PATH)

Nutzung:
  powershell -ExecutionPolicy Bypass -File scripts\build_installer.ps1
#>

param(
    [string]$InnoScriptPath = "installer\inno_setup.iss",
    [string]$DistExePath = "dist\MeinImmoKauf.exe",
    [string]$ISCCPath = ""
)

Write-Host "==> Prüfe Voraussetzungen" -ForegroundColor Cyan
if (!(Test-Path $DistExePath)) {
    Write-Error "EXE nicht gefunden: $DistExePath. Bitte zuerst 'scripts\\build_exe.ps1' ausführen."
    exit 1
}

function Resolve-ISCCPath {
    param([string]$ProvidedPath)

    if ($ProvidedPath -and (Test-Path $ProvidedPath)) {
        return $ProvidedPath
    }

    $cmd = Get-Command ISCC -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Path }

    $candidates = @(
        (Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe')
        (Join-Path ${env:ProgramFiles} 'Inno Setup 6\ISCC.exe')
    )
    foreach ($p in $candidates) {
        if (Test-Path $p) { return $p }
    }

    return $null
}

$resolvedISCC = Resolve-ISCCPath -ProvidedPath $ISCCPath
if (-not $resolvedISCC) {
    Write-Error "Inno Setup Compiler (ISCC.exe) nicht gefunden. Bitte Inno Setup installieren oder Pfad per -ISCCPath angeben (z. B. 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe')."
    exit 1
}

Write-Host "==> Starte Inno Setup Build" -ForegroundColor Cyan
& $resolvedISCC $InnoScriptPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "Inno Setup Build fehlgeschlagen (ExitCode: $LASTEXITCODE)"
    exit $LASTEXITCODE
}

Write-Host "==> Fertig. Setup liegt in 'installer_output'" -ForegroundColor Green