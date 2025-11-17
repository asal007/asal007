# MeinImmoKauf - Keystore Generator (robuste Version)

$KeystorePath = 'mobile\android\meinimmokauf-release.keystore'
$Alias = 'meinimmokauf-key'
$Validity = 9125

Write-Host 'MeinImmoKauf - Keystore Generator'
Write-Host '---------------------------------'

if (Test-Path $KeystorePath) {
    Write-Host "Keystore existiert bereits: $KeystorePath"
    $response = Read-Host 'Moechtest du ihn ueberschreiben? (y/n)'
    if ($response -ne 'y') {
        Write-Host 'Abgebrochen.'
        exit
    }
}

Write-Host 'Bitte folgende Informationen eingeben:'

# Secure password input
$storePassSecure = Read-Host 'Keystore-Passwort (min. 6 Zeichen)' -AsSecureString
$storePassConfirmSecure = Read-Host 'Passwort wiederholen' -AsSecureString

function SecureToPlain($s) {
    return [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToCoTaskMemUnicode($s))
}

$storePass = SecureToPlain $storePassSecure
$storePassConfirm = SecureToPlain $storePassConfirmSecure

if ($storePass -ne $storePassConfirm) {
    Write-Host 'Passwoerter stimmen nicht ueberein!'
    exit 1
}

if ($storePass.Length -lt 6) {
    Write-Host 'Passwort zu kurz (mindestens 6 Zeichen)'
    exit 1
}

$keyPass = $storePass

Write-Host 'Persoenliche Informationen (fuer Zertifikat):'

$firstName = Read-Host 'Vorname'
$lastName = Read-Host 'Nachname'
$org = Read-Host 'Organisation (z.B. Name oder Firma)'
$city = Read-Host 'Stadt'
$state = Read-Host 'Bundesland'
$country = Read-Host 'Land (2-Buchstaben Code, z.B. DE)'

$CN = "${firstName} ${lastName}"
$dname = "CN=$CN, OU=$org, O=$org, L=$city, S=$state, C=$country"

Write-Host 'Generiere Keystore...'

# Prepare keytool arguments to avoid parsing issues
$args = @('-genkeypair', '-v', '-keystore', $KeystorePath, '-keyalg', 'RSA', '-keysize', '2048', '-validity', $Validity.ToString(), '-alias', $Alias, '-storepass', $storePass, '-keypass', $keyPass, '-dname', $dname)

try {
    & keytool @args
    $exit = $LASTEXITCODE
} catch {
    Write-Host 'Fehler beim Ausfuehren von keytool. Bitte stelle sicher, dass Java und keytool installiert sind.'
    exit 1
}

if ($exit -eq 0) {
    Write-Host ''
    Write-Host 'Keystore erfolgreich generiert!'
    Write-Host ''
    Write-Host 'Speichere diese Informationen sicher:'
    Write-Host "  Keystore-Datei: $KeystorePath"
    Write-Host "  Alias: $Alias"
    Write-Host ''
    Write-Host 'WICHTIG: Keystore und Passwort sicher aufbewahren.'
} else {
    Write-Host 'Keystore-Generierung fehlgeschlagen.'
    exit $exit
}
