# MeinImmoKauf – Architektur-Dokumentation

## 🏗️ System-Architektur

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                    │
│  (Browser-basiert, Responsive UI, Multi-Language)       │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Server                       │
│         (app.py, pages/*, auth.py, i18n.py, utils.py)   │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┬─────────────────┐
        │                         │                 │
        ▼                         ▼                 ▼
   ┌─────────────┐         ┌───────────────┐  ┌────────────┐
   │   db.py     │         │  auth.py      │  │ Secrets /  │
   │  (SQLite)   │         │  (bcrypt,     │  │ SMTP       │
   │             │         │   pyotp)      │  │            │
   │ ┌─────────┐ │         │               │  │            │
   │ │ users   │ │         │               │  │            │
   │ │ favorites│ │         │               │  │            │
   │ │ todos   │ │         │               │  │            │
   │ └─────────┘ │         │               │  │            │
   └─────────────┘         └───────────────┘  └────────────┘
```

---

## 📁 Dateistruktur

```
ImmoGuide/
├── app.py                          # Startseite / Haupteinstieg
├── auth.py                         # Authentifizierung & Profil
├── db.py                          # Datenbankoperationen
├── i18n.py                        # Übersetzungen (DE/EN/AR)
├── utils.py                       # UI-Utilities, Formatierungen
├── requirements.txt               # Python-Abhängigkeiten
├── Dockerfile                     # Docker-Containerisierung
├── .gitignore                     # Git-Ignoriere-Regeln
├── .streamlit/
│   ├── config.toml               # Streamlit-Konfiguration
│   ├── secrets.toml              # SMTP & Credentials (GIT-IGNORED)
│   └── users.db                  # SQLite-Datenbank
├── pages/
│   ├── 0_Admin.py               # Admin-Panel
│   ├── 1_Vor_dem_Kauf.py        # Phase 1: Budget & Vorbereitung
│   ├── 2_Waehrend_des_Kaufs.py  # Phase 2: Kauf-Prozess
│   └── 3_Nach_dem_Kauf.py       # Phase 3: Post-Purchase
├── scripts/
│   ├── init_admin.py            # Erstellt ersten Admin-Benutzer
│   ├── make_admin.py            # Nutzer zu Admin befördern
│   ├── build_exe.ps1            # Windows EXE-Builder
│   └── build_installer.ps1      # Windows Installer-Builder
└── docs/
    ├── setup.md                 # Setup- & Admin-Anleitung
    ├── deployment.md            # Deployment-Optionen
    ├── architecture.md          # Diese Datei
    ├── password-reset.md        # Passwort-Reset-Erklärung
    ├── build-exe.md             # EXE-Build-Anleitung
    ├── publish-mobile.md        # Mobile App-Publikation
    └── windows-installer.md     # Windows Installer-Guide
```

---

## 🔄 Datenfluss

### 1. Login-Flow

```
┌──────────┐
│ Benutzer │
└────┬─────┘
     │ Benutzername + Passwort
     ▼
┌────────────────────────┐
│  login_gate() in auth  │
└────┬───────────────────┘
     │ Verifizieren
     ▼
┌─────────────────────────────────────┐
│  verify_password() + bcrypt.checkpw │
└────┬────────────────────────────────┘
     │
     ├─ Fail → error_message
     │
     └─ Success:
         ├─ TOTP aktiviert?
         │  ├─ Ja → ask_for_code()
         │  └─ Nein → next
         └─ st.session_state["auth_user"] = username
            └─ st.rerun()
```

### 2. Registrierungs-Flow

```
┌──────────┐
│ Benutzer │
└────┬─────┘
     │ Neuer Username + Passwort
     ▼
┌──────────────────────────┐
│ Validierungen            │
├──────────────────────────┤
│ - Min 6 Zeichen Passwort │
│ - Username existiert?    │
│ - Registrierung aktiv?   │
└────┬─────────────────────┘
     │
     ├─ Fail → error_message
     │
     └─ Success:
         ├─ hash_password()
         ├─ add_user() → DB
         └─ success_message
```

### 3. Passwort-Reset-Flow

```
┌──────────┐
│ Benutzer │
└────┬─────┘
     │ "Passwort vergessen"
     ▼
┌──────────────────────────┐
│ request_password_reset() │
└────┬─────────────────────┘
     │
     ├─ Benutzer existiert?
     │  └─ Nein → error
     │
     └─ Ja:
        ├─ Generiere Token (secrets.token_urlsafe)
        ├─ Token expires = now + 30 min
        ├─ Speichere in reset_tokens Tabelle
        └─ Sende E-Mail (via SMTP)
           └─ Zeige Token (wenn SHOW_RESET_TOKEN_INLINE)
```

### 4. Datenbank-Zugriff

```
Streamlit App
    │
    ├─ auth.py              → get_user(), check_user_exists()
    ├─ pages/*.py           → get_favorites(), get_todos()
    └─ 0_Admin.py           → list_all_users(), set_admin()
                  │
                  ▼
              db.py Funktionen
                  │
        ┌─────────┼─────────┐
        │         │         │
    Users     Favorites   Todos
   (auth)    (Favoriten) (Aufgaben)
        │         │         │
        └─────────┼─────────┘
                  │
                  ▼
        .streamlit/users.db
           (SQLite 3)
```

---

## 🔐 Sicherheits-Architektur

### Passwort-Hashing

```
Eingabe: "mein_passwort"
  │
  ▼
hash_password()
  │
  ├─ bcrypt.gensalt(12)  # Cost factor
  └─ bcrypt.hashpw()
  │
  ▼
Gespeichert in DB:
"$2b$12$abcdefgh..."  (60 Zeichen)
```

### Token-basierte Authentifizierung

```
Session State (in Streamlit):
┌─────────────────────────────┐
│ st.session_state:           │
│  - auth_user: "username"    │
│  - lang: "de"               │
│  - session_data: {}         │
└─────────────────────────────┘
     │ (Persistiert während Session)
     │ (Wird zurückgesetzt bei Reload)
     ▼
Login-Gate-Check (app.py):
if not st.session_state.get("auth_user"):
    → Zeige Login-Seite
    → st.stop()
```

### Reset-Token

```
Gültigkeitsdauer: 30 Minuten
Format: secrets.token_urlsafe(32)
Beispiel: "Drmhze6EPcv0fN_81Bj-nA"

Stored in DB:
┌──────────────────────┐
│ reset_tokens Table   │
├──────────────────────┤
│ id                   │
│ username             │
│ token (UNIQUE)       │
│ expires_at           │
└──────────────────────┘
```

### Rate Limiting (Brute-Force-Schutz)

```
Pro Benutzer + Endpoint:
- 5 Versuche
- 15 Minuten Window
- Auto-Reset nach Ablauf

Implementierung:
check_rate_limit("username", "login", max_attempts=5, window_minutes=15)
```

---

## 🌍 Mehrsprachigkeits-System

### Sprachen-Architektur

```
i18n.py (Zentrale Verwaltung)
  │
  ├─ TRANSLATIONS Dict
  │  ├─ "de" → 200+ Keys
  │  ├─ "en" → 200+ Keys
  │  └─ "ar" → 200+ Keys
  │
  └─ Funktionen:
     ├─ t(key) → get_translation()
     ├─ language_selector() → UI-Dropdown
     └─ apply_rtl_if_needed() → Arabisch-Support
```

### Session Language

```
Priorität (Reihenfolge):
1. Query Parameter: ?lang=de
2. st.session_state["lang"]
3. Standard: "de"

Speicherung:
st.session_state["lang"] = "en"
```

### Arabisch (RTL) Support

```
CSS-Klasse für RTL:
direction: rtl;

Number-Eingaben:
direction: ltr;  (Zahlen bleiben LTR)
text-align: right;

Implementierung:
apply_rtl_if_needed() → st.markdown(CSS)
```

---

## 📊 Datenbank-Schema

### users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,           -- bcrypt hash
    email TEXT,                             -- Optional für Password-Reset
    totp_secret TEXT,                       -- TOTP 2FA Secret
    is_admin INTEGER DEFAULT 0,             -- 0=User, 1=Admin
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### reset_tokens Table

```sql
CREATE TABLE reset_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,             -- 43 Zeichen urlsafe
    expires_at TEXT NOT NULL,               -- ISO format
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

### favorites Table

```sql
CREATE TABLE favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    title TEXT,                             -- Objekt-Name
    price REAL,                             -- Kaufpreis
    location TEXT,                          -- Stadt/Ort
    sqm REAL,                               -- Wohnfläche
    energy_class TEXT,                      -- A+, A, B, ...
    condition TEXT,                         -- Zustand
    notes TEXT,                             -- Benutzernotizen
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

### todos Table

```sql
CREATE TABLE todos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    category TEXT,                          -- "renovation", "move"
    text TEXT,                              -- To-Do Text
    done INTEGER DEFAULT 0,                 -- 0=Offen, 1=Erledigt
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(username) REFERENCES users(username)
);
```

---

## 🔄 Session State Management

```python
st.session_state:
{
    "auth_user": "username" or None,
    "lang": "de" | "en" | "ar",
    
    # Favoriten (in-memory, nicht persistent)
    "favoriten": [ ... ],
    
    # Renovierungs-To-Dos
    "renovierung_todos": [ ... ],
    
    # Umzugs-To-Dos
    "umzug_todos": [ ... ],
    
    # Form-State (automatisch von Streamlit)
    "form_input_*": ...
}
```

**Wichtig**: Session State wird bei Seitenneuladen zurückgesetzt.  
Für Persistierung: `db.py` Favoriten/Todos-Funktionen nutzen.

---

## 📱 Multi-Device-Unterstützung

### Responsive Breakpoints

```css
Mobile (< 480px):
- Single Column Layout
- Angepasste Font-Größen
- Touch-friendly Buttons (40px Höhe)

Tablet (480px - 768px):
- 2-Column Layout
- Normale Font-Größen

Desktop (> 768px):
- 3-Column Layout
- Optimierte Spacing
```

### Navigation

```
Desktop/Tablet:
┌─────────────────┐
│   Hamburger     │
│  (Popover)      │
└─────────────────┘

Mobile:
┌─────────────────┐
│   Hamburger     │
│  (Expander)     │
└─────────────────┘
```

---

## 🚀 Performance-Optimierungen

### Caching

```python
@st.cache_data
def get_translations():
    return TRANSLATIONS

@st.cache_resource
def get_db_connection():
    return sqlite3.connect(DB_PATH)
```

### Lazy Loading

- Seiten werden nur beim Zugriff geladen
- Session State wird bei Bedarf initialisiert

### Optimierte DB-Queries

```python
# Gut: Nur benötigte Spalten laden
SELECT id, title, price FROM favorites

# Vermeiden: Alle Spalten ohne Limit
SELECT * FROM todos
```

---

## 🐛 Fehlerbehandlung

### Try-Except Pattern

```python
try:
    user = get_user(username)
    if user:
        # Logik
except Exception as e:
    st.error(f"Fehler: {str(e)}")
    logger.exception("Detaillierte Exception")
```

### Validierungen

```python
# Form-Validierung
if not username or not password:
    st.error(t("auth_fill_all"))
    return False

# Geschäftslogik-Validierung
if not verify_password(password, user["password_hash"]):
    st.error(t("auth_login_failed"))
    return False
```

---

## 📈 Skalierungsmöglichkeiten

### Phase 1 (Aktuell): SQLite lokal
- Benutzer: 1-100
- Speicherung: .streamlit/users.db
- Rücksicherung: Manuell

### Phase 2: PostgreSQL auf VM
- Benutzer: 100-10,000
- Speicherung: Remote PostgreSQL
- Rücksicherung: Automatisch

### Phase 3: Kubernetes + Cloud
- Benutzer: 10,000+
- Speicherung: Cloud-DB (AWS RDS, etc.)
- Rücksicherung: Automated Snapshots

---

## 📖 Entwickler-Guide

### Code-Konvention

- Funktionsnamen: `snake_case`
- Klassennamen: `CamelCase`
- Konstanten: `UPPER_CASE`
- Docstrings auf Deutsch

### Testing

```bash
# Lokale Tests ausführen
pytest tests/

# Code-Style überprüfen
flake8 *.py
black *.py
```

### Debug-Modus

```bash
streamlit run app.py --logger.level=debug --client.showErrorDetails=true
```

---

**Letzte Aktualisierung**: November 2025
