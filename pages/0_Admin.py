import streamlit as st
from utils import inject_top_nav, hide_sidebar_completely, hide_header_actions_for_non_admin
from i18n import t, language_selector, apply_rtl_if_needed
from auth import login_gate
from db import list_all_users, set_admin, delete_user, get_user

st.set_page_config(page_title="Admin", page_icon="⚙️", layout="wide")

# Auth-Gate
login_gate()

# Prüfe Admin-Zugriff
username = st.session_state.get("auth_user")
user = get_user(username)
is_admin = bool(user and int(user.get("is_admin", 0)) == 1)

if not is_admin:
    st.error("Zugriff verweigert. Sie müssen ein Administrator sein.")
    st.stop()

language_selector()
apply_rtl_if_needed()
hide_sidebar_completely()
hide_header_actions_for_non_admin()

inject_top_nav()

st.title("⚙️ Admin Panel")
st.caption("Benutzerverwaltung und Systemeinstellungen")

st.divider()

st.header("👥 Benutzerverwaltung")

users = list_all_users()

if users:
    # Nutzer-Tabelle mit Aktionen
    for u in users:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.write(f"**{u['username']}**" + (" (Admin)" if u['is_admin'] else ""))
        with col2:
            st.caption(f"📧 {u['email'] or '(keine)'}")
        with col3:
            st.caption(f"Benutzerseit {u['created_at'][:10]}")
        with col4:
            # Optionen für Nutzer
            col_admin, col_delete = st.columns(2)
            with col_admin:
                # Toggle Admin
                if st.button(
                    "Admin-Status",
                    key=f"admin_toggle_{u['username']}",
                    use_container_width=True
                ):
                    new_status = not u['is_admin']
                    set_admin(u['username'], new_status)
                    st.success(f"Admin-Status aktualisiert: {new_status}")
                    st.rerun()
            
            with col_delete:
                # Lösch-Button
                if st.button(
                    "🗑️ Löschen",
                    key=f"delete_{u['username']}",
                    use_container_width=True
                ):
                    delete_user(u['username'])
                    st.success(f"Benutzer '{u['username']}' gelöscht")
                    st.rerun()
else:
    st.info("Noch keine Benutzer vorhanden.")

st.divider()

st.header("⚙️ Systemeinstellungen")

col_left, col_right = st.columns(2)
with col_left:
    st.subheader("Datenspeicher")
    st.info("Alle Benutzerdaten werden lokal in SQLite (.streamlit/users.db) gespeichert.")
    
with col_right:
    st.subheader("Sicherheit")
    st.info("Passwörter werden mit bcrypt gehashed. TOTP (2FA) ist pro Benutzer aktivierbar.")

st.divider()

st.header("📊 Statistiken")
col_stats1, col_stats2, col_stats3 = st.columns(3)
with col_stats1:
    st.metric("Gesamte Benutzer", len(users))
with col_stats2:
    admins = sum(1 for u in users if u['is_admin'])
    st.metric("Administratoren", admins)
with col_stats3:
    normal_users = len(users) - sum(1 for u in users if u['is_admin'])
    st.metric("Normale Benutzer", normal_users)

st.divider()

st.header("🔧 Debug-Informationen")
if st.checkbox("Debug-Informationen anzeigen"):
    st.code(f"Aktueller Benutzer: {username}")
    st.code(f"Admin-Status: {is_admin}")
    st.write("Alle Benutzer:")
    st.dataframe(
        [{"Username": u['username'], "Admin": u['is_admin'], "Email": u['email']} for u in users],
        use_container_width=True
    )
