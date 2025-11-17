import math
import streamlit as st
from utils import fmt_currency, inject_top_nav, number_input_localized, hide_sidebar_completely, hide_header_actions_for_non_admin
from i18n import t, language_selector, apply_rtl_if_needed
from auth import login_gate, logout_button

st.set_page_config(page_title="Phase 1", page_icon="🏁", layout="wide")

# Auth-Gate
login_gate()

language_selector()
apply_rtl_if_needed()
hide_sidebar_completely()
hide_header_actions_for_non_admin()

inject_top_nav()

st.title(t("phase1_title"))
st.caption(t("phase1_caption"))

st.header(t("financial_prep"))
st.subheader(t("budget_calc"))

with st.container():
    col_a, col_b = st.columns(2)
    with col_a:
        einkommen = number_input_localized(t("income_monthly"), value=4000.0, min_value=0.0, decimals=2, key="inp_income")
        ausgaben = number_input_localized(t("expenses_monthly"), value=2000.0, min_value=0.0, decimals=2, key="inp_expenses")
        reserve = number_input_localized(t("reserve_monthly"), value=300.0, min_value=0.0, decimals=2, key="inp_reserve")
        eigenkapital = number_input_localized(t("equity"), value=80000.0, min_value=0.0, decimals=2, key="inp_equity")
    with col_b:
        zins = number_input_localized(t("interest_pa"), value=3.5, min_value=0.0, decimals=2, key="inp_interest")
        laufzeit_j = int(number_input_localized(t("term_years"), value=30, min_value=1, decimals=0, key="inp_term"))
        nk_prozent = st.slider(t("closing_costs_pct"), min_value=5, max_value=15, value=10)
    submitted = st.button(t("calc_max_price"))

    # Debug: Zeige gespeicherte Session-Keys für die numerischen Eingaben
    if st.checkbox("Debug: Zahlenfelder anzeigen", key="debug_numbers"):
        lang = st.session_state.get("lang", "de")
        keys = [
            ("inp_income", "Einkommen"),
            ("inp_expenses", "Ausgaben"),
            ("inp_reserve", "Reserve"),
            ("inp_equity", "Eigenkapital"),
        ]
        debug = {}
        for k, label in keys:
            state_key = f"{k}_val"
            ui_key = f"{k}_{lang}"
            debug[label] = {
                "ui_key": ui_key,
                "ui_value": st.session_state.get(ui_key),
                "state_key": state_key,
                "parsed_value": st.session_state.get(state_key),
            }
        st.json(debug)

if submitted:
    verfuegbare_rate = max(0.0, einkommen - ausgaben - reserve)
    i = (zins / 100.0) / 12.0
    n = laufzeit_j * 12
    if i > 0:
        kreditbetrag_max = verfuegbare_rate * (1 - (1 + i) ** (-n)) / i
    else:
        kreditbetrag_max = verfuegbare_rate * n
    nk_faktor = 1 + (nk_prozent / 100.0)
    max_kaufpreis = (kreditbetrag_max + eigenkapital) / nk_faktor

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t("available_rate"), fmt_currency(verfuegbare_rate, 0))
    with col2:
        st.metric(t("max_loan"), fmt_currency(kreditbetrag_max, 0))
    with col3:
        st.metric(t("max_price_incl"), fmt_currency(max_kaufpreis, 0))

st.subheader(t("closing_costs"))
bundesland_saetze = {
    "Baden-Württemberg": 5.0,
    "Bayern": 3.5,
    "Berlin": 6.0,
    "Brandenburg": 6.5,
    "Bremen": 5.0,
    "Hamburg": 4.5,
    "Hessen": 6.0,
    "Mecklenburg-Vorpommern": 5.0,
    "Niedersachsen": 5.0,
    "Nordrhein-Westfalen": 6.5,
    "Rheinland-Pfalz": 5.0,
    "Saarland": 6.5,
    "Sachsen": 3.5,
    "Sachsen-Anhalt": 5.0,
    "Schleswig-Holstein": 6.5,
    "Thüringen": 6.5,
}
colx, coly = st.columns(2)
with colx:
    kaufpreis_nk = number_input_localized(t("purchase_price"), value=500000.0, min_value=0.0, decimals=2, key="nk_kaufpreis")
    land = st.selectbox(t("state_land_tax"), options=list(bundesland_saetze.keys()), index=1)
