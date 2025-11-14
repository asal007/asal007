#!/usr/bin/env python3
"""
Initialisierungs-Skript für MeinImmoKauf.
Erstellt einen Admin-Benutzer, wenn die Datenbank noch leer ist.
"""

import sys
import os
from pathlib import Path

# Füge das Projekt-Verzeichnis zum Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent))

from db import init_db, add_user, list_all_users, set_admin
from auth import hash_password


def main():
    print("🏠 MeinImmoKauf - Initialisierung")
    print("-" * 50)
    
    # Initialisiere DB
    init_db()
    print("✓ Datenbank initialisiert")
    
    # Prüfe ob Benutzer existieren
    users = list_all_users()
    if users:
        print(f"✓ Datenbank enthält bereits {len(users)} Benutzer")
        return
    
    print("\nKeine Benutzer gefunden. Bitte erstellen Sie einen Admin-Benutzer.")
    print("-" * 50)
    
    while True:
        username = input("Benutzername: ").strip()
        if not username or len(username) < 3:
            print("❌ Benutzername muss mindestens 3 Zeichen lang sein")
            continue
        
        password = input("Passwort: ").strip()
        if not password or len(password) < 6:
            print("❌ Passwort muss mindestens 6 Zeichen lang sein")
            continue
        
        password2 = input("Passwort wiederholen: ").strip()
        if password != password2:
            print("❌ Passwörter stimmen nicht überein")
            continue
        
        # Erstelle Admin-Benutzer
        hashed = hash_password(password)
        add_user(username, hashed, is_admin=True)
        set_admin(username, True)
        
        print(f"\n✓ Admin-Benutzer '{username}' erfolgreich erstellt!")
        print("\nSie können sich jetzt anmelden:")
        print(f"  Benutzername: {username}")
        print("  Passwort: (das eingegebene Passwort)")
        break


if __name__ == "__main__":
    main()
