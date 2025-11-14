# MeinImmoKauf - Keystore Generator
# Generiert einen Release-Keystore für Google Play Store

$KeystorePath = "mobile\android\meinimmokauf-release.keystore"
$Alias = "meinimmokauf-key"
$Validity = 9125  # 25 Jahre

Write-Host "🔐 MeinImmoKauf - Keystore Generator" -ForegroundColor Green
Write-Host "---------------------------------------" -ForegroundColor Green
Write-Host ""

# Überprüfe ob Keystore bereits existiert
if (Test-Path $KeystorePath) {
    Write-Host "⚠️  Keystore existiert bereits: $KeystorePath" -ForegroundColor Yellow
    $response = Read-Host "Möchtest du ihn überschreiben? (y/n)"
    if ($response -ne "y") {
        Write-Host "Abgebrochen." -ForegroundColor Red
        exit
    }
}

# Passwörter eingeben
Write-Host "Bitte folgende Informationen eingeben:" -ForegroundColor Cyan
Write-Host ""

# Keystore-Passwort (doppelt eingeben zur Bestätigung)
$storePass = Read-Host "Keystore-Passwort (min. 6 Zeichen)" -AsSecureString
$storePassConfirm = Read-Host "Passwort wiederholen" -AsSecureString

$storePlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($storePass))
$confirmPlain = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($storePassConfirm))

if ($storePlain -ne $confirmPlain) {
    Write-Host "❌ Passwörter stimmen nicht überein!" -ForegroundColor Red
    exit
}

if ($storePlain.Length -lt 6) {
    Write-Host "❌ Passwort muss mindestens 6 Zeichen lang sein!" -ForegroundColor Red
    exit
}

# Alias-Passwort (muss gleich sein wie Keystore-Passwort bei keytool)
$keyPass = $storePlain

Write-Host ""
Write-Host "Persönliche Informationen (für Zertifikat):" -ForegroundColor Cyan

$firstName = Read-Host "Vorname"
$lastName = Read-Host "Nachname"
$org = Read-Host "Organisation (z.B. dein Name oder Firma)"
$city = Read-Host "Stadt"
$state = Read-Host "Bundesland"
$country = Read-Host "Land (2-Buchstaben Code, z.B. DE)"

$CN = "$firstName $lastName"
$OU = $org
$O = $org
$L = $city
$S = $state
$C = $country

Write-Host ""
Write-Host "Generiere Keystore..." -ForegroundColor Yellow

# Keystore mit keytool generieren
$dname = "CN=$CN, OU=$OU, O=$O, L=$L, S=$S, C=$C"

& keytool -genkey -v `
  -keystore $KeystorePath `
  -keyalg RSA `
  -keysize 2048 `
  -validity $Validity `
  -alias $Alias `
  -storepass $storePlain `
  -keypass $keyPass `
  -dname $dname

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Keystore erfolgreich generiert!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Speichere diese Informationen sicher:" -ForegroundColor Cyan
    Write-Host "  Keystore-Datei: $KeystorePath" -ForegroundColor White
    Write-Host "  Keystore-Passwort: [gespeichert]" -ForegroundColor White
    Write-Host "  Alias: $Alias" -ForegroundColor White
    Write-Host "  Alias-Passwort: [gespeichert]" -ForegroundColor White
    Write-Host ""
    Write-Host "⚠️  WICHTIG:" -ForegroundColor Red
    Write-Host "  - Speichere das Keystore-Passwort sicher ab (erforderlich für zukünftige Updates)"
    Write-Host "  - Verliere die Keystore-Datei nicht"
    Write-Host "  - Sie ist BEREITS in .gitignore ausgeschlossen" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "❌ Keystore-Generierung fehlgeschlagen!" -ForegroundColor Red
    exit 1
}
