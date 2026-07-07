from __future__ import annotations

import streamlit as st

from config import ASSETS_DIR
from utils import apply_theme, ensure_initialized, top_banner

st.set_page_config(
    page_title="Etiqa Motor Insurance System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
ensure_initialized()

top_banner()

logo_path = ASSETS_DIR / "logo.png"
banner_path = ASSETS_DIR / "banner.png"

col1, col2 = st.columns([1, 3])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
with col2:
    if banner_path.exists():
        st.image(str(banner_path), use_container_width=True)

st.markdown("### Welcome")
st.write(
    "This application simulates an end-to-end motor vehicle insurance workflow "
    "from customer registration until policy issuance and analytics dashboard."
)

st.info("Use the sidebar to navigate through Home, New Application, Premium, Underwriting, Policy, and Dashboard pages.")

st.markdown("### Workflow")
st.markdown(
    "Customer → Vehicle Information → Coverage Selection → Premium Calculation (OJK) → "
    "Application Submission → Document Verification → Underwriting → Approval/Rejection → "
    "Policy Issued → Analytics Dashboard"
)
