# 🚀 Schritt 1: GitHub + Render Setup

**Geschätzte Zeit:** 25-30 Minuten

## Überblick

```
MeinImmoKauf (lokal)
         ↓
    git push
         ↓
    GitHub Repo
         ↓
    Render erkennt Auto-Deployment
         ↓
    App auf HTTPS-URL gehostet ✅
    (z.B. https://meinimmokauf.onrender.com)
```

---

## Phase 1: GitHub Repository erstellen (5 min)

### 1.1 Neues Repository
1. Gehe zu: **https://github.com/new**
2. Melde dich an (oder registriere dich)
3. Fülle aus:

| Feld | Wert |
|------|------|
| Repository name | `meinimmokauf` |
| Description | `MeinImmoKauf - Ratgeber für Immobilienkauf` |
| Visibility | **Public** ✅ (Render braucht Zugriff) |
| Initialize | **Nein** (wir committen lokal) |

4. Klick: **"Create repository"**

### 1.2 Repository URL kopieren
Nach Erstellung siehst du die URL:
```
https://github.com/DEIN-USERNAME/meinimmokauf.git
```
→ **SPEICHERE DIESE URL** (brauchst du gleich)

---

## Phase 2: Git lokal einrichten (10 min)

### 2.1 Öffne PowerShell/Terminal

**Windows:** `Windows-Taste` → `PowerShell` → `Enter`

### 2.2 Befehle nacheinander ausführen

```powershell
# 1. In den App-Ordner gehen
cd c:\Users\KAsys\Desktop\ImmoGuide

# 2. Git Repository initialisieren
git init

# 3. Alle Dateien hinzufügen
git add .

# 4. Ersten Commit erstellen
git commit -m "Initial commit: MeinImmoKauf v1.0 - Ready for Play Store"

# 5. Main Branch setzen
git branch -M main

# 6. GitHub verbinden (ERSETZE DEIN-USERNAME!)
git remote add origin https://github.com/DEIN-USERNAME/meinimmokauf.git

# 7. Zu GitHub pushen
git push -u origin main
```

### 2.3 Sicherheitsabfrage

Beim ersten `git push` wird dich GitHub fragen:
- **Option 1:** Browser öffnet sich → "Authorize GitHub"
- **Option 2:** Personal Access Token eingeben (Settings → Developer Settings)

### 2.4 Erfolg prüfen

Nach `git push` solltest du sehen:
```
✓ main -> main
✓ Branch 'main' set up to track remote 'origin/main'
```

Prüfe auf GitHub: **https://github.com/DEIN-USERNAME/meinimmokauf**
→ Deine Dateien sollten dort sein! ✅

---

## Phase 3: Render Web Service (10 min)

### 3.1 Render.com Account erstellen
1. Gehe zu: **https://render.com/register**
2. Klick: **"Sign up with GitHub"**
3. Authorize Render
4. Bestätige E-Mail (falls nötig)

### 3.2 Web Service erstellen
1. Render Dashboard öffnen
2. Klick: **"New"** (oben rechts)
3. Wähle: **"Web Service"**

### 3.3 GitHub Repository verbinden
1. Klick: **"Connect to GitHub"**
2. Wähle Repository: **"meinimmokauf"**
3. Authorize Render (falls noch nicht)

### 3.4 Web Service konfigurieren

Fülle folgende Felder aus:

