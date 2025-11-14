import streamlit as st
from utils import inject_top_nav, hide_sidebar_completely, hide_header_actions_for_non_admin
from i18n import t, language_selector, apply_rtl_if_needed
from auth import login_gate, logout_button

st.set_page_config(page_title="Phase 3", page_icon="🔑", layout="wide")

# Auth-Gate
login_gate()

language_selector()
apply_rtl_if_needed()
hide_sidebar_completely()
hide_header_actions_for_non_admin()

inject_top_nav()

st.title(t("phase3_title"))
st.caption(t("phase3_caption"))

st.header(t("gov_registrations"))
st.checkbox(t("reg_meldeamt"))
st.checkbox(t("reg_tax"))
st.checkbox(t("reg_building_ins"))
st.checkbox(t("reg_utilities"))
st.checkbox(t("reg_gez"))
st.checkbox(t("reg_household_ins"))
st.checkbox(t("reg_post_forward"))

st.subheader(t("links_title"))
colL1, colL2, colL3 = st.columns(3)
with colL1:
    st.link_button(t("elster_tax"), "https://www.elster.de/")
    st.link_button(t("gez_fee"), "https://www.rundfunkbeitrag.de/")
with colL2:
    st.link_button(t("post_forwarding"), "https://shop.deutschepost.de/shop/mds/nachsendeservice.jsp")
    st.link_button(t("building_insurance_info"), "https://www.gdv.de/service/find/gdv/86764?query=hausratversicherungen")
with colL3:
    st.link_button(t("household_insurance_info"), "https://www.gdv.de/service/find/gdv/86764?query=wohngebaeudeversicherung")

st.header(t("practical_after"))
if "renovierung_todos" not in st.session_state:
    st.session_state["renovierung_todos"] = []
if "umzug_todos" not in st.session_state:
    st.session_state["umzug_todos"] = []

colA, colB = st.columns(2)
with colA:
    st.subheader(t("renovation_plan"))
    new_task = st.text_input(t("new_task"))
    add_task = st.button(t("add"))
    if add_task and new_task.strip():
        st.session_state.renovierung_todos.append({"text": new_task.strip(), "done": False})
    st.write(t("todo_list"))
    for i, task in enumerate(st.session_state.renovierung_todos):
        st.checkbox(task["text"], value=task["done"], key=f"renov_{i}")
        task["done"] = st.session_state[f"renov_{i}"]

with colB:
    st.subheader(t("move_planning"))
    new_umzug = st.text_input(t("new_move_task"))
    add_umzug = st.button(t("add"), key="add_umzug")
    if add_umzug and new_umzug.strip():
        st.session_state.umzug_todos.append({"text": new_umzug.strip(), "done": False})
    st.write(t("todo_list"))
    for i, task in enumerate(st.session_state.umzug_todos):
        st.checkbox(task["text"], value=task["done"], key=f"umzug_{i}")
        task["done"] = st.session_state[f"umzug_{i}"]

st.subheader(t("contracts_energy"))
st.checkbox(t("checked_energy_contracts"))
st.checkbox(t("compared_tariffs"))
st.checkbox(t("updated_insurances"))