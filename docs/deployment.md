# MeinImmoKauf – Deployment-Anleitung

Dieses Dokument beschreibt verschiedene Methoden, um MeinImmoKauf in Produktion zu nehmen.

## Übersicht Deployment-Optionen

| Methode | Kosten | Benutzer | Skalierbarkeit | Datenbank | Best für |
|---------|--------|----------|----------------|-----------|----------|
| **Lokal** | €0 | 1-10 | Keine | SQLite | Entwicklung/Testing |
| **Streamlit Cloud** | €0-20 | 10-100+ | Mittel | SQLite (flüchtig!) | Kleine Teams |
| **Docker lokal** | €0 | 1-10 | Keine | SQLite | Docker-Umgebungen |
| **Docker + Postgres** | €5-50 | 100-1000 | Hoch | PostgreSQL | Produktiv |
| **VM (DigitalOcean, Linode)** | €5-50 | 100-1000 | Hoch | PostgreSQL | Vollständige Kontrolle |
| **Kubernetes** | €20-200 | 1000+ | Sehr hoch | PostgreSQL | Enterprise |

---

## 1. Lokal (Entwicklung)

### Installation

```bash
# Repository klonen
git clone <repo-url>
cd ImmoGuide

# Virtuelle Umgebung erstellen
python -m venv .venv
source .venv/bin/activate  # oder .venv\Scripts\Activate.ps1 auf Windows

# Abhängigkeiten installieren
pip install -r requirements.txt

# Admin-Benutzer erstellen
python scripts/init_admin.py

# App starten
streamlit run app.py
```

**Zugriff**: http://localhost:8501

---

## 2. Streamlit Cloud (Einfach, keine Infrastruktur)

### Voraussetzungen

- GitHub-Account
- Streamlit Community Cloud-Account (kostenlos)

### Schritte

1. **Repository auf GitHub hochladen**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/your-username/meinimmokauf.git
git push -u origin main
```

**Wichtig**: Stelle sicher, dass `secrets.toml` in `.gitignore` ist!

2. **In Streamlit Cloud verbinden**

- Gehe zu https://share.streamlit.io
- Klicke "New app"
- Wähle Repository, Branch und Datei: `app.py`
- Klicke "Deploy"

3. **Secrets konfigurieren**

Nach erfolgreichem Deploy:
- Klicke auf das Menü-Icon (oben rechts)
- Gehe zu "Settings" → "Secrets"
- Füge Inhalte von `.streamlit/secrets.toml` hinzu:

```toml
[smtp]
host = "smtp.gmail.com"
port = 587
user = "your-email@gmail.com"
password = "your-app-password"
from = "noreply@example.com"
use_tls = true

disable_registration = false
```

4. **Admin-Benutzer erstellen**

⚠️ **Problem**: Streamlit Cloud hat kein Terminal-Zugriff.

**Lösung**: 
- Erstelle einen normalen Benutzer über die Registrierung
- Schreibe einen Admin-Setup-Endpunkt oder nutze SQLite-Browser-Tool

### ⚠️ Wichtige Einschränkungen

- **Datenbank ist flüchtig**: Wird täglich zurückgesetzt
- **Keine persistente Speicherung**: Alle Daten gehen verloren
- **Kein Dateisystem**: `.streamlit/` ist nicht persistent

**Für produktive Nutzung wird PostgreSQL oder ähnliches empfohlen.**

---

## 3. Docker (Lokal oder Remote)

### Voraussetzungen

- Docker installiert

### Schritt 1: Image bauen

```bash
docker build -t meinimmokauf:latest .
```

### Schritt 2: Container starten

```bash
# Standard (ohne persistente Daten)
docker run -p 8501:8501 meinimmokauf:latest

# Mit persistenter Datenbank
docker run -p 8501:8501 \
  -v $(pwd)/.streamlit:/app/.streamlit \
  meinimmokauf:latest

# Windows (PowerShell)
docker run -p 8501:8501 `
  -v ${PWD}/.streamlit:/app/.streamlit `
  meinimmokauf:latest
```

### Schritt 3: Admin-Benutzer erstellen

```bash
# In den Container einsteigen
docker exec -it <container-id> /bin/bash

# Admin-Skript ausführen
python scripts/init_admin.py

