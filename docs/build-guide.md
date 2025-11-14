# Build-Anleitung für Google Play Store

## Voraussetzungen

- **Node.js** (v16+) und npm
- **Java JDK** (v11+)
- **Android SDK** (min. API 26 für Android 8.0)
- **Android Studio** (empfohlen)
- **Keystore** für Release-Signing (oder unten erstellen)

---

## 1️⃣ Umgebung vorbereiten

### 1.1 Node.js & Dependencies installieren
```bash
cd mobile
npm install
```

### 1.2 Capacitor CLI installieren
```bash
npm install -g @capacitor/cli
```

### 1.3 Android-Plattform hinzufügen
```bash
npx cap add android
npx cap sync android
```

Ergebnis: `mobile/android/` Ordner wird erstellt

---

## 2️⃣ Konfiguration

### 2.1 Produktions-URL setzen

Öffne `mobile/capacitor.config.ts`:

```typescript
server: {
  url: 'https://deine-produktions-domain.com',  // ← HIER ÄNDERN
  cleartext: false,
},
```

**⚠️ WICHTIG:** Muss HTTPS sein, nicht HTTP!

### 2.2 App-Informationen
Öffne `mobile/android/app/build.gradle`:

```gradle
android {
    compileSdkVersion 33
    ...
    defaultConfig {
        applicationId "de.meinimmokauf.app"
        minSdkVersion 26              // Android 8.0
        targetSdkVersion 33           // Android 13
        versionCode 1                 // Inkrementell pro Build
        versionName "1.0.0"           // Für Play Store
    }
}
```

---

## 3️⃣ Keystore erstellen (einmalig)

Ein Keystore ist nötig zum Signieren des Release-APK/AAB.

### 3.1 Keystore generieren
```bash
cd mobile/android

keytool -genkey -v -keystore meinimmokauf-release.keystore \
  -keyalg RSA -keysize 2048 -validity 9125 \
  -alias meinimmokauf-key
```

Du wirst gefragt nach:
```
Keystore-Passwort: [SICHERES PASSWORT NOTIEREN]
Alias-Passwort: [KANN GLEICH SEIN]
First and last name: [Dein Name oder Unternehmen]
Organizational Unit: [z.B. "Development"]
Organization: [z.B. "MeinImmoKauf GmbH"]
City: [z.B. "Berlin"]
State: [z.B. "BE"]
Country Code: [z.B. "DE"]
```

**Ergebnis:** `meinimmokauf-release.keystore` (NIEMALS in Git committen!)

### 3.2 .gitignore aktualisieren
```bash
echo "*.keystore" >> .gitignore
echo "*.jks" >> .gitignore
```

---

## 4️⃣ Android App Bundle (AAB) bauen

### 4.1 Capacitor synchronisieren
```bash
cd mobile
npx cap sync android
```

### 4.2 Keystore in build.gradle hinterlegen
Öffne `mobile/android/app/build.gradle` und füge am Ende hinzu:

```gradle
android {
    ...
    signingConfigs {
        release {
            storeFile file('meinimmokauf-release.keystore')
            storePassword 'DEIN-KEYSTORE-PASSWORT'
            keyAlias 'meinimmokauf-key'
            keyPassword 'DEIN-KEY-PASSWORT'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 4.3 Release-Build erstellen
```bash
cd mobile/android

# Option 1: Via Gradle (Terminal)
./gradlew bundleRelease

