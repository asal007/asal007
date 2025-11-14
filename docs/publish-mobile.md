# Veröffentlichung in Google Play & Apple App Store

Dieser Leitfaden zeigt, wie du deine bestehende Streamlit‑Web‑App als mobile App in beiden Stores veröffentlichst. Wir verwenden einen schlanken nativen Wrapper (Capacitor), der deine App über eine HTTPS‑URL lädt.

## Voraussetzungen
- Öffentliche HTTPS‑URL deiner Streamlit‑App (z. B. `https://meinimmokauf.de`)
- Google Play Console (Einmalgebühr ca. 25 USD)
- Apple Developer Program (jährlich ca. 99 USD)
- App‑Name, Kurzbeschreibung, Screenshots, App‑Icons (1024×1024), Datenschutzrichtlinie‑URL
- Eindeutige Bundle‑IDs: Android `de.meinimmokauf.app`, iOS `de.meinimmokauf.app`

## Schritt 1: App hosten
- Option schnell: Render, Railway, Fly.io oder Cloud Run. Stelle sicher, dass die URL per HTTPS erreichbar ist.
- Beispiel Render: „Web Service“ mit `streamlit run app.py`, Auto‑Deploy, Domain verbinden.

## Schritt 2: Mobiler Wrapper (Capacitor)
Wir legen ein kleines Projekt an, das nur deine HTTPS‑URL lädt. Der Code liegt im Ordner `mobile/`.

### Setup (lokal ausführen)
```
# Im Ordner mobile/
npm install
# Plattformen hinzufügen
npx cap add android
npx cap add ios
```

Öffne die Projekte:
```
npx cap open android   # Android Studio
npx cap open ios       # Xcode
```

Konfiguration: Trage deine Produktions‑URL in `mobile/capacitor.config.ts` ein:
```
server: {
  url: 'https://DEINE-DOMAIN',
  cleartext: false
}
```

### Android Build (AAB)
- In Android Studio: „Build > Generate Signed Bundle/APK > Android App Bundle“.
- Erstelle einen Keystore (sicher aufbewahren), wähle Release‑Build.
- Prüfe `android/app/src/main/AndroidManifest.xml`: Internet‑Permission vorhanden.
- Lade das AAB in der Google Play Console hoch, fülle „Data safety“, Inhalteinstufung, Screenshots, Beschreibung.

### iOS Build (IPA)
- In Xcode: Team wählen, Bundle Identifier setzen (`de.meinimmokauf.app`).
- „Signing & Capabilities“: automatisches Signieren aktivieren.
- Stelle sicher, dass die aufgerufene Domain HTTPS verwendet (ATS). Falls nötig: gezielte Ausnahme unter `Info.plist` > `NSAppTransportSecurity` > `NSExceptionDomains`.
- „Product > Archive“ und anschließend „Distribute App“ über den Organizer.

## Store‑Richtlinien & Hinweise
- Apple Richtlinie 4.2 (Minimum Functionality): Ein reiner Webseiten‑Wrapper kann abgelehnt werden. Empfohlen:
  - Native Extras: z. B. Teilen‑Sheet, Deep‑Links, Push‑Benachrichtigungen (über Capacitor Plugins), App‑Icon/Splash nativ.
  - Saubere Mobiloptimierung, schnelle Ladezeiten, klare Navigation.
- Datenschutz: Erkläre klar, welche Daten verarbeitet werden (Sessions, keine Tracker außer technisch notwendig). Verlinke die Richtlinie.
- Support: Gib eine Support‑E‑Mail/Website an.

## Häufige Stolpersteine
- Keine HTTPS‑URL: iOS blockiert unsichere Verbindungen standardmäßig.
- Fehlende Icons/Screenshots: Stores verlangen spezifische Größen.
- Nur Webview ohne Mehrwert: Apple lehnt u. U. ab. Füge kleine native Funktionen hinzu.

## Nächste Schritte
1) URL final wählen und in `mobile/capacitor.config.ts` setzen.
2) Icons/Splash in `mobile/` ergänzen.
3) Android/iOS Projekte erzeugen und Release‑Builds erstellen.
4) Play Console / App Store Connect Einträge ausfüllen und zur Prüfung einreichen.

Bei Bedarf kann ich dir die native Extras (Teilen‑Sheet, Deep‑Links, Push) direkt integrieren.