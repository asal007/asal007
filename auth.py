import streamlit as st
import bcrypt
import pyotp
import os
import smtplib
import secrets
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from db import (
    get_user, add_user, update_user_password, check_user_exists,
    get_reset_token, set_reset_token, verify_reset_token, update_user_email
)
from i18n import t


def hash_password(password: str) -> str:
    """Hasht ein Passwort mit bcrypt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """Verifiziert ein Passwort gegen einen bcrypt-Hash."""
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except Exception:
        return False


def send_reset_email(username: str, email: str, reset_token: str) -> bool:
    """
    Sendet einen Passwort-Reset-Link per E-Mail.
    Liest SMTP-Konfiguration aus Streamlit Secrets.
    """
    try:
        smtp_config = st.secrets.get("smtp", {})
        if not smtp_config or not smtp_config.get("host"):
            return False
        
        host = smtp_config.get("host")
        port = smtp_config.get("port", 587)
        smtp_user = smtp_config.get("user")
        smtp_pass = smtp_config.get("password")
        from_addr = smtp_config.get("from", "noreply@example.com")
        use_tls = smtp_config.get("use_tls", True)
        
        msg = MIMEMultipart()
        msg["From"] = from_addr
        msg["To"] = email
        msg["Subject"] = "Passwort-Reset für MeinImmoKauf"
        
        body = f"""Hallo {username},

Sie haben einen Passwort-Reset angefordert.
Reset-Token: {reset_token}
Gültig für 30 Minuten.

Viele Grüße,
MeinImmoKauf Team"""
        
        msg.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(host, port) as server:
            if use_tls:
                server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"E-Mail-Versand fehlgeschlagen: {e}")
        return False


def login(username: str, password: str, totp_code: str = "") -> bool:
    """Versucht, einen Benutzer anzumelden."""
    if not username or not password:
        st.error(t("auth_fill_all"))
        return False
    
    user = get_user(username)
    if not user:
        st.error(t("auth_login_failed"))
        return False
    
    if not verify_password(password, user.get("password_hash", "")):
        st.error(t("auth_login_failed"))
        return False
    
    if user.get("totp_secret"):
        if not totp_code:
            st.error(t("auth_totp_required"))
            return False
        
        totp = pyotp.TOTP(user["totp_secret"])
        if not totp.verify(totp_code, valid_window=1):
            st.error(t("auth_totp_invalid"))
            return False
    
    st.session_state["auth_user"] = username
    st.success(t("auth_login_success"))
    return True


def register(username: str, password: str) -> bool:
    """Registriert einen neuen Benutzer."""
    disable_reg = os.getenv("DISABLE_REGISTRATION", "").lower() == "true"
    if disable_reg:
        st.error(t("auth_register_disabled"))
        return False
    
    if not username or not password:
        st.error(t("auth_fill_all"))
        return False
    
    if len(password) < 6:
        st.error(t("auth_pw_weak"))
        return False
    
    if check_user_exists(username):
        st.error(t("auth_user_exists"))
        return False
    
    hashed = hash_password(password)
    add_user(username, hashed)
    st.success(t("auth_register_success"))
    st.info(t("auth_now_login"))
    return True


def request_password_reset(username: str, email: str = "") -> bool:
    """Erzeugt einen Reset-Token."""
    user = get_user(username)
    if not user:
        st.error(t("auth_login_failed"))
        return False
    
    user_email = email or user.get("email", "")
    token = secrets.token_urlsafe(32)
    expires = datetime.now() + timedelta(minutes=30)
    
    set_reset_token(username, token, expires.isoformat())
    st.success(t("auth_reset_requested"))
    
    if user_email:
        email_sent = send_reset_email(username, user_email, token)
        if email_sent:
            st.info(f"Reset-Link wurde an {user_email} versendet.")
    
    if os.getenv("SHOW_RESET_TOKEN_INLINE", "").lower() == "true":
        st.code(token, language="text")
    
    return True


def reset_password(username: str, token: str, new_password: str) -> bool:
    """Setzt ein Passwort zurück mit Token-Verifizierung."""
    if not username or not token or not new_password:
        st.error(t("auth_fill_all"))
        return False
    
    if not verify_reset_token(username, token):
        st.error(t("auth_token_invalid"))
        return False
    
    if len(new_password) < 6:
        st.error(t("auth_pw_weak"))
        return False
    
    hashed = hash_password(new_password)
    update_user_password(username, hashed)
    set_reset_token(username, None, None)
    
    st.success(t("auth_reset_success"))
    return True


def logout_button():
    """Zeigt einen Logout-Button an."""
    if st.session_state.get("auth_user"):
        if st.button(t("auth_logout")):
            st.session_state.pop("auth_user", None)
            st.rerun()


def login_gate():
    """Auth-Gate: Wenn nicht angemeldet, zeige Login/Registrierung."""
    if st.session_state.get("auth_user"):
        return
    
    st.title(t("auth_title"))
    
    tab1, tab2, tab3 = st.tabs([
        t("auth_login_tab"),
        t("auth_register_tab"),
        t("auth_forgot_pw")
    ])
    
    with tab1:
        st.subheader(t("auth_login"))
        username = st.text_input(t("auth_username"), key="login_user")
        password = st.text_input(t("auth_password"), type="password", key="login_pass")
        totp_code = st.text_input(t("auth_totp_code"), key="login_totp", placeholder="(optional)")
        
        if st.button(t("auth_login")):
            if login(username, password, totp_code):
                st.rerun()
    
    with tab2:
        st.subheader(t("auth_register"))
        reg_user = st.text_input(t("auth_username"), key="reg_user")
        reg_pass = st.text_input(t("auth_password"), type="password", key="reg_pass")
        reg_pass2 = st.text_input(t("auth_password") + " (wiederholen)", type="password", key="reg_pass2")
        
        if st.button(t("auth_register")):
            if reg_pass != reg_pass2:
                st.error("Passwörter stimmen nicht überein.")
            elif register(reg_user, reg_pass):
                pass
    
    with tab3:
        st.write(t("auth_reset_help"))
        reset_user = st.text_input(t("auth_username"), key="reset_user")
        reset_email = st.text_input("E-Mail (optional)", key="reset_email")
        
        if st.button(t("auth_request_reset_btn")):
            if reset_user:
                request_password_reset(reset_user, reset_email)
        
        st.divider()
        st.write(t("auth_reset"))
        token_user = st.text_input(t("auth_username"), key="token_user")
        token = st.text_input(t("auth_reset_token"), key="token_input")
        new_pw = st.text_input(t("auth_new_password"), type="password", key="new_pw")
        
        if st.button(t("auth_reset_btn")):
            if reset_password(token_user, token, new_pw):
                st.rerun()
    
    st.stop()