# Container verlassen
exit
```

**Zugriff**: http://localhost:8501

---

## 4. Docker-Compose (mit Postgres für Produktion)

### Schritt 1: `docker-compose.yml` erstellen

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/meinimmokauf
    volumes:
      - ./.streamlit:/app/.streamlit
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=meinimmokauf
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Schritt 2: Starten

```bash
docker-compose up -d
```

---

## 5. DigitalOcean / Linode (VPS)

### Kosten

- **Droplet** (Ubuntu 22.04): €5-20/Monat
- **Postgresql Database**: €15-100/Monat

### Schritt 1: Droplet erstellen

1. Gehe zu https://www.digitalocean.com
2. Erstelle einen neuen Droplet (Ubuntu 22.04, $5/Monat)
3. SSH-Key hinzufügen oder Root-Password nutzen
4. Notiere die IP-Adresse

### Schritt 2: SSH-Verbindung

```bash
ssh root@<your-droplet-ip>
```

### Schritt 3: System aktualisieren

```bash
apt update && apt upgrade -y
apt install -y python3-pip python3-venv git
```

### Schritt 4: Repository klonen und Setup

```bash
git clone <repo-url> /opt/meinimmokauf
cd /opt/meinimmokauf
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scripts/init_admin.py
```

### Schritt 5: Systemd-Service erstellen

Erstelle `/etc/systemd/system/meinimmokauf.service`:

```ini
[Unit]
Description=MeinImmoKauf Streamlit App
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/meinimmokauf
Environment="PATH=/opt/meinimmokauf/venv/bin"
ExecStart=/opt/meinimmokauf/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### Schritt 6: Service starten

```bash
systemctl daemon-reload
systemctl start meinimmokauf
systemctl enable meinimmokauf
systemctl status meinimmokauf
```

### Schritt 7: Nginx als Reverse Proxy

```bash
apt install -y nginx
```

Erstelle `/etc/nginx/sites-available/meinimmokauf`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Aktiviere den Site:

```bash
ln -s /etc/nginx/sites-available/meinimmokauf /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

### Schritt 8: SSL mit Let's Encrypt

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d your-domain.com
```

**Zugriff**: https://your-domain.com

---

## 6. Datenbank-Migration (SQLite zu PostgreSQL)

Falls Sie später von SQLite zu PostgreSQL wechseln:

### Schritt 1: PostgreSQL-Datenbankmodule aktualisieren

```bash
pip install psycopg2-binary sqlalchemy
```

### Schritt 2: `db.py` anpassen

Ersetze SQLite-Logik durch PostgreSQL (nicht in diesem Guide enthalten).

### Schritt 3: Daten migrieren

```python
import sqlite3
import psycopg2

# SQLite lesen
sqlite_conn = sqlite3.connect('.streamlit/users.db')
sqlite_cursor = sqlite_conn.cursor()
sqlite_cursor.execute("SELECT * FROM users")
users = sqlite_cursor.fetchall()
sqlite_conn.close()

# PostgreSQL schreiben
pg_conn = psycopg2.connect("postgresql://user:password@localhost/meinimmokauf")
pg_cursor = pg_conn.cursor()
for user in users:
    pg_cursor.execute("""
        INSERT INTO users (username, password_hash, email, is_admin, created_at)
        VALUES (%s, %s, %s, %s, %s)
    """, user)
pg_conn.commit()
pg_cursor.close()
pg_conn.close()
```

---

## Checkliste für Produktion

- [ ] SMTP konfiguriert (`secrets.toml`)
- [ ] Admin-Account erstellt und gesichert
- [ ] `.streamlit/secrets.toml` in `.gitignore`
- [ ] Regelmäßige Backups eingerichtet
- [ ] SSL/HTTPS aktiviert (bei öffentlicher URL)
- [ ] Firewall konfiguriert (nur Port 80/443)
- [ ] Rate Limiting aktiviert
- [ ] Passwort-Reset getestet
- [ ] 2FA konfiguriert (optional)
- [ ] Monitoring/Logs eingerichtet

---

## Monitoring & Logs

### Streamlit Logs

```bash
# Streamlit Debug-Modus
streamlit run app.py --logger.level=debug

# Logs ansehen (Systemd)
journalctl -u meinimmokauf -f
```

### Docker Logs

```bash
docker logs <container-id> -f
```

---

## Problembehebung

### "Datenbank-Fehler beim Deploy"

- Stelle sicher, dass `.streamlit/` mit persistentem Volume gemountet ist
- Überprüfe Dateiberechtigungen

### "SMTP-Fehler"

- Überprüfe `secrets.toml` auf Streamlit Cloud
- Teste lokale SMTP-Verbindung: `telnet smtp.gmail.com 587`

### "App startet nicht"

- Logs überprüfen: `journalctl -u meinimmokauf -f`
- Abhängigkeiten neu installieren: `pip install -r requirements.txt`

---

**Fragen?** Kontaktieren Sie den Administrator.
