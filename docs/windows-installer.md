# Windows Setup (Installer) für MeinImmoKauf

Dieser Leitfaden erstellt ein klassisches Windows‑Setup (Installationsassistent), das deine bereits gebaute EXE (`dist\MeinImmoKauf.exe`) benutzerfreundlich installiert, Startmenü/Desktop‑Verknüpfung erstellt und die App direkt startet.

## Voraussetzungen
- Windows mit PowerShell
- EXE gebaut: `scripts\build_exe.ps1` ausgeführt, Ergebnis in `dist\MeinImmoKauf.exe`
- Inno Setup installiert (https://jrsoftware.org/isinfo.php) und `ISCC.exe` im `PATH`

## Build des Installers
1. Öffne PowerShell im Projektordner.
2. (Optional) venv aktivieren: ` .\.venv\Scripts\Activate.ps1 `
3. Installer bauen:
   ```powershell
   scripts\build_installer.ps1
   ```
4. Ergebnis: `installer_output\MeinImmoKaufSetup.exe`

## Was macht der Installer?
- Installiert nach `%LOCALAPPDATA%\MeinImmoKauf` (keine Admin‑Rechte nötig)
- Erstellt Startmenüeintrag „MeinImmoKauf“ und optional eine Desktop‑Verknüpfung
- Startet die App nach der Installation automatisch
- Saubere Deinstallation über „Apps & Features“ / „Programme und Features“

## Optionen anpassen
- Produktname/Version: in `installer/inno_setup.iss` `AppName`, `AppVersion` anpassen
- Installationspfad: `DefaultDirName` ändern (Standard: `{localappdata}\MeinImmoKauf`)
- Desktop‑Shortcut standardmäßig aktivieren: in `[Tasks]` Flag `unchecked` entfernen
- Post‑Install Autostart entfernen: `[Run]` Sektion entfernen oder `skipifsilent` anpassen

## Typische Probleme
- `ISCC.exe nicht gefunden`: Inno Setup installieren und den Compiler zum `PATH` hinzufügen
- `EXE nicht gefunden`: erst `scripts\build_exe.ps1` ausführen
- Antivirus blockiert lokalen Server: App signieren oder Whitelist hinzufügen

## Signierung (empfohlen)
Für weniger Warnungen beim Download:
- Code‑Signing Zertifikat verwenden und die EXE/Setup signieren (z. B. mit `signtool.exe`)
- Signierung kann vor dem Inno‑Build (EXE) oder nach dem Inno‑Build (Setup) erfolgen

## Deinstallation
- Über „Apps & Features“: MeinImmoKauf auswählen → Deinstallieren
- Entfernt Verknüpfungen und den Installationsordner `%LOCALAPPDATA%\MeinImmoKauf`