| Feld | Wert |
|------|------|
| **Name** | `meinimmokauf` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=10000 --server.address=0.0.0.0` |
| **Instance Type** | `Free` (mit Auto-Sleep) oder `Paid` ($7/Mo) |

### 3.5 Environment Variables (Optional)
Klick: **"Environment"** → Add Variable

```
STREAMLIT_SERVER_HEADLESS  =  true
STREAMLIT_SERVER_PORT      =  10000
```

### 3.6 Starten
Klick: **"Create Web Service"**

Render startet automatisch den Deploy! 🚀

---

## Phase 4: Deploy warten (5-10 min)

### 4.1 Logs beobachten
- Render Dashboard zeigt Live-Logs
- Suche nach: `"Listening on"`
- Status sollte: `"Running"` sein

### 4.2 Deploy-URL anzeigen lassen
Nach erfolgreichem Deploy siehst du oben:
```
https://meinimmokauf.onrender.com
```

Die exakte URL wird dir in Render angezeigt (kann unterschiedlich sein)

---

## Phase 5: capacitor.config.ts aktualisieren (5 min)

### 5.1 Datei öffnen
Öffne in VS Code:
```
mobile/capacitor.config.ts
```

### 5.2 URL eintragen
Suche diese Zeile:
```typescript
server: {
  url: 'https://DEINE-PRODUKTIONS-URL.com',
  cleartext: false,
}
```

Ersetze durch:
```typescript
server: {
  url: 'https://meinimmokauf.onrender.com',  // ← DEINE RENDER-URL!
  cleartext: false,
}
```

### 5.3 Speichern & Committen
```powershell
git add mobile/capacitor.config.ts
git commit -m "Update Capacitor server URL to production"
git push
```

---

## Phase 6: Test (5 min)

### 6.1 Öffne Browser
```
https://meinimmokauf.onrender.com
```

### 6.2 Test-Schritte
- [ ] Seite lädt (kann 15-20 Sekunden dauern)
- [ ] Login funktioniert: `admin` / `admin1234`
- [ ] Favoriten speichern geht
- [ ] Zu Seite 1 navigieren geht
- [ ] Logout funktioniert
- [ ] Admin-Panel erreichbar (in der UI-Ecke)

### 6.3 Fehlerbehandlung

**Problem: 503 Service Unavailable**
- Render schläft (Free Plan)
- **Fix:** 2-3 Minuten warten, dann nochmal laden
- Cache löschen: `Ctrl+Shift+R`

**Problem: 404 Not Found**
- URL falsch?
- **Fix:** Render Dashboard öffnen, richtige URL kopieren

**Problem: Login schlägt fehl**
- Datenbank-Issue?
- **Fix:** Render Logs prüfen (Dashboard → Logs)

---

## ✅ Erfolgskriterien

- ✅ GitHub Repository online
- ✅ Render Web Service "Running"
- ✅ HTTPS-URL funktioniert
- ✅ Login & Navigation funktionieren
- ✅ capacitor.config.ts aktualisiert

---

## 🎯 Nächste Schritte

Wenn alles funktioniert:

1. **Notiere deine Render-URL:**
   ```
   https://meinimmokauf.onrender.com
   ```
   (Diese brauchst du später für Play Store!)

2. **Weiter zu Schritt 2:** Google Play Console Setup
   - Siehe: `GOOGLE_PLAY_STORE_READY.md`

3. **Build & AAB erstellen:**
   - Siehe: `docs/build-guide.md`

---

## 💡 Tipps

- **Render Free Plan:**
  - Auto-Sleep nach 15 min inaktiv
  - Erste Load: 15-20 Sekunden (Cold Start)
  - Das ist OK für Beta/Testing
  
- **Render Paid Plan ($7/Mo):**
  - Keine Sleep-Zeiten
  - Bessere Performance
  - Lohnt sich für Production

- **Datenbank:**
  - SQLite funktioniert, aber Backups manuell!
  - Für Production: PostgreSQL empfohlen
  - Render hat kostenlose PostgreSQL-Tier

- **Secrets:**
  - SMTP-Credentials über Environment Variables, nicht in Code!
  - Render Dashboard → Secrets-Option verwenden

---

## 📞 Support

Probleme? Schau hier:
- `docs/deployment-anleitung.md` - Alle Deployment-Optionen
- `GOOGLE_PLAY_STORE_READY.md` - Komplette Checkliste
- Render Docs: https://render.com/docs

**Status:** ✅ Ready for Step 2!
