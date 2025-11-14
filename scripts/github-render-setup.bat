@echo off
REM MeinImmoKauf - GitHub + Render Setup Checklist
REM Interactive Windows PowerShell Script

cls
echo.
echo ============================================================
echo   MeinImmoKauf - GitHub + Render Setup CHECKLIST
echo ============================================================
echo.

set step=1

echo.
echo [%step%] GitHub Repository erstellen
echo =========================================
echo.
echo  1. Gehe zu: https://github.com/new
echo  2. Repository Name: "meinimmokauf"
echo  3. Beschreibung: "MeinImmoKauf - Ratgeber fuer Immobilienkauf"
echo  4. Public auswählen
echo  5. "Create repository" klicken
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] Git Credentials speichern (wenn nötig)
echo =========================================
echo.
echo Falls Windows GitCredentialManager nutzt:
echo - Erstes Mal beim Push: GitHub Login eingeben
echo - Danach automatisch gespeichert
echo.
echo Falls Token-basiert nötig:
echo - GitHub: Settings ^> Developer Settings ^> Personal Access Tokens
echo - Token mit "repo" Scope erstellen
echo - Als Passwort beim Push verwenden
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] Lokale Git-Befehle
echo =========================================
echo.
echo Füge diese Befehle in PowerShell ein (nacheinander):
echo.
echo 1. cd c:\Users\KAsys\Desktop\ImmoGuide
echo    git init
echo.
echo 2. git add .
echo.
echo 3. git commit -m "Initial commit: MeinImmoKauf v1.0"
echo.
echo 4. git branch -M main
echo.
echo 5. git remote add origin https://github.com/DEIN-USERNAME/meinimmokauf.git
echo    ^(Ersetze DEIN-USERNAME^)
echo.
echo 6. git push -u origin main
echo.
echo Danach solltest du die Dateien auf GitHub sehen!
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] Render.com Setup
echo =========================================
echo.
echo  1. Gehe zu: https://render.com/register
echo  2. Mit GitHub anmelden
echo  3. Account bestätigen
echo  4. Dashboard ^> "New" ^> "Web Service"
echo  5. "Connect to GitHub" ^> meinimmokauf auswählen
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] Web Service Konfiguration
echo =========================================
echo.
echo Folgende Werte eintragen:
echo.
echo Name:              meinimmokauf
echo Environment:       Python 3
echo Region:            Frankfurt (ams)
echo.
echo Build Command:
echo   pip install -r requirements.txt
echo.
echo Start Command:
echo   streamlit run app.py --server.port=10000 --server.address=0.0.0.0
echo.
echo Instance Type:     Free (oder Paid $7/Mo)
echo.
echo "Create Web Service" klicken
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] Deploy warten
echo =========================================
echo.
echo Die Deploy beginnt automatisch...
echo Warte 2-5 Minuten
echo.
echo Indikator: "Running" = Erfolgreich
echo.
echo Die URL sollte angezeigt werden:
echo https://meinimmokauf.onrender.com
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] capacitor.config.ts aktualisieren
echo =========================================
echo.
echo 1. Öffne: mobile\capacitor.config.ts
echo 2. Suche: url: 'https://DEINE-PRODUKTIONS-URL.com'
echo 3. Ersetze durch: url: 'https://meinimmokauf.onrender.com'
echo 4. Speichern
echo.
echo 5. PowerShell-Befehle:
echo    git add mobile/capacitor.config.ts
echo    git commit -m "Update Capacitor URL"
echo    git push
echo.
pause

set /a step+=1
cls
echo.
echo [%step%] URL Test
echo =========================================
echo.
echo 1. Browser öffnen
echo 2. Gehe zu: https://meinimmokauf.onrender.com
echo 3. Warte auf Laden (kann 20 Sekunden dauern)
echo.
echo 4. Test-Schritte:
echo    - Login: admin / admin1234
echo    - Favoriten speichern?
echo    - Navigation funktioniert?
echo    - Logout funktioniert?
echo.
pause

cls
echo.
echo ============================================================
echo  FERTIG!
echo ============================================================
echo.
echo Nächste Schritte:
echo.
echo 1. Google Play Console Account: https://play.google.com/console
echo    (Kostet 25 USD Einmalgebühr mit Kreditkarte)
echo.
echo 2. AAB bauen:
echo    cd c:\Users\KAsys\Desktop\ImmoGuide\mobile\android
echo    gradlew bundleRelease
echo.
echo 3. Upload zu Play Store & Review
echo.
echo Hilfreiche Dateien:
echo - docs\build-guide.md
echo - docs\play-store-metadaten.md
echo - GOOGLE_PLAY_STORE_READY.md
echo.
pause
