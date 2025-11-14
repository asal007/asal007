# MeinImmoKauf – Versionshistorie & Änderungen

## Version 2.0 (November 2025) – Überarbeitete Version

### ✨ Neue Features

#### 🔐 Authentifizierung & Sicherheit
- ✅ **Login & Registrierung** mit Validierung
- ✅ **Passwort-Hashing** mit bcrypt (Kosten-Faktor 12)
- ✅ **Passwort-Reset** mit zeitlich begrenzten Tokens (30 Min.)
- ✅ **TOTP 2FA** (Zwei-Faktor-Authentifizierung via Authenticator-App)
- ✅ **Rate Limiting** gegen Brute-Force-Angriffe
- ✅ **Admin-Panel** zur Benutzerverwaltung
- ✅ **Profil-Einstellungen** (E-Mail, Passwort, 2FA)
- ✅ **SMTP-Integration** für E-Mail-basierte Passwort-Resets

#### 🌍 Mehrsprachigkeit
- ✅ Deutsch (Standard)
- ✅ Englisch
- ✅ Arabisch mit RTL-Layout
- ✅ Lokalisierte Zahlformate und Währungen

#### 🎨 UI/UX Verbesserungen
- ✅ Responsive Hamburger-Navigation (statt Sidebar)
- ✅ Dunkles Theme mit modernen Farben
- ✅ Mobile-optimiert (Tablets, Smartphones)
- ✅ Versteckte Header-Aktionen für Nicht-Admins
- ✅ Lokalisierte Datum/Zeit/Zahlformate

#### 💾 Datenpersistierung
- ✅ **SQLite-Datenbank** für Benutzer
- ✅ **Favoriten speichern** (Immobilien-Liste)
- ✅ **To-Dos persistieren** (Renovierung, Umzug)
- ✅ **Reset-Tokens** mit Verfallszeit
- ✅ **Rate-Limit-Tracking** für Sicherheit

#### 📊 Inhalte & Rechner
- ✅ **Budgetrechner** (max. Kaufpreis basierend auf Einkommen)
- ✅ **Nebenkostenrechner** (Steuern, Notar, Makler pro Bundesland)
- ✅ **Finanzierungsrechner** (Monatliche Rate, Gesamtzinsen)
- ✅ **Favoritenliste** mit Bildergalerie
- ✅ **Phase-basierte Checklisten** (Vor/Während/Nach dem Kauf)
- ✅ **To-Do-Listen** für Renovierung & Umzug

### 📁 Neue/Geänderte Dateien

```
✨ Neu:
├── auth.py                  # Login, Registrierung, 2FA, Profil
├── db.py                    # SQLite-Datenbankoperationen
├── .streamlit/config.toml   # Streamlit-Theme-Konfiguration
├── docs/setup.md            # Setup- & Admin-Anleitung
├── docs/architecture.md     # Technische Dokumentation
├── docs/deployment.md       # Deployment-Optionen
├── scripts/test_setup.py    # Test-Skript zum Validieren

📝 Geändert:
├── app.py                   # + Auth-Gate, Top-Navigation
├── pages/0_Admin.py         # Neu: Admin-Panel
├── pages/1_Vor_dem_Kauf.py  # + Auth-Gate
├── pages/2_Waehrend_des_Kaufs.py  # + Auth-Gate
├── pages/3_Nach_dem_Kauf.py # + Auth-Gate
├── requirements.txt         # Neue Abhängigkeiten (bcrypt, pyotp)
├── .gitignore              # + users.db, secrets.toml
└── README.md               # Vollständig überarbeitet
```

### 🔐 Sicherheit

#### Neue Sicherheitsmaßnahmen
- Bcrypt-Hashing für Passwörter (nicht plaintext!)
- TOTP-basierte 2FA
- Zeitlich begrenzte Reset-Tokens
- Rate Limiting gegen Brute-Force
- Session-basierte Authentifizierung
- Secrets-Management für SMTP & API-Keys

#### Best Practices implementiert
- Validierung aller Eingaben
- Exception-Handling auf allen Ebenen
- Separation of Concerns (auth, db, i18n, utils)
- Keine Credentials im Code

### 📊 Datenbankschema

```sql
-- Neue Tabellen:
users            -- Benutzer mit gehashten Passwörtern
reset_tokens     -- Passwort-Reset-Tokens mit TTL
rate_limits      -- Login-Versuche (Brute-Force-Schutz)
favorites        -- Immobilien-Favoriten
todos            -- To-Do-Listen pro Benutzer & Kategorie
```

### 🚀 Deployment-Optionen

Neue Dokumentation für folgende Optionen:
1. **Lokal** (Entwicklung) – SQLite
2. **Streamlit Cloud** (Kostenlos) – Für kleine Teams
3. **Docker** (Self-Hosted) – SQLite oder PostgreSQL
4. **VPS** (DigitalOcean, Linode) – PostgreSQL + Nginx
5. **Kubernetes** – Enterprise-Grade

### 🐛 Behobene Probleme

- ✅ Keine Persistierung von Daten zwischen Sessions → SQLite-DB
- ✅ Keine Authentifizierung → Login & 2FA implementiert
- ✅ Admin-Features → Admin-Panel erstellt
- ✅ Sprachprobleme in RTL-Sprachen → Arabisch-Unterstützung
- ✅ Mobile nicht optimiert → Responsive Design
- ✅ Keine E-Mail-Integration → SMTP-Support

### 📈 Performance-Verbesserungen

- Caching von Übersetzungen
- Optimierte DB-Queries
- Lazy-Loading von Seiten
- Reduzierte Session-State-Größe

### 💥 Breaking Changes

- **Auth-Gate**: Apps erfordern jetzt Login
- **Session-State**: Favoriten/Todos sind jetzt in DB, nicht in Session
- **Admin-Features**: Versteckt für normale Benutzer

### 🔄 Migration von v1.x

Falls Sie von einer älteren Version aktualisieren:

1. **Backup erstellen**: `.streamlit/users.db` wird neu erstellt
2. **Dependencies aktualisieren**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Admin-Benutzer erstellen**:
   ```bash
   python scripts/init_admin.py
   ```
4. **App starten**:
   ```bash
   streamlit run app.py
   ```

---

## Version 1.0 (Frühere Versionen)

### Basis-Features
- Phase 1, 2, 3 Seiten
- Grundlegende Rechner (Budget, Nebenkos­ten, Finanzierung)
- Deutschen UI
- Keine Authentifizierung
- Session-basierte Datenspeicherung

---

## 🗺️ Roadmap für kommende Versionen

### Version 2.1 (Geplant)
- [ ] PostgreSQL-Support
- [ ] Advanced 2FA (Biometrie)
- [ ] Datei-Upload für Dokumente
- [ ] E-Mail-Benachrichtigungen für Aufgaben
- [ ] API für externe Integrationen

### Version 3.0 (Geplant)
- [ ] Mobile-App (Flutter/React Native)
- [ ] Dashboard mit Statistiken
- [ ] Kollaborative Features (Familie laden)
- [ ] Integration mit Immobilien-APIs
- [ ] Video-Tutorials

---

## 🤝 Lizenz

© 2025 – Alle Rechte vorbehalten

---

**Fragen zur Version? Kontaktieren Sie den Entwickler.**
