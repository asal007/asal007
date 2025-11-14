#!/usr/bin/env python3
"""
Passwort-Änderungs-Skript für MeinImmoKauf.
Ermöglicht das Ändern des Passworts für einen Benutzer.
"""

import sys
import os
from pathlib import Path

# Füge das Projekt-Verzeichnis zum Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from db import init_db, get_user, update_user_password
from auth import hash_password


def main():
    print("🔐 MeinImmoKauf - Passwort ändern")
    print("-" * 50)
    
    # Initialisiere DB
    init_db()
    
    username = input("Benutzername: ").strip()
    if not username:
        print("❌ Benutzername ist erforderlich")
        return
    
    user = get_user(username)
    if not user:
        print(f"❌ Benutzer '{username}' existiert nicht")
        return
    
    print(f"✓ Benutzer '{username}' gefunden")
    
    while True:
        new_password = input("Neues Passwort: ").strip()
        if not new_password or len(new_password) < 6:
            print("❌ Passwort muss mindestens 6 Zeichen lang sein")
            continue
        
        new_password2 = input("Passwort wiederholen: ").strip()
        if new_password != new_password2:
            print("❌ Passwörter stimmen nicht überein")
            continue
        
        # Update password
        hashed = hash_password(new_password)
        update_user_password(username, hashed)
        
        print(f"\n✓ Passwort für '{username}' erfolgreich geändert!")
        break


if __name__ == "__main__":
    main()
