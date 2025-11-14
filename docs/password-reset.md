# Passwort-Reset – Leitfaden

Dieser Leitfaden beschreibt den implementierten Passwort‑Reset‑Flow mit Einmal‑Token sowie relevante Konfigurationen.

## Überblick
- Reset‑Token werden pro Benutzer erzeugt und sind standardmäßig 30 Minuten gültig.
- Nach erfolgreichem Reset wird das Passwort mit `bcrypt` gespeichert.
- Alte SHA256‑Hashes werden beim nächsten erfolgreichen Login automatisch zu `bcrypt` migriert.

## Reset anfordern
1. In der App den Tab „Forgot password?“ öffnen.
2. Benutzername eingeben und auf „Token erstellen“ klicken.
3. Den generierten Token sicher an den Benutzer übermitteln (z. B. E‑Mail).

Hinweis: Für lokale Tests kann der Token optional direkt im UI angezeigt werden.

## Passwort zurücksetzen
1. Tab „Reset password“ öffnen.
2. Benutzername, Token und neues Passwort eingeben.
3. Mit „Passwort zurücksetzen“ bestätigen.

## Konfiguration
- Registrierung deaktivieren:
  - Environment: `REGISTER_ENABLED=false`
  - (Alternativ Secrets) `[auth] REGISTER_ENABLED = false`
- Token inline im UI anzeigen (nur Test/Entwicklung):
  - Environment: `SHOW_RESET_TOKEN_INLINE=true`
  - In Produktion sollte der Token nicht im UI angezeigt werden.

## Token‑Speicherung
- Tokens werden in `./.streamlit/users.json` unter dem jeweiligen Benutzer gespeichert, inkl. Ablaufzeit.
- Nach erfolgreichem Reset wird der Token entfernt.

## Sicherheitsempfehlungen
- In Produktion: Versand des Tokens per E‑Mail oder anderem sicheren Kanal.
- Nutzung einer Datenbank für Benutzerverwaltung statt der lokalen JSON‑Datei.
- Aktivieren Sie 2‑Faktor‑Authentifizierung, Rate‑Limiting und Monitoring, wo möglich.