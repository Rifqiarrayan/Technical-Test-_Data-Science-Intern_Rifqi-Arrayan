from __future__ import annotations

from datetime import date

import streamlit as st

from config import APP_SUBTITLE, APP_TITLE
from database import initialize_database


def format_currency(amount: float) -> str:
    return f"IDR {amount:,.0f}"


def status_badge(status: str) -> str:
    color_map = {
        "Submitted": "#F59E0B",
        "Document Verified": "#3B82F6",
        "Underwriting": "#6366F1",
        "Approved": "#10B981",
        "Rejected": "#EF4444",
        "Policy Issued": "#0EA5E9",
        "Need Survey": "#8B5CF6",
        "Issued": "#14B8A6",
    }
    color = color_map.get(status, "#1F2937")
    return (
        f"<span style='background:{color};color:white;padding:4px 10px;"
        "border-radius:999px;font-size:12px;font-weight:600;'>"
        f"{status}</span>"
    )


def apply_theme() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #F3F9FF 0%, #E9F2FF 40%, #FFFFFF 100%);
            }
            .block-container {
                padding-top: 1.2rem;
                padding-bottom: 2rem;
            }
            .metric-card {
                background: #FFFFFF;
                border: 1px solid #D7E5FF;
                border-radius: 12px;
                padding: 14px;
                box-shadow: 0 6px 18px rgba(32, 76, 146, 0.06);
            }
            .section-title {
                color: #0B2B5C;
                font-weight: 700;
                margin-top: 0.4rem;
            }
            .small-note {
                color: #4B5563;
                font-size: 0.9rem;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def ensure_initialized() -> None:
    if "_initialized" not in st.session_state:
        with st.spinner("Initializing insurance system and data..."):
            initialize_database()
            st.session_state["_initialized"] = True


def top_banner() -> None:
    st.title(APP_TITLE)
    st.caption(APP_SUBTITLE)
    st.markdown(f"System Date: **{date.today()}**")