# Option 2: Via Android Studio
# → Build → Generate Signed Bundle/APK → Android App Bundle
```

**Output:** `mobile/android/app/build/outputs/bundle/release/app-release.aab`

---

## 5️⃣ APK erzeugen (für Testing lokal)

Falls du das AAB zuerst testen möchtest:

```bash
cd mobile/android
./gradlew assembleRelease
```

**Output:** `mobile/android/app/build/outputs/apk/release/app-release.apk`

Installation auf Test-Gerät:
```bash
adb install mobile/android/app/build/outputs/apk/release/app-release.apk
```

---

## 6️⃣ Play Console Upload

### 6.1 Google Play Console öffnen
1. Gehe zu https://play.google.com/console
2. Melde dich an (Google-Account erforderlich)

### 6.2 App erstellen
1. Klick auf "Alle Apps" → "+ App erstellen"
2. **App-Name:** "MeinImmoKauf"
3. **Standardsprache:** Deutsch
4. **App- oder Spiel-Kategorie:** "Produktivität"
5. **Inhaltstyp:** App
6. Erkläre, warum die App keine offizielle App vom Herausgeber ist (falls relevant)

### 6.3 AAB hochladen
1. Gehe zu **"Version" → "Produktion"** (oder zuerst Internal Testing)
2. Klick auf **"Create new release"**
3. Hochladen: `app-release.aab`
4. Speichern

### 6.4 Store-Listing ausfüllen

#### a) Basis-Informationen
- **App-Name:** MeinImmoKauf
- **Kurzbeschreibung:** Ratgeber für Immobilienkauf in Deutschland
- **Vollständige Beschreibung:** [Siehe `docs/play-store-metadaten.md`]

#### b) Grafiken & Media
- **App-Icon:** 512x512 PNG (hier: `icon.png`)
- **Feature-Graphic:** 1024x500 PNG
- **Screenshots:** Mindestens 2-3 (1080x1920)
- **Vorschau-Video:** Optional

#### c) Kategorisierung
- **Kategorie:** Produktivität
- **Inhaltsbewertung:** Fragebogen ausfüllen
  - Altersfreigabe: 13+
  - Keine Gewalt, sexuelle Inhalte, etc.

#### d) Datenschutz & Sicherheit
- **Datenschutzrichtlinie-URL:** https://deine-domain.de/datenschutz (MUSS existieren!)
- **Data Safety Form:** Alle Fragen beantworten
  - Welche Daten werden verarbeitet?
  - Werden Daten weitergegeben?
  - Ist HTTPS aktiviert? ✅ Ja

#### e) Support & Kontakt
- **Support-E-Mail:** support@meinimmokauf.de
- **Website:** https://deine-domain.de
- **Impressum/Kontakt:** https://deine-domain.de/kontakt

### 6.5 Review starten
1. Alle Felder ausfüllen ✅
2. Klick auf **"Submit for review"**
3. **Warten:** 1-7 Tage (meist 2-3 Tage)

---

## 7️⃣ Internal Testing (optional aber empfohlen)

### 7.1 Test-Track erstellen
1. Play Console → **"Testversionen"** → **"Internal testing"**
2. AAB hochladen
3. Test-Link generieren
4. Mit Google-Testern teilen (E-Mail-Liste)

### 7.2 Testing durchführen
- Installieren auf min. 2-3 verschiedenen Geräten
- Testen:
  - Login funktioniert?
  - Favoriten speichern/laden?
  - 2FA funktioniert?
  - Admin-Panel lädt?
  - Keine Crashes?
  - Offlineverhalten?

### 7.3 Bugs beheben
Falls Probleme gefunden:
1. Fix in der Streamlit-App durchführen
2. App neu deployen
3. Neue APK/AAB generieren (versionCode erhöhen!)
4. Erneut testen

---

## 8️⃣ Häufige Build-Fehler

### Fehler: "Unsigned App"
**Ursache:** Keystore nicht richtig konfiguriert
**Lösung:** 
```bash
./gradlew bundleRelease --stacktrace
```

### Fehler: "API Level zu alt"
**Ursache:** targetSdkVersion < 31
**Lösung:** In `build.gradle` erhöhen:
```gradle
targetSdkVersion 33
```

### Fehler: "INTERNET permission missing"
**Ursache:** AndroidManifest.xml unvollständig
**Lösung:** Prüfe, dass vorhanden:
```xml
<uses-permission android:name="android.permission.INTERNET" />
```

### Fehler: "App kann sich nicht mit Server verbinden"
**Ursache:** URL falsch oder nicht HTTPS
**Lösung:**
```bash
# In capacitor.config.ts prüfen:
url: 'https://YOUR-DOMAIN',  # Muss HTTPS sein!
```

---

## 9️⃣ Versionierung

Für zukünftige Updates:

```gradle
versionCode 2          // Muss höher sein als vorher (2, 3, 4, ...)
versionName "1.0.1"    // Sichtbare Version (1.0.1, 1.1.0, 2.0.0, ...)
```

Dann wieder:
```bash
cd mobile/android
./gradlew bundleRelease
```

---

## 🔟 Checkliste vor Submit

- [ ] Produktions-URL in `capacitor.config.ts` gesetzt
- [ ] App-Icons vorhanden (512x512)
- [ ] Screenshots 5+ (1080x1920)
- [ ] Feature-Graphic (1024x500)
- [ ] Datenschutzrichtlinie-URL funktioniert
- [ ] Support-E-Mail erreichbar
- [ ] AAB erfolgreich gebaut
- [ ] Internal Testing bestanden
- [ ] Alle Store-Listing Felder ausgefüllt
- [ ] Data Safety Form komplett
- [ ] Ready für Submission!

---

## 📚 Weitere Ressourcen

- [Google Play Console](https://play.google.com/console)
- [Android Build Documentation](https://developer.android.com/build)
- [Capacitor Android Guide](https://capacitorjs.com/docs/android)
- [App Bundle Publishing Guide](https://developer.android.com/guide/app-bundle)

---

**Gutes Gelingen! 🚀**
