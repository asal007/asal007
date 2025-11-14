# MeinImmoKauf – Bereitstellung

Dieses Projekt ist eine Streamlit-App. Nachfolgend findest du Schritte zur lokalen Ausführung und zur Bereitstellung (Streamlit Cloud oder Docker).

## ✨ Neue Features

Diese vollständig überarbeitete Version bietet:

- 🔐 **Authentifizierung & Autorisierung**
  - Benutzer-Login und Registrierung mit bcrypt-Verschlüsselung
  - Passwort-Reset mit zeitlich begrenzten Tokens
  - Zwei-Faktor-Authentifizierung (TOTP/Authenticator-App)
  - Admin-Panel zur Benutzerverwaltung
  - Brute-Force-Schutz mit Rate Limiting

- 🌍 **Mehrsprachigkeit**
  - Deutsch, Englisch, Arabisch (RTL-Layout)
  - Automatische Spracherkennung
  - Lokalisierte Zahlformate

- 🎨 **Modernes UI**
  - Responsive Navigation
  - Dunkles Theme (anpassbar)
  - Mobile-optimiert
  - Versteckte Sidebar (Top-Nav-Menü)

- 📊 **Umfangreiche Finanz-Rechner**
  - Budgetrechner
  - Nebenkostenrechner
  - Finanzierungsrechner

- ✅ **Checklisten & Favoriten**
  - Immobilien-Favoritenliste
  - Phase-basierte Checklisten
  - To-Do-Listen für Renovierung & Umzug

## Voraussetzungen

- Python 3.9+ (getestet mit 3.13)
- `pip` zum Installieren der Abhängigkeiten

## 🚀 Schnellstart

### 1. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 2. Admin-Benutzer erstellen (beim ersten Start)

```bash
python scripts/init_admin.py
```

Folge den Anweisungen, um einen Admin-Benutzer zu erstellen.

### 3. App lokal starten

```bash
streamlit run app.py
```

Die App öffnet sich dann unter `http://localhost:8501`.

### 4. Anmelden

Melde dich mit dem erstellten Admin-Benutzer an.

## 🏗️ Projektstruktur

```
ImmoGuide/
├── app.py                    # Haupteinstiegspunkt (Startseite)
├── auth.py                   # Login/Registrierung/2FA-Logik
├── db.py                     # SQLite-Datenbankoperationen
├── i18n.py                   # Übersetzungen & Sprachmanagement
├── utils.py                  # UI-Utilities, Formatierungen
├── requirements.txt          # Python-Abhängigkeiten
├── Dockerfile                # Docker-Image-Definition
├── .streamlit/
│   ├── config.toml          # Streamlit-Konfiguration
│   └── users.db             # SQLite-Benutzerdatenbank (wird erzeugt)
├── pages/
│   ├── 0_Admin.py           # Admin-Panel (für Admins nur)
│   ├── 1_Vor_dem_Kauf.py    # Phase 1: Vorbereitung & Budgetierung
│   ├── 2_Waehrend_des_Kaufs.py  # Phase 2: Kauf-Prozess
│   └── 3_Nach_dem_Kauf.py   # Phase 3: Post-Purchase
├── scripts/
│   ├── init_admin.py        # Erstellt ersten Admin-Benutzer
│   ├── build_exe.ps1        # Build-Skript für .exe (Windows)
│   └── build_installer.ps1  # Installer-Build (Windows)
└── docs/
    ├── password-reset.md    # Passwort-Reset-Dokumentation
    └── ...
```

## 🔐 Sicherheit

### Authentifizierung

- **Passwort-Hashing**: Alle Passwörter werden mit bcrypt (Kosten-Faktor 12) gehashed
- **Passwort-Reset**: Zeitlich begrenzte Tokens (30 Min. Standard)
- **TOTP 2FA**: Optional pro Benutzer aktivierbar (Authenticator-App kompatibel)
- **Brute-Force-Schutz**: Rate Limiting auf Login-Endpoint

### Datenspeicherung

- **SQLite-Datenbank**: Lokal im `.streamlit/users.db` mit folgendem Schema:
  - `users` – Benutzer mit gehashten Passwörtern
  - `reset_tokens` – Zeitlich begrenzte Reset-Tokens
  - `rate_limits` – Login-Versuche (Brute-Force-Schutz)

## 📋 Benutzerverwaltung

### Admin-Panel

Nur Administratoren können auf `pages/0_Admin.py` zugreifen:

