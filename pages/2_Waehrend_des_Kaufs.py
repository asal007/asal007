import streamlit as st
from utils import fmt_currency, inject_top_nav, number_input_localized, hide_sidebar_completely, hide_header_actions_for_non_admin
from i18n import t, language_selector, apply_rtl_if_needed
from auth import login_gate, logout_button

st.set_page_config(page_title="Phase 2", page_icon="🏠", layout="wide")

# Auth-Gate
login_gate()

language_selector()
apply_rtl_if_needed()
hide_sidebar_completely()
hide_header_actions_for_non_admin()

inject_top_nav()

st.title(t("phase2_title"))
st.caption(t("phase2_caption"))

if "favoriten" not in st.session_state:
    st.session_state["favoriten"] = []

st.header(t("search_selection_header"))
with st.form("favoriten_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        titel = st.text_input(t("title_object"))
        preis = number_input_localized(t("price_euro"), value=450000.0, min_value=0.0, decimals=2, key="fav_price")
    with col2:
        lage = st.text_input(t("location_city"))
        qm = number_input_localized(t("living_area"), value=100.0, min_value=0.0, decimals=0, key="fav_qm")
    with col3:
        energie_options = [t("energy_a_plus"), t("energy_a"), t("energy_b"), t("energy_c"), t("energy_d"), t("energy_e"), t("energy_f"), t("energy_g")]
        energie = st.selectbox(t("energy_class"), energie_options)
        zustand_options = [t("condition_new"), t("condition_good"), t("condition_renovation"), t("condition_restoration")]
        zustand = st.selectbox(t("condition"), zustand_options)
    notizen = st.text_area(t("notes"))
    fotos = st.file_uploader(t("add_photos"), type=["png","jpg","jpeg"], accept_multiple_files=True)
    add = st.form_submit_button(t("save_to_favorites"))

if add and titel:
    st.session_state.favoriten.append({
        "titel": titel,
        "preis": preis,
        "lage": lage,
        "qm": qm,
        "energie": energie,
        "zustand": zustand,
        "notizen": notizen,
        "fotos": fotos or []
    })
    st.success(f"'{titel}' {t('added_to_favorites')}.")

if st.session_state.favoriten:
    st.subheader(t("favorites_list"))
    for i, fav in enumerate(st.session_state.favoriten):
        with st.expander(f"{fav['titel']} – {fmt_currency(fav['preis'], 0)} {t('in_word')} {fav['lage']}"):
            colA, colB, colC = st.columns(3)
            with colA:
                from utils import fmt_number
                st.write(f"{t('living_area_label')}: {fmt_number(fav['qm'], 0)} {t('sqm_unit')}")
                pm2 = fav['preis']/fav['qm'] if fav['qm'] else 0
                st.write(f"{t('price_per_sqm')}: {fmt_currency(pm2, 0).replace(' €', '')} {t('eur_per_sqm')}")
            with colB:
                st.write(f"{t('energy_label')}: {fav['energie']}")
                st.write(f"{t('condition_label')}: {fav['zustand']}")
            with colC:
                st.write(f"{t('notes_label')}:")
                st.write(fav["notizen"]) 
            if fav["fotos"]:
                st.write(f"{t('photos_label')}:")
                for f in fav["fotos"]:
                    try:
                        st.image(f, use_column_width=True)
                    except Exception:
                        st.caption(t("photo_error"))

st.header(t("viewing_eval"))
colD, colE = st.columns(2)
with colD:
    besichtigungsdatum = st.date_input(t("viewing_date"))
    besichtigungszeit = st.time_input(t("viewing_time"))
with colE:
    st.checkbox(t("check_energycert"))
    st.checkbox(t("check_renovation"))
    st.checkbox(t("checklist_attention"))

st.header(t("finance_bank"))
st.checkbox(t("bank_docs"))
st.checkbox(t("save_compare_offers"))
st.checkbox(t("loan_compare_done"))

st.header(t("contract_notary"))
st.markdown(t("doc_overview"))
# Dokumentenübersicht (Tabelle)
cat = t("col_category"); doc = t("col_document"); desc = t("col_description")
docs_rows = [
    {cat: t("cat_personal"),    doc: t("doc_personal_list"),    desc: t("desc_personal")},
    {cat: t("cat_financing"),   doc: t("doc_financing_list"),   desc: t("desc_financing")},
    {cat: t("cat_property"),    doc: t("doc_property_list"),    desc: t("desc_property")},
    {cat: t("cat_contract"),    doc: t("doc_contract_list"),    desc: t("desc_contract")},
    {cat: t("cat_authorities"), doc: t("doc_authorities_list"), desc: t("desc_authorities")},
]
st.table(docs_rows)

st.checkbox(t("contract_draft"))
st.checkbox(t("land_register_extract"))
st.checkbox(t("partition_declaration"))
st.checkbox(t("energy_cert"))
st.markdown(t("notary_expl"))

st.success("Erinnerung erstellen: Notartermin am Datum/Uhrzeit oben gespeichert.")