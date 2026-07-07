from __future__ import annotations

import streamlit as st

from config import ASSETS_DIR
from utils import apply_theme, ensure_initialized, page_footer, top_banner

st.set_page_config(
    page_title="Etiqa Motor Insurance System",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()
ensure_initialized()

top_banner()

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #0A1F3D 0%, #1A3860 100%);
        border-radius: 14px;
        padding: 48px 52px;
        margin-bottom: 28px;
        box-shadow: 0 8px 32px rgba(10,31,61,0.22);
        text-align: center;
    ">
        <div style="font-family:'Inter',sans-serif;font-size:2rem;font-weight:800;
            color:#FFFFFF;margin-bottom:12px;letter-spacing:-0.02em;">
            Welcome to Etiqa Motor Vehicle Insurance
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1rem;color:#A8BEDB;
            max-width:600px;margin:0 auto;line-height:1.7;">
            End-to-end insurance management — from customer registration to policy issuance
            and executive analytics, powered by OJK-compliant calculations.
        </div>
        <div style="margin-top:20px;font-family:'Inter',sans-serif;font-size:0.8rem;
            color:#C8973A;font-weight:600;letter-spacing:0.06em;">
            Use the sidebar to navigate between pages ›
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page_footer()
