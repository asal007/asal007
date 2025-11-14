#!/usr/bin/env python3
"""
Quick test script für MeinImmoKauf
"""
import sys
sys.path.insert(0, '.')

from db import init_db, add_user, check_user_exists, list_all_users, set_admin
from auth import hash_password

# Initialisiere DB
init_db()
print("✓ Datenbank initialisiert")

# Erstelle Admin-Benutzer falls nicht vorhanden
if not check_user_exists("admin"):
    hashed = hash_password("admin1234")
    add_user("admin", hashed, email="admin@example.com", is_admin=True)
    set_admin("admin", True)
    print("✓ Admin-Benutzer 'admin' erstellt")
    print("  Passwort: admin1234")
else:
    print("✓ Admin-Benutzer existiert bereits")

# Zeige alle Benutzer
users = list_all_users()
print(f"\n📋 Alle Benutzer ({len(users)}):")
for u in users:
    admin_badge = " [ADMIN]" if u['is_admin'] else ""
    print(f"  - {u['username']}{admin_badge}")

print("\n✓ Test erfolgreich!")
print("\nSie können die App nun starten mit:")
print("  streamlit run app.py")
