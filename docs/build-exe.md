# Windows EXE erstellen (Streamlit → MeinImmoKauf.exe)

Dieser Leitfaden erstellt eine eigenständige Windows‑EXE, die deine Streamlit‑App startet und automatisch im Browser öffnet.

## Voraussetzungen
- Windows, PowerShell
- Python/venv mit allen Abhängigkeiten (`pip install -r requirements.txt`)
- Projektwurzel: `c:\Users\KAsys\Documents\trae_projects\meinimmokauf`

## Build‑Schritte
1. Öffne PowerShell in der Projektwurzel.
2. Aktiviere ggf. dein venv: `.\.venv\Scripts\Activate.ps1`.
3. Starte das Build‑Skript:
   ```powershell
   scripts\build_exe.ps1
   ```
4. Ergebnis: `dist\MeinImmoKauf.exe`.

## Was macht die EXE?
- Lädt die gebündelte App (`app.py`, `pages`, `.streamlit`) und startet Streamlit lokal auf `http://localhost:8502/`.
- Öffnet den Standardbrowser automatisch.

## Optionen
- Debug‑Build mit Konsolenfenster: ändere in `scripts/build_exe.ps1` `--windowed` zu `--console`.
- Port anpassen: in `scripts/windows_launcher.py` `run_streamlit(..., port=8502)` ändern.

## Häufige Fragen
- „Die EXE startet, aber nichts passiert“: Prüfe Firewall/Antivirus. Einige blockieren lokalen Server.
- „Große EXE“: PyInstaller packt Python und Abhängigkeiten ein; OneFile ist i. d. R. 100+ MB.
- „Konfiguration wird ignoriert“: Achte darauf, dass `.streamlit\config.toml` mitgepackt wird (im Skript enthalten).

## Release weitergeben
- Verteile nur die Datei `dist\MeinImmoKauf.exe`.
- Die EXE startet ohne zusätzliches Python, da die Laufzeit eingebettet ist.