def fmt_eur(value: float, decimals: int = 0) -> str:
    """
    Formatiert eine Zahl als Euro-Betrag mit deutscher Schreibweise:
    Tausenderpunkt und Dezimalkomma.
    Beispiel: 17500 -> "17.500 €", 1234.56 -> "1.234,56 €"
    """
    s = f"{value:,.{decimals}f}"
    # English format uses "," for thousands and "." for decimals.
    # Swap to German: "." thousands, "," decimals.
    s = s.replace(",", "__T__").replace(".", ",").replace("__T__", ".")
    return f"{s} €"

def inject_sidebar():
    """Fügt ein modernes Hamburger-Menü-Design in die Sidebar ein und setzt das Label mehrsprachig."""
    import streamlit as st
    try:
        from i18n import t
        nav_label = t("nav")
    except Exception:
        nav_label = "Navigation"

    # CSS separat als normaler String, damit keine f-String-Braces ausgewertet werden
    st.markdown(
        """
        <style>
        /* Sidebar Hintergrund und Rahmen */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
            border-right: 1px solid #1f2937;
            overflow: hidden; /* verhindert Buchstaben-Überlauf bei schmaler Breite */
        }
        /* Default Sidebar-Header (App-Name) ausblenden */
        [data-testid="stSidebar"] header { display: none; }

        /* Hamburger Header */
        .miq-hamburger { display:flex; align-items:center; gap:.75rem; padding:1rem 1.2rem; color:#e5e7eb; font-weight:600; }
        .miq-hamburger .icon { width:22px; height:16px; position:relative; }
        .miq-hamburger .icon span { position:absolute; left:0; right:0; height:2px; background:#00c49a; border-radius:2px; }
        .miq-hamburger .icon span:nth-child(1){ top:0; }
        .miq-hamburger .icon span:nth-child(2){ top:7px; }
        .miq-hamburger .icon span:nth-child(3){ bottom:0; }

        /* Standard-Streamlit-Seitenliste vollständig ausblenden (wir nutzen eigene Buttons) */
        [data-testid="stSidebarNav"] { display: none !important; }

        /* Navigation Items (custom) */
        .miq-nav { padding: .5rem 1rem; }
        .miq-nav a {
            display:block; padding:.6rem .8rem; border-radius:10px; color:#e5e7eb !important;
            text-decoration:none; transition: all .2s ease;
        }
        .miq-nav a:hover { background:#111827; color:#ffffff !important; box-shadow: inset 0 0 0 1px #00c49a33; }

        /* Mehr Abstand oben für Inhaltsbereich, damit Titel frei stehen */
        .block-container { padding-top: 2rem; }
        @media (max-width: 480px) {
            .block-container { padding-top: 2rem; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # HTML separat mit f-String für das mehrsprachige Label
    st.markdown(
        f"""
        <div class="miq-hamburger">
            <div class="icon"><span></span><span></span><span></span></div>
            <div id="miq-nav-label">{nav_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Custom translated navigation using buttons + switch_page to preserve session_state
    try:
        from i18n import t
        with st.sidebar:
            btn_home = st.button(t("home"), use_container_width=True)
            btn_before = st.button(t("phase_before"), use_container_width=True)
            btn_during = st.button(t("phase_during"), use_container_width=True)
            btn_after = st.button(t("phase_after"), use_container_width=True)
            # Admin-Link nur für eingeloggte Admins anzeigen
            uname = st.session_state.get("auth_user")
            is_admin = False
            if uname:
                try:
                    from db import get_user
                    u = get_user(uname)
                    is_admin = bool(u and int(u.get("is_admin", 0)) == 1)
                except Exception:
                    is_admin = False
            btn_admin = st.button(t("admin"), use_container_width=True) if is_admin else None
        # Perform navigation outside the sidebar context
        if btn_home:
            st.switch_page("app.py")
        elif btn_before:
            st.switch_page("pages/1_Vor_dem_Kauf.py")
        elif btn_during:
            st.switch_page("pages/2_Waehrend_des_Kaufs.py")
        elif btn_after:
            st.switch_page("pages/3_Nach_dem_Kauf.py")
        elif btn_admin:
            st.switch_page("pages/0_Admin.py")
    except Exception:
        with st.sidebar:
            btn_home = st.button(t("home"), use_container_width=True)
            btn_before = st.button(t("phase_before"), use_container_width=True)
            btn_during = st.button(t("phase_during"), use_container_width=True)
            btn_after = st.button(t("phase_after"), use_container_width=True)
            uname = st.session_state.get("auth_user")
            btn_admin = None
            if uname:
                try:
                    from db import get_user
                    u = get_user(uname)
                    if u and int(u.get("is_admin", 0)) == 1:
                        btn_admin = st.button("Admin", use_container_width=True)
                except Exception:
                    btn_admin = None
        if btn_home:
            st.switch_page("app.py")
        elif btn_before:
            st.switch_page("pages/1_Vor_dem_Kauf.py")
        elif btn_during:
            st.switch_page("pages/2_Waehrend_des_Kaufs.py")
        elif btn_after:
            st.switch_page("pages/3_Nach_dem_Kauf.py")
        elif btn_admin:
            st.switch_page("pages/0_Admin.py")


def hide_sidebar_if_not_logged_in():
    """Blendet die gesamte Sidebar aus, wenn kein Nutzer angemeldet ist.

    Die CSS-Regel wird nur gesetzt, wenn `st.session_state['auth_user']` nicht vorhanden ist.
    Nach erfolgreichem Login wird die Regel nicht mehr angewendet und die Sidebar erscheint wieder.
    """
    import streamlit as st
    if not st.session_state.get("auth_user"):
        st.markdown(
            """
            <style>
            /* ganze Sidebar ausblenden, inkl. Container */
            [data-testid="stSidebar"] { display: none !important; }
            /* optional: Platzreservierung minimieren */
            .stAppViewContainer { padding-left: 0 !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )


def hide_sidebar_completely():
    """Blendet die gesamte Sidebar inklusive Toggle dauerhaft aus."""
    import streamlit as st
    st.markdown(
        """
        <style>
        /* komplette Sidebar und der Toggle-Pfeil ausblenden */
        section[data-testid="stSidebar"][aria-expanded="true"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        [data-testid="stSidebar"] { display: none !important; }
        /* verschiedene mögliche Test-IDs für den Toggle verlässlich ausblenden */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid*="collapse"],
        /* Chevron auch im Header entfernen (neuere Streamlit-Versionen platzieren ihn dort) */
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        [data-testid="stHeader"] [data-testid*="Collapsed"],
        [data-testid="stHeader"] [data-testid*="collapse"],
        [data-testid="stHeader"] button[title*="Sidebar"],
        [data-testid="stHeader"] button[aria-label*="Sidebar"],
        [data-testid="stHeader"] button[aria-label*="Seitenleiste"],
        [data-testid="stHeader"] button[title*="Seitenleiste"]
        { display: none !important; }
        /* alte Hamburger-Überschrift der Sidebar (falls irgendwo gerendert) ausblenden */
        .miq-hamburger { display: none !important; }
        /* Platz links entfernen */
        .stAppViewContainer { padding-left: 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hide_header_actions_for_non_admin():
    """Verbirgt die Header-Aktionen (Deploy & Drei-Punkte-Menü) für Nicht‑Admins.

    Diese Funktion sollte früh im Seitenaufbau aufgerufen werden (vor dem Login‑Gate),
    damit Gäste und eingeloggte Nicht‑Admins die Header‑Aktionen nicht sehen. Für
    Admins wird keine CSS-Regel gesetzt, sodass die Aktionen sichtbar bleiben.
    """
    import streamlit as st
    # Prüfe Admin-Status
    uname = st.session_state.get("auth_user")
    is_admin = False
    if uname:
        try:
            from db import get_user
            u = get_user(uname)
            is_admin = bool(u and int(u.get("is_admin", 0)) == 1)
        except Exception:
            is_admin = False

    if is_admin:
        return

    # CSS zum Verbergen der Header-Buttons und -Menüs für Nicht-Admins
    st.markdown(
        """
        <style>
        /* Header-Aktionen (rechts oben) für Nicht-Admins verstecken */
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] a { display: none !important; }
        [data-testid="stHeader"] [data-testid*="Toolbar"],
        [data-testid="stHeader"] [class*="toolbar"],
        [data-testid="stHeader"] [class*="headerActions"] { display: none !important; }
        /* Header vorsichtig kollabieren, um Platz zu gewinnen */
        [data-testid="stHeader"] { height: 0 !important; min-height: 0 !important; background: transparent !important; }
        [data-testid="stHeader"] > div { display: none !important; }
        /* Inhalt ohne zusätzlichen Abstand direkt unter dem Header */
        .block-container { padding-top: 0 !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def inject_top_nav():
    """Zeigt eine horizontale Navigation oben anstelle der Sidebar an."""
    import streamlit as st
    try:
        from i18n import t
    except Exception:
        t = lambda k: k

    # Admin ermitteln
    uname = st.session_state.get("auth_user")
    is_admin = False
    if uname:
        try:
            from db import get_user
            u = get_user(uname)
            is_admin = bool(u and int(u.get("is_admin", 0)) == 1)
        except Exception:
            is_admin = False

    # Styling für Top-Bar
    st.markdown(
        """
        <style>
        /* Top-Bar: Höhe und Padding entfernen, keine zusätzliche Lücke oben */
        .miq-topnav { 
            background: linear-gradient(180deg, #0f172a 0%, #0b1220 100%);
            border-bottom: none;
            padding: 0;
            height: 0;
            min-height: 0;
        }
        /* Inhalt direkt unter dem Header beginnen lassen */
        .block-container { padding-top: 0 !important; }
        .miq-topnav .stButton>button { width: 100%; border-radius: 9999px; }
        /* Navigation-Trigger optisch links ausrichten */
        .miq-topnav .nav-trigger { font-weight: 600; color: #e5e7eb; }
        .miq-topnav .nav-trigger::before { content: "☰"; margin-right: .5rem; color: #00c49a; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Für Nicht-Admins: Header-Aktionen (Deploy & Drei-Punkte-Menü) ausblenden
    if not is_admin:
        st.markdown(
            """
            <style>
            /* Verstecke alle Buttons/Links im Header rechts für Nicht-Admins */
            [data-testid="stHeader"] button,
            [data-testid="stHeader"] a { display: none !important; }
            /* Verschiedene mögliche Toolbar-Container ebenfalls ausblenden */
            [data-testid="stHeader"] [data-testid*="Toolbar"],
            [data-testid="stHeader"] [class*="toolbar"],
            [data-testid="stHeader"] [class*="headerActions"] { display: none !important; }
            /* Header selbst kollabieren (Höhe entfernen) */
            [data-testid="stHeader"] { height: 0px !important; min-height: 0 !important; background: transparent !important; }
            [data-testid="stHeader"] > div { display: none !important; }
            /* Inhalt weiter nach oben rücken */
            .block-container { padding-top: 0.5rem !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

    with st.container():
        # Sprachwahl kompakt VOR der Navigation anzeigen
        langs = {"de": "Deutsch", "en": "English", "ar": "العربية"}
        current_lang = st.session_state.get("lang", "de")
        selected_lang = st.selectbox(
            "Sprache / Language / اللغة",
            list(langs.keys()),
            index=["de","en","ar"].index(current_lang),
            format_func=lambda k: langs[k],
            key="lang_selector",
            label_visibility="collapsed",
        )
        if selected_lang != current_lang:
            st.session_state["lang"] = selected_lang
            try:
                qp = getattr(st, "query_params", None)
                if qp is not None:
                    qp["lang"] = selected_lang
            except Exception:
                pass
            st.rerun()

        st.markdown('<div class="miq-topnav"></div>', unsafe_allow_html=True)
        btn_home = btn_before = btn_during = btn_after = btn_admin = False
        # Popover bevorzugen, Expander als Fallback
        try:
            pop = st.popover(f"☰ {t('nav')}")
            with pop:
                btn_home = st.button(t("home"), use_container_width=True)
                btn_before = st.button(t("phase_before"), use_container_width=True)
                btn_during = st.button(t("phase_during"), use_container_width=True)
                btn_after = st.button(t("phase_after"), use_container_width=True)
                # Admin-Button nur für Administratoren einblenden (zwischen Während und Abmelden)
                btn_admin = st.button(t("admin"), use_container_width=True) if is_admin else False
                if st.session_state.get("auth_user"):
                    if st.button(t("auth_logout"), use_container_width=True):
                        st.session_state.pop("auth_user", None)
                        st.rerun()
        except Exception:
            with st.expander(f"☰ {t('nav')}", expanded=False):
                btn_home = st.button(t("home"), use_container_width=True)
                btn_before = st.button(t("phase_before"), use_container_width=True)
                btn_during = st.button(t("phase_during"), use_container_width=True)
                btn_after = st.button(t("phase_after"), use_container_width=True)
                btn_admin = st.button(t("admin"), use_container_width=True) if is_admin else False
                if st.session_state.get("auth_user"):
                    if st.button(t("auth_logout"), use_container_width=True):
                        st.session_state.pop("auth_user", None)
                        st.rerun()

    if btn_home:
        st.switch_page("app.py")
    elif btn_before:
        st.switch_page("pages/1_Vor_dem_Kauf.py")
    elif btn_during:
        st.switch_page("pages/2_Waehrend_des_Kaufs.py")
    elif btn_after:
        st.switch_page("pages/3_Nach_dem_Kauf.py")
    elif btn_admin:
        st.switch_page("pages/0_Admin.py")

def fmt_currency(value: float, decimals: int = 0) -> str:
    """Formatiert Währungswerte je Sprache (DE/EN/AR) mit Euro-Symbol."""
    import streamlit as st
    lang = st.session_state.get("lang", "de")
    if lang == "de":
        return fmt_eur(value, decimals)
    # EN & AR: nutze englische Formatierung, Euro bleibt erhalten
    s = f"{value:,.{decimals}f} €"
    # In arabischer Ansicht mit LRM umbrechen, damit Ziffern LTR bleiben
    if lang == "ar":
        lrm = "\u200E"
        return f"{lrm}{s}{lrm}"
    return s

def fmt_number(value: float, decimals: int = 2) -> str:
    """
    Formatiert eine Zahl ohne Währung je nach Sprache.
    - Deutsch: Tausenderpunkt, Dezimalkomma (z. B. 4.000,00)
    - Englisch & Arabisch: Tausenderkomma, Dezimalpunkt (z. B. 4,000.00)
    """
    import streamlit as st
    lang = st.session_state.get("lang", "de")
    s = f"{value:,.{decimals}f}"
    if lang == "de":
        s = s.replace(",", "__T__").replace(".", ",").replace("__T__", ".")
    # Für Englisch bleibt das Standardformat erhalten; Arabisch: sichere LTR mit LRM
    if lang == "ar":
        lrm = "\u200E"
        return f"{lrm}{s}{lrm}"
    return s

def parse_localized_number(text: str, default: float = 0.0) -> float:
    """Parst eine lokalisierte Zahl (z. B. '4.000,00' oder '4,000.00') robust zu float."""
    try:
        s = str(text).strip()
        if not s:
            return default
        # Entferne Leerzeichen und Apostroph als Tausendertrennzeichen
        s = s.replace(" ", "").replace("'", "")
        # Wenn sowohl "," als auch "." vorkommen, nutze das zuletzt auftretende als Dezimaltrenner
        if "," in s and "." in s:
            last_comma = s.rfind(",")
            last_dot = s.rfind(".")
            decimal = "," if last_comma > last_dot else "."
            thousands = "." if decimal == "," else ","
            s = s.replace(thousands, "")
            s = s.replace(decimal, ".")
            return float(s)
        # Nur Komma vorhanden -> deutsches Dezimaltrennzeichen
        if "," in s and "." not in s:
            s = s.replace(".", "")  # vorsorglich
            s = s.replace(",", ".")
            return float(s)
        # Nur Punkt vorhanden -> englisches/arabisches Dezimaltrennzeichen
        if "." in s and "," not in s:
            s = s.replace(",", "")
            return float(s)
        # Keine Trennzeichen -> reine Ganzzahl
        return float(s)
    except Exception:
        return default


def number_input_localized_on_change(ui_key: str, state_key: str | None, decimals: int = 2):
    """
    Callback for Streamlit `on_change` to parse the raw text, update the
    persisted numeric state and replace the visible text with a localized
    formatted representation.
    """
    import streamlit as st
    try:
        raw = st.session_state.get(ui_key, "")
        current_val = st.session_state.get(state_key, 0.0) if state_key else 0.0
        parsed = parse_localized_number(raw, default=current_val)
        if state_key:
            st.session_state[state_key] = parsed
        display_after = fmt_number(parsed, decimals)
        # Update the visible text input to the localized formatted value
        st.session_state[ui_key] = display_after
    except Exception:
        # Silently ignore formatting errors to avoid breaking the UI
        return

def number_input_localized(label: str, value: float, min_value: float = 0.0, decimals: int = 2, key: str | None = None):
    """
    Wrapper um eine lokalisierte Zahleneingabe via Textfeld.
    - Zeigt die Zahl mit Sprachformatierung an
    - Gibt den geparsten float-Wert zurück (min_value wird beachtet)
    Hinweis: `st.number_input` ist nicht voll lokalisiert; dieses Feld ersetzt es.
    """
    import streamlit as st
    lang = st.session_state.get("lang", "de")
    # Persist numeric value under a stable state key; use language-specific UI key to reset on language switch
    state_key = f"{key}_val" if key else None
    current_val = st.session_state.get(state_key, value) if state_key else value
    display = fmt_number(current_val, decimals)
    ui_key = f"{key}_{lang}" if key else None
    # Note: Streamlit does not allow widget callbacks inside `st.form` except
    # on the form submit button. To support forms and regular pages we avoid
    # using `on_change` here. Instead we parse the input and update the
    # visible text with a localized formatted value immediately after parsing.
    if ui_key:
        # Initialize session state with the formatted display value if not already set
        if ui_key not in st.session_state:
            st.session_state[ui_key] = display
        # Try to attach an on_change callback to format immediately when the
        # user finishes editing. If this widget happens to be inside a form,
        # Streamlit will raise an exception for callbacks on widgets inside
        # forms (only form_submit_button supports callbacks). We catch that
        # and fall back to a plain text_input to avoid crashing the app.
        try:
            text = st.text_input(label, key=ui_key, on_change=number_input_localized_on_change, args=(ui_key, state_key, decimals))
        except Exception:
            text = st.text_input(label, key=ui_key)
    else:
        text = st.text_input(label, value=display)
    parsed = parse_localized_number(text, default=current_val)
    if state_key:
        st.session_state[state_key] = parsed
    if parsed < min_value:
        parsed = min_value
    # Aktualisiere das sichtbare Textfeld mit der lokalisierten Darstellung
    # (z. B. 3000 -> 3.000,00 für DE oder 3,000.00 für EN/AR). Diese direkte
    # Aktualisierung funktioniert auch innerhalb von `st.form` (ohne Callbacks).
    try:
        display_after = fmt_number(parsed, decimals)
        # Setze nur, wenn sich der Text unterscheidet (vermeidet unnötige Reruns)
        if ui_key and st.session_state.get(ui_key, None) != display_after:
            st.session_state[ui_key] = display_after
            # Force a rerun so the updated formatted value is shown immediately.
            # This is safe because on the next run the value equals display_after
            # and we won't trigger another rerun.
            try:
                st.experimental_rerun()
            except Exception:
                # If rerun fails for any reason, ignore and continue.
                pass
    except Exception:
        pass

    return parsed
