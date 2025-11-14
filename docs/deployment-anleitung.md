# Deployment Guide - MeinImmoKauf

Diese Anleitung zeigt die beste Methode, um die Streamlit-App produktiv zu hosten (HTTPS-URL für Mobile Wrapper).

---

## 🎯 Übersicht: Deployment-Optionen

| Option | Kosten | Setup | Performance | HTTPS | Empfehlung |
|--------|--------|-------|-------------|-------|-----------|
| **Render** | ✅ Kostenlos (mit Sleep) | ⭐⭐ Einfach | ⭐⭐⭐ Gut | ✅ Ja | 🏆 Beste Anfänger-Option |
| **Fly.io** | ✅ Kostenlos (begrenzt) | ⭐⭐⭐ Mittel | ⭐⭐⭐⭐ Sehr gut | ✅ Ja | ⭐ Für Scale-up |
| **Railway** | ✅ $5-20/Mo | ⭐⭐ Einfach | ⭐⭐⭐ Gut | ✅ Ja | 📌 Gute Mitte |
| **AWS Lambda** | ❌ $10-50/Mo | ⭐⭐⭐ Komplex | ⭐⭐⭐⭐⭐ Optimal | ✅ Ja | 💼 Enterprise |
| **Docker (Selbst-gehostet)** | 💰 VPS $5-50/Mo | ⭐⭐⭐ Schwer | ⭐⭐⭐⭐ Gut | ⚠️ Mit SSL | 👨‍💼 Profi |

---

## Option 1️⃣: Render (EMPFOHLEN für Anfänger)

### Schritt 1: Render-Account erstellen
1. Gehe zu https://render.com
2. Registriere dich (kostenlos)
3. Verbinde GitHub (oder deployment direkt)

### Schritt 2: Neue Web Service erstellen
1. Klick auf **"New"** → **"Web Service"**
2. Wähle **"Build and deploy from a Git repository"**
3. Verbinde GitHub-Repo mit MeinImmoKauf

### Schritt 3: Konfigurieren
Fülle folgende Felder aus:

```
Name:              meinimmokauf
Environment:       Python 3
Build Command:     pip install -r requirements.txt
Start Command:     streamlit run app.py --server.port=10000 --server.address=0.0.0.0
Instance Type:     Free
```

### Schritt 4: Environment Variables (Secret)
Klick auf **"Environment"** und füge hinzu:

```
STREAMLIT_SERVER_PORT=10000
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
```

Falls SMTP für Passwort-Reset (optional):
```
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=deine-email@gmail.com
SMTP_PASSWORD=dein-app-passwort  # Google App Password!
```

### Schritt 5: Deploy
1. Klick auf **"Create Web Service"**
2. Warte auf Deploy (2-5 Minuten)
3. Erhältst automatisch URL: `https://meinimmokauf.onrender.com`

### Schritt 6: Custom Domain (optional)
1. Render Dashboard → Settings
2. Custom Domain → Domain-Name eingeben
3. DNS-Einträge aktualisieren

---

## Option 2️⃣: Fly.io (Für Scale-Up)

### Schritt 1: Fly.io-Account & CLI
```bash
# Install CLI
curl -L https://fly.io/install.sh | sh

# Anmelden
fly auth login

# Im MeinImmoKauf-Ordner:
fly launch

# Fragen:
# - App name: meinimmokauf
# - Region: Frankfurt (ams für Europa)
# - PostgreSQL/Redis: Nein (SQLite reicht)
```

### Schritt 2: fly.toml anpassen
Öffne `fly.toml`:

```toml
[app]
primary_region = "ams"

[[services]]
internal_port = 8501
protocol = "tcp"

[env]
STREAMLIT_SERVER_PORT = "8501"
STREAMLIT_SERVER_ADDRESS = "0.0.0.0"
```

### Schritt 3: Dockerfile (falls nicht existiert)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Schritt 4: Deploy
```bash
fly deploy
```

Result: `https://meinimmokauf.fly.dev`

---

## Option 3️⃣: Railway.app (Balance)

### Schritt 1: Railway-Account
1. Gehe zu https://railway.app
2. Registriere dich mit GitHub

### Schritt 2: Neues Projekt
1. Klick **"New Project"** → **"Deploy from GitHub"**
2. Wähle MeinImmoKauf-Repository

### Schritt 3: Konfigurieren
Railway auto-erkennt `requirements.txt` und `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=$PORT", "--server.address=0.0.0.0"]
```

### Schritt 4: Environment Variables
Im Railway Dashboard:

```
STREAMLIT_SERVER_HEADLESS=true
DATABASE_PATH=/tmp/meinimmokauf.db  # Railway hat /tmp
```

### Schritt 5: Domain
Railway bietet automatisch HTTPS: `https://meinimmokauf-prod.railway.app`

