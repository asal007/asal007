# MeinImmoKauf - Google Play Store Checkliste

## ✅ Vor dem Build

### App-Identität
- [x] App-Name: "MeinImmoKauf"
- [x] Package Name: "de.meinimmokauf.app"
- [x] Version: "1.0.0"
- [ ] Produktions-URL konfiguriert (in `capacitor.config.ts`)

### Icons & Grafiken (ERFORDERLICH)
Alle müssen im PNG-Format sein:

**Android Icons:**
- [ ] `android/app/src/main/res/mipmap-mdpi/ic_launcher.png` (48x48)
- [ ] `android/app/src/main/res/mipmap-hdpi/ic_launcher.png` (72x72)
- [ ] `android/app/src/main/res/mipmap-xhdpi/ic_launcher.png` (96x96)
- [ ] `android/app/src/main/res/mipmap-xxhdpi/ic_launcher.png` (144x144)
- [ ] `android/app/src/main/res/mipmap-xxxhdpi/ic_launcher.png` (192x192)

**Play Store Icons:**
- [ ] App Icon (512x512) - bereits vorhanden: `icon.png`
- [ ] Feature Graphic (1024x500)
- [ ] Screenshots (9 Stück, mindestens):
  - 3x Login/Register Screen (1080x1920)
  - 3x Haupt-Features (1080x1920)
  - 3x Admin/Profil (1080x1920)

### Texte & Beschreibungen
- [ ] App-Name: "MeinImmoKauf"
- [ ] Kurzbeschreibung (80 Zeichen): "Ratgeber für Immobilienkauf in Deutschland"
- [ ] Vollständige Beschreibung (4000 Zeichen)
- [ ] Änderungsnotizen für diese Version
- [ ] Support-E-Mail
- [ ] Datenschutzrichtlinie-URL (HTTPS)
- [ ] Website-URL

### Inhalt & Richtlinien
- [ ] Inhaltsbewertung ausgefüllt (ESRB)
- [ ] Zielgruppe: 13+ Jahre
- [ ] Datensicherheit erklärt
  - Welche Daten werden verarbeitet?
  - Werden Daten weitergegeben?
  - Verschlüsselung über HTTPS? ✓
- [ ] Richtlinien akzeptiert

### Technische Anforderungen
- [ ] Mindest Android-Version: 8.0 (API 26)
- [ ] Ziel Android-Version: 13+ (API 33)
- [ ] HTTPS erzwungen (nicht HTTP)
- [ ] Keystore mit Release-Key generiert
- [ ] AAB (Android App Bundle) signiert

---

## 🔑 Keystore generieren (einmalig)

```bash
cd mobile/android

# Keystore erstellen (2048-bit RSA, 25 Jahre gültig)
keytool -genkey -v -keystore meinimmokauf-release.keystore \
  -keyalg RSA -keysize 2048 -validity 9125 \
  -alias meinimmokauf-key

# Wird gefragt nach:
# - Keystore-Passwort (mindestens 6 Zeichen)
# - Alias-Passwort
# - Name, Stadt, Land, etc.
```

**⚠️ WICHTIG:** Keystore-Datei und Passwort sicher aufbewahren! (git ignore)

---

## 📦 Build-Prozess

### 1. Dependencies installieren
```bash
cd mobile
npm install
npx cap sync android
```

### 2. Android App Bundle erstellen
```bash
cd mobile/android
./gradlew bundleRelease
```

Ausgabe: `android/app/build/outputs/bundle/release/app-release.aab`

### 3. AAB in Play Console hochladen
1. Gehe zu Google Play Console
2. Wähle "MeinImmoKauf" oder erstelle neue App
3. Gehe zu "Version > Produktion" (oder "Testversionen > Internal testing")
4. Lade `app-release.aab` hoch
5. Alle erforderlichen Felder ausfüllen
6. Überprüfung starten

---

## 📋 Play Console Schritte

### Schritt 1: App erstellen
- Gehe zu https://play.google.com/console
- Klick "Alle Apps" > "+ App erstellen"
- Name: "MeinImmoKauf"
- Kategorie: "Produktivität"
- Inhaltstyp: "App"

### Schritt 2: Basis-Info
- App-Name: "MeinImmoKauf"
- Kurzbeschreibung
- Vollständige Beschreibung
- Website-URL
- Support-E-Mail

### Schritt 3: Grafiken & Media
- App Icon (512x512)
- Feature Graphic (1024x500)
- Screenshots (min. 2)
- Vorschau-Video (optional)

### Schritt 4: Inhaltsbewertung
- Fragebogen ausfüllen
- "Datenschutz und Sicherheit" → Alle Fragen beantworten
- Datenschutzrichtlinie-URL erforderlich

### Schritt 5: Zielgruppe & Inhalt
- Min. Altersfreigabe: 13+
- Lizenz-Vereinbarungen akzeptieren

### Schritt 6: AAB hochladen
- AAB in die Testversionsstrecke hochladen
- Test durchführen
- Zur Produktion hochladen

---

## 🧪 Testing vor Veröffentlichung

### Internal Testing
1. Play Console > "Testversionen" > "Internal testing"
2. AAB hochladen
3. Test-Link mit Google-Testern teilen
4. Min. 2-3 Tage Testing

### Fehler checken
```bash
# Build-Fehler überprüfen
cd mobile/android
./gradlew bundleRelease --stacktrace
```

---

## 🚨 Häufige Ablehnungsgründe

1. **Zu wenig Funktionalität** → Nur Webview?
   - Lösungen: Share-Sheet, Deep-Links hinzufügen, Native Features

2. **Sicherheit** → Nicht-HTTPS URL
   - Prüfe: `capacitor.config.ts` hat `cleartext: false`

3. **Datenschutz** → Keine Privacy Policy
   - Generiere: https://www.privacypolicygenerator.info/

4. **Screenshots** → Zu klein oder zu wenig
   - Muss: 1080x1920 sein (mindestens 2, besser 5)

5. **App-Icon** → Transparenz oder falsche Größe
   - Muss: 512x512, PNG, keine Transparenz

---

## 📝 Datenschutzerklärung (schnell erstellen)

```markdown
# Datenschutz

## Verarbeitete Daten
- Benutzername, E-Mail (lokale Authentifizierung)
- Passwort (mit bcrypt gehashed, nicht im Klartext)
- Favoriten & To-Do-Listen (lokal in Datenbank)

## Datenfreigabe
- Keine Weitergabe an Dritte
- Keine Tracking-Cookies
- Keine Werbenetze

## Speicherung
- Alle Daten lokal auf unserem Server
- HTTPS-verschlüsselt
- Löschbar über Profileinstellungen

## Kontakt
- E-Mail: support@meinimmokauf.de
- Oder: [Deine Website]
```

---

## ⏱️ Zeitrahmen

- **Build**: 30 min (erste Mal mit Android Studio Setup)
- **Play Console Setup**: 1-2 Stunden
- **Überprüfung**: 1-7 Tage (meist 2-3 Tage)

---

## 🎯 Nächste Schritte

1. [ ] Produktions-URL in `capacitor.config.ts` setzen
2. [ ] Icons generieren (oder mich fragen zum Batch-generieren)
3. [ ] Keystore erstellen
4. [ ] Privacy Policy schreiben
5. [ ] Play Console Account einrichten
6. [ ] AAB bauen und hochladen
7. [ ] Internal Testing durchführen
8. [ ] Zur Produktion freigeben
