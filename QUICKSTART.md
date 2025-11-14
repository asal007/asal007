# 🏠 MeinImmoKauf – Schnellstart-Anleitung

## 5 Minuten bis zur laufenden App

### Schritt 1: Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### Schritt 2: Admin-Benutzer erstellen

```bash
python scripts/init_admin.py
```

Folgen Sie den Anweisungen:
- **Benutzername**: `admin`
- **Passwort**: `admin1234`

### Schritt 3: App starten

```bash
streamlit run app.py
```

### Schritt 4: Anmelden

Öffnen Sie http://localhost:8501 und melden Sie sich an:
- **Benutzer**: `admin`
- **Passwort**: `admin1234`

---

## 🎯 Was ist wo?

| Sektion | Ort | Beschreibung |
|---------|-----|-------------|
| **Startseite** | Home | Willkommen & Überblick |
| **Phase 1** | "Vor dem Kauf" | Budgetrechner, Finanzierung, Dokumente |
| **Phase 2** | "Während des Kaufs" | Favoritenliste, Besichtigung, Verträge |
| **Phase 3** | "Nach dem Kauf" | Behördliches, Umzug, To-Dos |
| **Admin-Panel** | "Admin" (nur für Admins) | Benutzerverwaltung, Statistiken |

---

## 👤 Benutzer-Management

### Neuen Benutzer erstellen

1. Gehen Sie zur Startseite
2. Klicken Sie auf "Registrieren"
3. Geben Sie Benutzername und Passwort ein

### Benutzer zu Admin befördern

1. Öffnen Sie das Admin-Panel
2. Suchen Sie den Benutzer
3. Klicken Sie "Admin-Status" 

### Benutzer löschen

1. Öffnen Sie das Admin-Panel
2. Klicken Sie auf "Löschen"

---

## 🔐 Sicherheit

### Passwort zurücksetzen

1. Klicken Sie auf "Passwort vergessen?"
2. Geben Sie Ihren Benutzernamen ein
3. Geben Sie einen Token ein oder warten Sie auf E-Mail

**Hinweis**: E-Mail-Versand erfordert SMTP-Konfiguration in `.streamlit/secrets.toml`

### Zwei-Faktor-Authentifizierung

1. Gehen Sie zu "Profil-Einstellungen"
2. Klicken Sie "2FA aktivieren"
3. Scannen Sie den QR-Code mit Ihrer Authenticator-App (Google Authenticator, Microsoft Authenticator, etc.)

---

## 📊 Features erkunden

### 💰 Budgetrechner

Berechnen Sie Ihren maximalen Kaufpreis basierend auf:
- Monatliches Einkommen
- Monatliche Ausgaben
- Eigenkapital
- Zinssätze

### 📋 Favoritenliste

Speichern Sie Ihre Lieblingsobjekte mit:
- Preis
- Lage
- Größe (m²)
- Energieeffizienzklasse
- Fotos

### ✅ Checklisten

Verfolgen Sie Ihre Fortschritte durch alle 3 Phasen mit vordefinierten Aufgaben.

### 📝 To-Do-Listen

Erstellen Sie Listen für:
- Renovierungsplanung
- Umzugsplanung

---

## 🌍 Sprache wechseln

Klicken Sie auf "Sprache / Language / اللغة" oben in der Navigation:
- 🇩🇪 Deutsch (Standard)
- 🇬🇧 English
- 🇸🇦 العربية (Arabisch, RTL-optimiert)

---

## 🐛 Häufige Probleme

### "Authentifizierung fehlgeschlagen"
- Überprüfen Sie Benutzernamen und Passwort
- Stellen Sie sicher, dass der Benutzer existiert

### "E-Mail konnte nicht versendet werden"
- Überprüfen Sie `.streamlit/secrets.toml` auf SMTP-Konfiguration
- Aktivieren Sie `SHOW_RESET_TOKEN_INLINE=true` zum Debuggen

### "Admin-Panel nicht sichtbar"
- Sie müssen mit einem Admin-Benutzer angemeldet sein
- Überprüfen Sie Ihren Benutzerstatus im Admin-Panel

---

## 📚 Mehr erfahren

- **Setup-Anleitung**: Siehe `docs/setup.md`
- **Deployment**: Siehe `docs/deployment.md`
- **Architektur**: Siehe `docs/architecture.md`
- **Änderungshistorie**: Siehe `CHANGES.md`

---

## 🚀 Nächste Schritte

1. ✅ App installieren und starten
2. ✅ Erste Benutzer erstellen
3. ✅ Alle 3 Phasen durchgehen
4. ✅ Features erkunden
5. → Für Produktion: Siehe `docs/deployment.md`

---

**Viel Spaß mit MeinImmoKauf! 🏠**