---

## Option 4️⃣: Docker Selbst-gehostet (VPS)

### Schritt 1: VPS mieten
- Anbieter: DigitalOcean, Linode, Hetzner, AWS
- Mindestens: 2GB RAM, 1 Core, Ubuntu 22.04
- Kosten: ~$5-10/Monat

### Schritt 2: SSH verbinden
```bash
ssh root@deine-vps-ip
```

### Schritt 3: Docker installieren
```bash
apt-get update
apt-get install -y docker.io docker-compose

# User-Permissionen
usermod -aG docker $USER
```

### Schritt 4: MeinImmoKauf clonen
```bash
git clone https://github.com/DEIN-USERNAME/meinimmokauf.git
cd meinimmokauf
```

### Schritt 5: docker-compose.yml erstellen
```yaml
version: '3.8'

services:
  streamlit:
    build: .
    ports:
      - "8501:8501"
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
      - DATABASE_PATH=/data/meinimmokauf.db
    volumes:
      - ./data:/data
    restart: always
    
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./certs:/etc/nginx/certs
    restart: always
    depends_on:
      - streamlit
```

### Schritt 6: Nginx mit SSL (Let's Encrypt)
```bash
# Certbot installieren
apt-get install -y certbot python3-certbot-nginx

# SSL-Zertifikat anfordern
certbot certonly --standalone -d meinimmokauf.de

# nginx.conf aktualisieren
```

### Schritt 7: Docker starten
```bash
docker-compose up -d
```

Result: `https://meinimmokauf.de`

---

## Option 5️⃣: AWS Lambda (Enterprise)

### Anforderungen
- AWS-Account mit Kreditkarte
- Containerimage (Docker)
- Costen: ~$20-50/Monat bei niedrigem Traffic

### Schritte (Übersicht)
1. Docker-Image zu **ECR** (Elastic Container Registry) pushen
2. **Lambda Function** erstellen
3. **API Gateway** als HTTP-Trigger
4. **CloudFront** + **ACM SSL** für HTTPS

**Komplexität:** ⭐⭐⭐⭐⭐ Nicht für Anfänger

---

## Recommended: Render + Custom Domain

### Finale Konfiguration für Mobile Wrapper:

**Render Setup:**
```
Build Command:     pip install -r requirements.txt
Start Command:     streamlit run app.py --server.port=10000 --server.address=0.0.0.0
Instance:          Free (mit Sleep) oder Paid ($7/Mo)
```

**capacitor.config.ts aktualisieren:**
```typescript
server: {
  url: 'https://deine-custom-domain.com',  // oder https://meinimmokauf.onrender.com
  cleartext: false,
}
```

**Build & Deploy:**
```bash
cd mobile
npm install
npx cap sync android
cd android
./gradlew bundleRelease
```

**Upload zu Play Store:**
- AAB: `mobile/android/app/build/outputs/bundle/release/app-release.aab`
- URL: Muss in Play Console hinterlegt sein

---

## ⚠️ Wichtige Hinweise

1. **HTTPS ist PFLICHT** für Mobile Wrapper
   - iOS blockiert unsichere Verbindungen
   - Android schränkt HTTP ein

2. **Database** für mobil
   - SQLite funktioniert, aber Backups nötig
   - Für Production: PostgreSQL empfohlen
   - Render/Fly bieten kostenlose DB-Options

3. **Secrets** (nicht in Git!)
   - `.streamlit/secrets.toml` → .gitignore
   - Environment Variables im Platform-Dashboard

4. **Cold Start** bei kostenlosen Plans
   - App kann beim ersten Request 30sec brauchen
   - Render: ~15sec, dann schnell
   - Acceptabel für User

---

## Checkliste Deployment

- [ ] Deployment-Plattform gewählt (Render/Fly/Railway/etc.)
- [ ] Git-Repository gepusht
- [ ] Web Service erstellt
- [ ] Environment Variables gesetzt
- [ ] Deploy erfolgreich (Status: Running)
- [ ] HTTPS-URL funktioniert
- [ ] Login funktioniert
- [ ] capacitor.config.ts aktualisiert
- [ ] AAB gebaut
- [ ] Play Console vorbereitet
- [ ] Ready für Submission!

---

## Troubleshooting

### App ist offline / 500 Error
```bash
# Render Logs prüfen
# Dashboard → Logs (oben rechts)
```

### Streamlit Port-Error
Stelle sicher, dass Port 10000 (oder $PORT) in build.gradle oder Server-Config stimmt.

### Database-Fehler auf Render
SQLite funktioniert, aber bei mehreren Instanzen können Locks auftreten.
**Lösung:** Zu PostgreSQL migrieren (Render bietet kostenlos!)

---

**Status:** Ready for Deployment 🚀
