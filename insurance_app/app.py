from __future__ import annotations

import streamlit as st

from utils import apply_theme, ensure_initialized

st.set_page_config(
    page_title="Etiqa Motor Insurance System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
ensure_initialized()
st.switch_page("pages/1_Dashboard.py")