with coly:
    notar_prozent = st.slider(t("notary_reg_pct"), 1, 2, 2)
    makler_prozent = st.slider(t("broker_pct"), 0, 7, 3)

grunderwerbsteuer = kaufpreis_nk * (bundesland_saetze[land] / 100.0)
notar_grundbuch = kaufpreis_nk * (notar_prozent / 100.0)
makler = kaufpreis_nk * (makler_prozent / 100.0)
summe_nk = grunderwerbsteuer + notar_grundbuch + makler

colN1, colN2, colN3, colN4 = st.columns(4)
with colN1:
    st.metric(t("land_tax"), fmt_currency(grunderwerbsteuer, 0), help=t("land_tax_help"))
with colN2:
    st.metric(t("notary_reg"), fmt_currency(notar_grundbuch, 0))
with colN3:
    st.metric(t("broker"), fmt_currency(makler, 0))
with colN4:
    st.metric(t("closing_costs_total"), fmt_currency(summe_nk, 0))

st.caption(t("tip_values_note"))

st.subheader(t("financing_calc"))
colF1, colF2, colF3 = st.columns(3)
with colF1:
    kaufpreis_fin = number_input_localized(t("purchase_price"), value=500000.0, min_value=0.0, decimals=2, key="fin_kaufpreis")
    eigenkapital_fin = number_input_localized(t("equity"), value=80000.0, min_value=0.0, decimals=2, key="fin_equity")
with colF2:
    zins_pa = number_input_localized(t("interest_pa"), value=3.5, min_value=0.0, decimals=2, key="fin_zins")
    laufzeit_j_fin = int(number_input_localized(t("term_years"), value=30, min_value=1, decimals=0, key="fin_laufzeit"))
with colF3:
    neb_kosten = number_input_localized(t("closing_costs_euro"), value=summe_nk, min_value=0.0, decimals=2, key="fin_nebkosten")

darlehen = max(0.0, kaufpreis_fin + neb_kosten - eigenkapital_fin)
i_fin = (zins_pa / 100.0) / 12.0
n_fin = int(laufzeit_j_fin * 12)
rate_monat = (darlehen * i_fin) / (1 - (1 + i_fin) ** (-n_fin)) if i_fin > 0 and n_fin > 0 else 0.0
zins_gesamt = rate_monat * n_fin - darlehen if rate_monat > 0 else 0.0

colR1, colR2, colR3 = st.columns(3)
with colR1:
    st.metric(t("loan_amount"), fmt_currency(darlehen, 0))
with colR2:
    st.metric(t("monthly_rate"), fmt_currency(rate_monat, 0))
with colR3:
    st.metric(t("total_interest"), fmt_currency(zins_gesamt, 0))

st.header(t("docs_prepare"))
st.checkbox(t("doc_pass"), key="doc_pass")
st.checkbox(t("doc_income"), key="doc_income")
st.checkbox(t("doc_equity"), key="doc_equity")
st.checkbox(t("doc_loans"), key="doc_loans")
st.checkbox(t("doc_object"), key="doc_object")

st.header(t("knowledge_tips"))
with st.expander(t("exp_flat_vs_house_title")):
    st.write(t("exp_flat_vs_house_body"))
with st.expander(t("exp_ready_check_title")):
    st.write(t("exp_ready_check_body"))
with st.expander(t("exp_rent_vs_buy_title")):
    st.write(t("exp_rent_vs_buy_body"))