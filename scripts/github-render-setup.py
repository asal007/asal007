#!/usr/bin/env python3
"""
MeinImmoKauf - GitHub + Render Setup Helper
Dieser Guide zeigt die exakten Schritte für Deployment
"""

import subprocess
import os
import sys

print("""
╔════════════════════════════════════════════════════════════╗
║   🚀 MeinImmoKauf - GitHub + Render Setup                  ║
║      Schritt-für-Schritt Guide                            ║
╚════════════════════════════════════════════════════════════╝
""")

# Schritt 1: Git initialisieren
print("\n📍 SCHRITT 1: GitHub Repository vorbereiten\n")
print("1.1 Gehe zu https://github.com/new")
print("    - Repository Name: 'meinimmokauf'")
print("    - Beschreibung: 'MeinImmoKauf - Ratgeber für Immobilienkauf'")
print("    - Public (damit Render zugreifen kann)")
print("    - Keine README/Lizenz (wir haben schon eine)")
print("")
print("1.2 Nach Erstellung: Kopiere die Repository-URL:")
print("    Beispiel: https://github.com/asal007/meinimmokauf.git")
print("")

# Lokale Git-Vorbereitung
print("1.3 Terminal: Git initialisieren\n")

commands = [
    ("git init", "Git Repository initialisieren"),
    ("git add .", "Alle Dateien hinzufügen"),
    ('git commit -m "Initial commit: MeinImmoKauf v1.0 - Ready for Play Store"', "Commit erstellen"),
    ("git branch -M main", "Branch zu 'main' umbenennen"),
]

print("   Führe diese Befehle aus:")
for i, (cmd, desc) in enumerate(commands, 1):
    print(f"   {i}. [{desc}]")
    print(f"      $ {cmd}\n")

print("\n" + "="*60)
print("📍 SCHRITT 2: Mit GitHub verbinden\n")

print("2.1 Im Terminal (nach git commit):")
print("""
   $ git remote add origin https://github.com/asal007/meinimmokauf.git
   $ git push -u origin main
""")

print("   Hinweis: Falls 'git push' fehlschlägt:")
print("   - Token-basiert: GitHub → Settings → Developer Settings")
print("   - Personal Access Token mit 'repo' Scope")
print("   - Passwort durch Token ersetzen")

print("\n" + "="*60)
print("📍 SCHRITT 3: Render Web Service erstellen\n")

print("""3.1 Gehe zu https://render.com/register
   - Mit GitHub anmelden
   - Account erstellen (kostenlos)

3.2 Dashboard → "New" → "Web Service"
   
3.3 "Connect to GitHub"
   - Repository: 'meinimmokauf' wählen
   - Authorize Render

3.4 Konfiguriere Web Service:

   Name:              meinimmokauf
   
   Environment:       Python 3
   
   Region:            Frankfurt (ams) oder EU
   
   Build Command:
   pip install -r requirements.txt
   
   Start Command:
   streamlit run app.py --server.port=10000 --server.address=0.0.0.0
   
   Instance Type:     Free (mit autom. Sleep)
                      oder Paid ($7/Mo für keine Sleep-Zeiten)

3.5 Environment Variables (Optional aber empfohlen):
   
   Key: STREAMLIT_SERVER_HEADLESS
   Value: true
   
   Key: STREAMLIT_SERVER_PORT
   Value: 10000

3.6 "Create Web Service" klicken

3.7 Warten (2-5 Minuten)
   - Logs folgen im Render Dashboard
   - Deployment abgeschlossen: Status = "Running"
   - URL angezeigt: https://meinimmokauf.onrender.com (BEISPIEL)
""")

print("\n" + "="*60)
print("📍 SCHRITT 4: URL in Capacitor eintragen\n")

print("""4.1 Öffne: mobile/capacitor.config.ts

4.2 Ändere diese Zeile:
   
   VON:
   server: { url: 'https://DEINE-PRODUKTIONS-URL.com', cleartext: false }
   
   ZU:
   server: { url: 'https://meinimmokauf.onrender.com', cleartext: false }
   
   (Verwende deine echte Render-URL)

4.3 Speichern und zu Git committen:
   
   $ git add mobile/capacitor.config.ts
   $ git commit -m "Update Capacitor URL to production"
   $ git push
""")

print("\n" + "="*60)
print("📍 SCHRITT 5: Test\n")

print("""5.1 Öffne in Browser: https://meinimmokauf.onrender.com

5.2 Teste:
   ☐ Seite lädt
   ☐ Login funktioniert (admin / admin1234)
   ☐ Favoriten speichern funktioniert
   ☐ Zu Seite 1 navigieren funktioniert
   ☐ Logout funktioniert

5.3 Falls 503 Error:
   - Warte 2-3 Minuten (Cold Start)
   - Refresh mit Ctrl+Shift+R (Cache leeren)
   - Render Logs prüfen (Dashboard)
""")

print("\n" + "="*60)
print("✅ FERTIG!\n")

print("""Nächste Schritte:
1. Google Play Console Account erstellen ($25)
2. Play Store Listing ausfüllen (2 Stunden)
3. AAB bauen: cd mobile/android && ./gradlew bundleRelease
4. AAB hochladen & Review abwarten (1-7 Tage)
5. 🎉 Im Play Store!

Hilfreiche Dateien:
📄 docs/build-guide.md - Komplette AAB Build-Anleitung
📄 docs/play-store-metadaten.md - Store-Texte
📄 GOOGLE_PLAY_STORE_READY.md - Komplette Checkliste
""")

print("\n" + "="*60)
print("\n💡 TIPPS:\n")

tips = [
    "Render: Free Plan lädt mit 15-20sec Verzögerung (Cold Start)",
    "Render: $7/Mo bezahlt → keine Sleep-Zeiten",
    "SQLite funktioniert, aber Backups manuell!",
    "Für Production: PostgreSQL nutzen (Render hat kostenlose Tier)",
    "Secrets (SMTP) über Render Environment Variables, nicht in Code!",
]

for tip in tips:
    print(f"  • {tip}")

print("\n" + "="*60)
print("🎯 Geschätzte Zeit:\n")
print("  GitHub Setup:    5 min")
print("  Render Setup:    10 min")
print("  Deploy warten:   5-10 min")
print("  URL testen:      5 min")
print("  ────────────────────")
print("  TOTAL:           25-30 min")
print("\n" + "="*60)
