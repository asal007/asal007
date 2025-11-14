# MeinImmoKauf – Setup- und Administrations-Anleitung

## 📋 Inhaltsverzeichnis

1. [Erste Schritte](#erste-schritte)
2. [Admin-Benutzer erstellen](#admin-benutzer-erstellen)
3. [SMTP-Konfiguration](#smtp-konfiguration)
4. [Datenbank-Verwaltung](#datenbank-verwaltung)
5. [Fehlerbehandlung](#fehlerbehandlung)
6. [Sicherheits-Best-Practices](#sicherheits-best-practices)

---

## Erste Schritte

### Schritt 1: Python-Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 2: Optionale virtuelle Umgebung (empfohlen)

**Windows (PowerShell)**:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**macOS/Linux**:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Schritt 3: Admin-Benutzer erstellen

```bash
python scripts/init_admin.py
```

Folgen Sie den Anweisungen:
- Geben Sie einen Benutzernamen ein (min. 3 Zeichen)
- Geben Sie ein Passwort ein (min. 6 Zeichen)
- Wiederholen Sie das Passwort

Nach erfolgreicher Erstellung können Sie sich anmelden.

### Schritt 4: App starten

```bash
streamlit run app.py
```

Die App öffnet sich unter `http://localhost:8501`.

---

## Admin-Benutzer erstellen

### Methode 1: Init-Skript (empfohlen)

```bash
python scripts/init_admin.py
```

### Methode 2: Manuell über Streamlit-UI

1. Starten Sie die App: `streamlit run app.py`
2. Gehen Sie zum Tab "Registrieren"
3. Erstellen Sie einen neuen Benutzer
4. Melden Sie sich mit diesem Benutzer an
5. Öffnen Sie die App mit: `python scripts/make_admin.py <username>`

### Methode 3: Python-Shell

```python
from db import init_db, add_user, set_admin
from auth import hash_password

init_db()
hashed = hash_password("your_password")
add_user("admin_user", hashed)
set_admin("admin_user", True)
print("✓ Admin erstellt!")
```

---

## SMTP-Konfiguration

Passwort-Reset per E-Mail benötigt SMTP-Konfiguration.

### Schritt 1: `secrets.toml` erstellen/bearbeiten

Erstelle oder bearbeite `.streamlit/secrets.toml`:

```toml
[smtp]
host = "smtp.gmail.com"
port = 587
user = "your-email@gmail.com"
password = "your-app-password"
from = "noreply@example.com"
use_tls = true
```

### Gmail-spezifische Anweisungen

1. Aktiviere "Less secure app access" oder verwende "App Passwords":
   - Gehe zu https://myaccount.google.com/security
   - Aktiviere "2-Step Verification"
   - Generiere ein "App Password" für E-Mail
   - Kopiere das Passwort in `secrets.toml`

### Alternative E-Mail-Provider

**Sendgrid**:
```toml
[smtp]
host = "smtp.sendgrid.net"
port = 587
user = "apikey"
password = "SG.your-sendgrid-api-key"
from = "noreply@example.com"
use_tls = true
```

**Postmark**:
```toml
[smtp]
host = "smtp.postmarkapp.com"
port = 587
user = "your-postmark-api-key"
password = "your-postmark-api-key"
from = "noreply@example.com"
use_tls = true
```

### Schritt 2: Reset-Token mit E-Mail testen

1. Gehen Sie zum Tab "Passwort vergessen"
2. Geben Sie einen Benutzernamen und E-Mail-Adresse ein
3. Klicken Sie "Token erstellen"
4. Überprüfen Sie Ihr E-Mail-Postfach

Falls die E-Mail nicht ankommt:
- Prüfen Sie Spam-Ordner
- Überprüfen Sie SMTP-Credentials
- Nutzen Sie `SHOW_RESET_TOKEN_INLINE=true` zum Debuggen

---

## Datenbank-Verwaltung

### Datenbankort

SQLite-Datenbank: `.streamlit/users.db`

### Datenbank-Schema

```sql
-- Benutzer
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email TEXT,
    totp_secret TEXT,
    is_admin INTEGER DEFAULT 0,
    created_at TEXT,
    updated_at TEXT
);

-- Reset-Tokens
CREATE TABLE reset_tokens (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT
);

-- Rate-Limiting
CREATE TABLE rate_limits (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    endpoint TEXT NOT NULL,
    attempt_count INTEGER,
    first_attempt TEXT
);

-- Favoriten
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    title TEXT,
    price REAL,
    location TEXT,
    sqm REAL,
    energy_class TEXT,
    condition TEXT,
    notes TEXT,
    created_at TEXT
);

-- To-Dos
CREATE TABLE todos (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    category TEXT,
    text TEXT,
    done INTEGER DEFAULT 0,
    created_at TEXT
);
```

### Datenbank-Backup

```bash
# Linux/macOS
cp .streamlit/users.db .streamlit/users.db.backup

# Windows (PowerShell)
Copy-Item .streamlit/users.db -Destination .streamlit/users.db.backup
```

### Datenbank zurücksetzen (Vorsicht!)

```bash
# Lösche die Datenbank (ALLE Daten gehen verloren!)
rm .streamlit/users.db

# oder Windows (PowerShell):
Remove-Item .streamlit/users.db -Force
```

---

## Fehlerbehandlung

### "Authentifizierung fehlgeschlagen"

- Überprüfen Sie Benutzernamen und Passwort
- Prüfen Sie, ob der Benutzer existiert: `.streamlit/users.db`
- Versuchen Sie, sich neu anzumelden

### "TOTP-Code ungültig"

- Prüfen Sie, dass die Systemzeit korrekt ist
- Regenerieren Sie den TOTP-Secret im Admin-Panel

### "Token ist ungültig oder abgelaufen"

- Reset-Tokens sind nur 30 Minuten gültig
- Fordern Sie einen neuen Token an

### "E-Mail konnte nicht versendet werden"

- Prüfen Sie `.streamlit/secrets.toml` auf SMTP-Konfiguration
- Überprüfen Sie Benutzername und Passwort
- Überprüfen Sie die Benutzer-E-Mail-Adresse
- Aktivieren Sie Debug mit: `SHOW_RESET_TOKEN_INLINE=true`

### "Registrierung ist deaktiviert"

Prüfen Sie folgende Einstellungen:
- Umgebungsvariable: `DISABLE_REGISTRATION=true`
- `.streamlit/secrets.toml`: `disable_registration = true`

Um Registrierung zu aktivieren, entfernen Sie diese Einstellungen.

---

## Sicherheits-Best-Practices

### 1. Passwort-Sicherheit

✅ **Best Practice**:
- Mindestlänge: 12+ Zeichen
- Großbuchstaben, Kleinbuchstaben, Zahlen, Sonderzeichen
- Regelmäßige Passwort-Wechsel

⚠️ **Warnung**:
- Speichern Sie Passwörter NICHT im Code oder Version Control
- Nutzen Sie `.streamlit/secrets.toml` für sensible Daten
- Fügen Sie `secrets.toml` in `.gitignore` hinzu

### 2. SMTP-Sicherheit

✅ **Best Practice**:
- Verwenden Sie "App Passwords" statt echte Passwörter
- Aktivieren Sie `use_tls = true`
- Nutzen Sie Streamlit Secrets, nicht Umgebungsvariablen

⚠️ **Warnung**:
- Speichern Sie SMTP-Passwörter NICHT im Code

### 3. Admin-Account

✅ **Best Practice**:
- Verwenden Sie starke Passwörter
- Aktivieren Sie 2FA für Admin
- Begrenzen Sie Admin-Konten auf notwendig

⚠️ **Warnung**:
- Löschen Sie NICHT den letzten Admin-Account

### 4. Datenbank-Sicherheit

✅ **Best Practice**:
- Regelmäßige Backups erstellen
- Dateiberechtigungen korrekt setzen (`.streamlit/` sollte nicht öffentlich zugänglich sein)
- Rate Limiting nutzen

⚠️ **Warnung**:
- `.streamlit/users.db` enthält sensible Daten
- Nicht in öffentliche Repositories committen

### 5. Deployment-Sicherheit

**Local/Entwicklung**:
```bash
streamlit run app.py --logger.level=debug
```

**Produktion**:
```bash
streamlit run app.py --client.toolbarMode=minimal
```

---

## Umgebungsvariablen (Referenz)

| Variable | Wert | Beschreibung |
|----------|------|-------------|
| `DISABLE_REGISTRATION` | `true`/`false` | Registrierung deaktivieren |
| `SHOW_RESET_TOKEN_INLINE` | `true`/`false` | Token im UI zeigen (nur Test!) |
| `STREAMLIT_SERVER_PORT` | `8501` | Port für Streamlit-Server |
| `STREAMLIT_SERVER_ADDRESS` | `localhost` | Server-Adresse |

---

## Support & Debugging

### Logs anschauen

```bash
streamlit run app.py --logger.level=debug
```

### Session-State prüfen

Öffnen Sie Admin-Panel → "Debug-Informationen anzeigen"

### Datenbankinhalt prüfen

```bash
# SQLite CLI
sqlite3 .streamlit/users.db

# Alle Benutzer auflisten:
SELECT username, email, is_admin FROM users;

# Benutzer löschen:
DELETE FROM users WHERE username = 'username';
```

---

**Fragen?** Kontaktieren Sie den Administrator oder schauen Sie in die Logs.
