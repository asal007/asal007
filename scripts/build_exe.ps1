# Requires: Python (same venv), pip packages installed per requirements.txt
# 1) Installiere PyInstaller
pip install pyinstaller

# 2) Baue eine OneFile-EXE (konsolelos: --windowed; für Debug: --console)
#    WICHTIG: Daten-Dateien hinzufügen, damit Streamlit app.py und Seiten findet.
pyinstaller --noconfirm --onefile --windowed `
  --name MeinImmoKauf `
  scripts/windows_launcher.py `
  --add-data "app.py;." `
  --add-data "i18n.py;." `
  --add-data "utils.py;." `
  --add-data "auth.py;." `
  --add-data "db.py;." `
  --add-data "pages;pages" `
  --add-data ".streamlit;.streamlit" `
  --add-data "README.md;." 

Write-Host "Fertig. EXE liegt unter dist/MeinImmoKauf.exe"