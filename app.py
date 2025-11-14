import streamlit as st
from utils import inject_top_nav, hide_sidebar_completely, hide_header_actions_for_non_admin
from i18n import t, language_selector, apply_rtl_if_needed
from auth import login_gate

st.set_page_config(page_title="MeinImmoKauf", page_icon="icon.png", layout="wide")

# Auth-Gate: Wenn nicht angemeldet, stoppe hier
login_gate()

# Header sofort ausblenden, um Flash zu vermeiden
hide_header_actions_for_non_admin()

language_selector()
apply_rtl_if_needed()
hide_sidebar_completely()

# Top-Navigation direkt am Seitenanfang einfügen
inject_top_nav()

st.title(t("app_title"))
st.subheader(t("app_sub"))

st.markdown(
    f"{t('intro_welcome')}\n\n{t('intro_find_phases')}\n{t('intro_p1')}\n{t('intro_p2')}\n{t('intro_p3')}\n\n{t('intro_goal')}"
)

st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(t("metrics_phases"), "3", t("metrics_phases_delta"))
with col2:
    st.metric(t("metrics_calculators"), "3", t("metrics_calculators_delta"))
with col3:
    st.metric(t("metrics_checklists"), t("many"), t("metrics_checklists_delta"))

st.info(t("info_tip"))