- 👥 Benutzer-Verwaltung
  - Alle Benutzer auflisten
  - Admin-Status vergeben/entfernen
  - Benutzer löschen

- ⚙️ Systemeinstellungen
  - Datenspeicher-Info
  - Sicherheits-Hinweise

- 📊 Statistiken
  - Gesamte Benutzeranzahl
  - Admin/Normal-Benutzer-Aufteilung

## 🌐 Streamlit Cloud (empfohlen für einfache Bereitstellung)

1. Code in ein Git-Repository (z. B. GitHub) pushen.
2. Stelle sicher, dass `requirements.txt` vorhanden ist.
3. In [Streamlit Community Cloud](https://share.streamlit.io) das Repository verbinden und `app.py` als Einstieg festlegen.
4. Optional: `.streamlit/config.toml` anpassen (Theme, Sprache, etc.).

### ⚠️ Wichtig für Cloud

Schreibzugriffe auf das Dateisystem sind in Cloud-Umgebungen oft flüchtig. Für produktive, mehrbenutzerfähige Szenarien wird eine echte Datenbank (z. B. PostgreSQL) statt SQLite empfohlen.

**Streamlit Secrets für SMTP** (`.streamlit/secrets.toml`):

```toml
[smtp]
host = "smtp.example.com"
port = 587
user = "smtp-user"
password = "smtp-pass"
from = "no-reply@example.com"
use_tls = true

disable_registration = false
```

## 🐳 Docker-Bereitstellung

### Container bauen

```bash
docker build -t meinimmokauf:latest .
```

### Container starten

```bash
docker run -p 8501:8501 --name meinimmokauf meinimmokauf:latest
```

Öffne `http://localhost:8501` im Browser.

### Mit persistentem Nutzerspeicher

```bash
docker run -p 8501:8501 -v $(pwd)/.streamlit:/app/.streamlit meinimmokauf:latest
```

**Windows (PowerShell)**:

```powershell
docker run -p 8501:8501 -v ${PWD}/.streamlit:/app/.streamlit meinimmokauf:latest
```

## 🔧 Umgebungsvariablen

```bash
# Registrierung deaktivieren
export DISABLE_REGISTRATION=true

# Reset-Token im UI anzeigen (nur für Testing!)
export SHOW_RESET_TOKEN_INLINE=true
```

## 📝 Produktionseinstellungen

### Registrierung deaktivieren

Option 1 – Umgebungsvariable:
```bash
export DISABLE_REGISTRATION=true
```

Option 2 – Streamlit Secrets (`.streamlit/secrets.toml`):
```toml
disable_registration = true
```

Wenn deaktiviert, wird der „Registrieren"-Tab ausgeblendet.

### SMTP für E-Mail-Versand (optional)

Konfiguriere in `.streamlit/secrets.toml`:

```toml
[smtp]
host = "smtp.gmail.com"
port = 587
user = "your-email@gmail.com"
password = "your-app-password"
from = "noreply@example.com"
use_tls = true
```

Der Versand erfolgt nur, wenn der Benutzer eine E-Mail hinterlegt hat.

## 🌍 Mehrsprachigkeit

Die App unterstützt automatisch:

- 🇩🇪 **Deutsch** (Standard)
- 🇬🇧 **English**
- 🇸🇦 **العربية** (Arabisch mit RTL)

Die Sprache wird über die URL-Parameter (`?lang=de|en|ar`) oder das Selectbox-Menü gewechselt.

## 📱 Mobile-Unterstützung

Die App ist vollständig responsive und optimiert für Tablets und Mobilgeräte:

- Top-Navigation statt Sidebar
- Angepasste Spalten-Layouts
- Touch-friendly Buttons

## 🐛 Debugging

### Logs anschauen

```bash
streamlit run app.py --logger.level=debug
```

### Session State inspizieren

Im Admin-Panel ist ein Debug-Bereich mit Session-State-Informationen verfügbar.

## 📖 Weitere Dokumentation

- `docs/password-reset.md` – Detaillierte Erklärung zum Passwort-Reset
- `docs/build-exe.md` – Anleitung zum Bauen einer Windows .exe
- `docs/publish-mobile.md` – Mobile App Deployment
- `docs/windows-installer.md` – Windows Installer erstellen

## 🤝 Lizenz

Dieses Projekt ist intern entwickelt worden. Alle Rechte vorbehalten.

## 📞 Support

Für Fragen und Fehlermeldungen bitte im internen Ticketing-System melden.

---

**Version**: 2.0 (vollständig überarbeitet)  
**Zuletzt aktualisiert**: November 2025
