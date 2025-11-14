#!/usr/bin/env python3
"""Generiere Screenshot-Mockups für Play Store"""

from PIL import Image, ImageDraw
import os

os.makedirs('assets/screenshots', exist_ok=True)

def create_screenshot(filename, title, content_lines):
    """Erstelle einen 1080x1920 Screenshot-Mockup"""
    img = Image.new('RGB', (1080, 1920), (15, 23, 42))
    draw = ImageDraw.Draw(img)
    
    # Header-Bar
    draw.rectangle([(0, 0), (1080, 120)], fill=(0, 196, 154))
    draw.text((40, 35), title, fill='white')
    
    # Inhaltszeilen
    y = 180
    for line in content_lines:
        draw.text((60, y), line, fill=(229, 231, 235))
        y += 70
    
    # Footer-Bar
    draw.rectangle([(0, 1800), (1080, 1920)], fill=(31, 41, 55))
    draw.text((420, 1850), "MeinImmoKauf", fill=(0, 196, 154))
    
    img.save(f'assets/screenshots/{filename}')
    print(f'  ✓ {filename}')

print('Generiere Screenshots...')

# Screenshot 1: Login
create_screenshot('1-login.png', 'Anmeldung', [
    'Sichere Anmeldung',
    '',
    'Benutzername',
    '[Eingabefeld]',
    '',
    'Passwort',
    '[Eingabefeld]',
    'ANMELDEN'
])

# Screenshot 2: Startseite
create_screenshot('2-home.png', 'Startseite', [
    'MeinImmoKauf',
    'Ratgeber für Immobilienkauf',
    '',
    'PHASE 1: Vor dem Kauf',
    'PHASE 2: Während des Kaufs',
    'PHASE 3: Nach dem Kauf'
])

# Screenshot 3: Budget-Rechner
create_screenshot('3-budget.png', 'Budget-Kalkulation', [
    'Finanzierungsrechner',
    '',
    'Kaufpreis: 300.000 €',
    'Maklergebühr: 7.500 €',
    'Nebenkosten: ~40.000 €',
    'Gesamtbudget: ~347.500 €'
])

# Screenshot 4: Favoriten
create_screenshot('4-favorites.png', 'Favoriten', [
    'Meine gespeicherten Objekte',
    '',
    '🏠 Berlin-Mitte',
    '450.000 € | 2 Zimmer',
    '',
    '🏠 Charlottenburg',
    '1.200.000 € | Villa'
])

# Screenshot 5: To-Do-Listen
create_screenshot('5-todos.png', 'Renovierungs-Checkliste', [
    'Umzug & Renovierung',
    '',
    '[✓] Internet anmelden',
    '[✓] Makler beauftragen',
    '[ ] Besichtigungen planen',
    '[ ] Finanzierung klären'
])

# Screenshot 6: Admin-Panel
create_screenshot('6-admin.png', 'Admin-Panel', [
    'Benutzerverwaltung',
    '',
    '👤 admin [ADMIN]',
    '👤 john_doe',
    '👤 jane_smith',
    '',
    'Insgesamt: 3 Benutzer'
])

print('\n✅ 6 Screenshots erstellt in: assets/screenshots/')
