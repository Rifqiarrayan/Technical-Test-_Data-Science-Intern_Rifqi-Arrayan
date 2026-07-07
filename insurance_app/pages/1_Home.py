from __future__ import annotations

import streamlit as st

from config import ASSETS_DIR
from utils import apply_theme, ensure_initialized, top_banner

st.set_page_config(page_title="Home", page_icon="🏠", layout="wide")
apply_theme()
ensure_initialized()

top_banner()

logo_path = ASSETS_DIR / "logo.png"
banner_path = ASSETS_DIR / "banner.png"

col1, col2 = st.columns([1, 2])
with col1:
    if logo_path.exists():
        st.image(str(logo_path), use_container_width=True)
with col2:
    if banner_path.exists():
        st.image(str(banner_path), use_container_width=True)

st.markdown("## Motor Vehicle Insurance Prototype")
st.write(
    "This production-style prototype demonstrates insurance business process automation, "
    "data processing, premium calculation based on OJK rates, underwriting decision rules, "
    "policy issuance, and interactive business analytics."
)

c1, c2 = st.columns(2)
with c1:
    st.success("Comprehensive Coverage")
    st.write("Protects against own damage, partial losses, and selected additional risks.")
with c2:
    st.success("Total Loss Only (TLO)")
    st.write("Protects total loss or theft scenarios as defined by policy terms.")

st.markdown("### Workflow Diagram")
st.graphviz_chart(
    """
    digraph G {
        rankdir=TB;
        node [shape=box, style=filled, color="#DBEAFE", fontname="Arial"];
        A [label="Customer Registration"];
        B [label="Vehicle Information"];
        C [label="Coverage Selection"];
        D [label="Premium Calculation (OJK)"];
        E [label="Application Submission"];
        F [label="Document Verification"];
        G [label="Underwriting (Rule-Based)"];
        H [label="Approval / Rejection"];
        I [label="Policy Issuance"];
        J [label="Analytics Dashboard"];
        A -> B -> C -> D -> E -> F -> G -> H -> I -> J;
    }
    """
)

if st.button("Start Application", type="primary"):
    try:
        st.switch_page("pages/2_New_Application.py")
    except Exception:
        st.info("Open the New Application page from sidebar.")
