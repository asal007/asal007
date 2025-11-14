#!/usr/bin/env python3
"""
Datenbank-Reset-Skript für MeinImmoKauf.
Löscht die alte Datenbank und erstellt eine neue mit Admin-Benutzer.
"""

import sys
import os
from pathlib import Path
import shutil

# Füge das Projekt-Verzeichnis zum Pfad hinzu
sys.path.insert(0, str(Path(__file__).parent.parent))

from db import init_db, add_user, set_admin, list_all_users
from auth import hash_password


def main():
    print("🔄 MeinImmoKauf - Datenbank Reset")
    print("-" * 50)
    
    db_dir = Path(".streamlit")
    db_path = db_dir / "users.db"
    
    # Backup erstellen
    if db_path.exists():
        backup_path = db_path.with_stem(f"{db_path.stem}_backup")
        shutil.copy(db_path, backup_path)
        print(f"✓ Backup erstellt: {backup_path}")
        
        # Alte DB löschen
        db_path.unlink()
        print(f"✓ Alte Datenbank gelöscht: {db_path}")
    
    # Neue DB initialisieren
    init_db()
    print("✓ Neue Datenbank erstellt")
    
    # Admin-Benutzer erstellen
    default_username = "admin"
    default_password = "admin1234"
    hashed = hash_password(default_password)
    add_user(default_username, hashed, is_admin=True)
    set_admin(default_username, True)
    print(f"✓ Admin-Benutzer '{default_username}' erstellt")
    
    # Verifizieren
    users = list_all_users()
    print(f"\n✓ Datenbank erfolgreich zurückgesetzt!")
    print(f"✓ Benutzer in DB: {len(users)}")
    
    for u in users:
        print(f"  - {u['username']} (Admin: {u['is_admin']})")
    
    print("\nSie können sich jetzt anmelden:")
    print(f"  Benutzername: {default_username}")
    print(f"  Passwort: {default_password}")


if __name__ == "__main__":
    main()
