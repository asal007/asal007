import sys, os
# Ensure project root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from db import ensure_schema, migrate_from_json, get_user, set_admin


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/make_admin.py <username>")
        sys.exit(1)
    username = sys.argv[1].strip()
    ensure_schema()
    migrate_from_json()
    u = get_user(username)
    if not u:
        print(f"User '{username}' not found. Please create the user first.")
        sys.exit(2)
    set_admin(username, True)
    print(f"User '{username}' has been granted admin rights.")


if __name__ == "__main__":
    main()