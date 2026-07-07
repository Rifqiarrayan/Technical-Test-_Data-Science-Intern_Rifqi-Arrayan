from __future__ import annotations

from datetime import date

import streamlit as st

from config import APP_SUBTITLE, APP_TITLE
from database import initialize_database


def format_currency(amount: float) -> str:
    return f"IDR {amount:,.0f}"


def status_badge(status: str) -> str:
    color_map = {
        "Submitted": "#D97706",
        "Document Verified": "#1A56DB",
        "Underwriting": "#6C3FC5",
        "Approved": "#0D7C4E",
        "Rejected": "#C0392B",
        "Policy Issued": "#0369A1",
        "Need Survey": "#7C3AED",
        "Issued": "#0F766E",
    }
    color = color_map.get(status, "#1F2937")
    return (
        f"<span style='"
        f"background:{color};"
        f"color:#FFFFFF;"
        f"padding:5px 14px;"
        f"border-radius:4px;"
        f"font-size:11px;"
        f"font-weight:700;"
        f"letter-spacing:0.06em;"
        f"text-transform:uppercase;"
        f"font-family:Inter,sans-serif;"
        f"box-shadow:0 1px 4px rgba(0,0,0,0.18);"
        f"'>{status}</span>"
    )


def apply_theme() -> None:
    st.markdown(
        """
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            /* ── Base ────────────────────────────────────────────── */
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            }

            .stApp {
                background: #F0F4F9;
            }

            /* ── Block container ─────────────────────────────────── */
            .block-container {
                padding-top: 3.5rem !important;
                padding-bottom: 3rem !important;
                max-width: 1280px;
            }

            /* ── Sidebar ─────────────────────────────────────────── */
            [data-testid="stSidebar"] {
                background: linear-gradient(175deg, #0A1F3D 0%, #102A50 60%, #0D2244 100%) !important;
                border-right: 1px solid rgba(200,151,58,0.25) !important;
            }
            [data-testid="stSidebar"] * {
                color: #CBD8E8 !important;
                font-family: 'Inter', sans-serif !important;
            }
            [data-testid="stSidebar"] a,
            [data-testid="stSidebar"] .st-emotion-cache-1rtdyuf,
            [data-testid="stSidebar"] span {
                color: #CBD8E8 !important;
            }
            [data-testid="stSidebar"] [aria-selected="true"] span,
            [data-testid="stSidebar"] [aria-selected="true"] {
                color: #C8973A !important;
                font-weight: 600 !important;
            }
            [data-testid="stSidebar"] hr {
                border-color: rgba(200,151,58,0.2) !important;
            }
            /* Sidebar nav items hover */
            [data-testid="stSidebar"] li:hover span {
                color: #C8973A !important;
            }

            /* ── Headings ────────────────────────────────────────── */
            h1, h2, h3, h4 {
                color: #0A1F3D !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 700 !important;
                letter-spacing: -0.01em;
            }
            h1 { font-size: 1.85rem !important; }
            h2 { font-size: 1.45rem !important; }
            h3 { font-size: 1.1rem !important; }

            /* ── Inputs ──────────────────────────────────────────── */
            [data-testid="stTextInput"] input,
            [data-testid="stNumberInput"] input,
            [data-testid="stTextArea"] textarea,
            [data-testid="stDateInput"] input {
                border: 1px solid #C9D7E8 !important;
                border-radius: 6px !important;
                background: #FFFFFF !important;
                color: #0A1F3D !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.875rem !important;
                padding: 8px 12px !important;
                transition: border-color 0.2s ease, box-shadow 0.2s ease;
            }
            [data-testid="stTextInput"] input:focus,
            [data-testid="stNumberInput"] input:focus,
            [data-testid="stTextArea"] textarea:focus {
                border-color: #C8973A !important;
                box-shadow: 0 0 0 3px rgba(200,151,58,0.15) !important;
                outline: none !important;
            }
            label, .stSelectbox label, .stRadio label {
                color: #2C3E5A !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
                letter-spacing: 0.03em !important;
                text-transform: uppercase !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* ── Selectbox ───────────────────────────────────────── */
            [data-testid="stSelectbox"] > div > div {
                border: 1px solid #C9D7E8 !important;
                border-radius: 6px !important;
                background: #FFFFFF !important;
                color: #0A1F3D !important;
                font-family: 'Inter', sans-serif !important;
            }

            /* ── Buttons ─────────────────────────────────────────── */
            .stButton > button[kind="primary"],
            button[data-testid="baseButton-primary"] {
                background: linear-gradient(135deg, #C8973A 0%, #A97A2A 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 6px !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
                letter-spacing: 0.04em !important;
                padding: 0.55rem 1.6rem !important;
                box-shadow: 0 3px 10px rgba(200,151,58,0.35) !important;
                transition: all 0.2s ease !important;
            }
            .stButton > button[kind="primary"]:hover,
            button[data-testid="baseButton-primary"]:hover {
                background: linear-gradient(135deg, #D4A44A 0%, #B88B38 100%) !important;
                box-shadow: 0 5px 16px rgba(200,151,58,0.45) !important;
                transform: translateY(-1px) !important;
            }
            .stButton > button[kind="secondary"] {
                background: #FFFFFF !important;
                color: #0A1F3D !important;
                border: 1px solid #C9D7E8 !important;
                border-radius: 6px !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
            }

            /* ── Download button ─────────────────────────────────── */
            [data-testid="stDownloadButton"] button {
                background: linear-gradient(135deg, #C8973A 0%, #A97A2A 100%) !important;
                color: #FFFFFF !important;
                border: none !important;
                border-radius: 6px !important;
                font-family: 'Inter', sans-serif !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
                letter-spacing: 0.04em !important;
                padding: 0.55rem 1.6rem !important;
                box-shadow: 0 3px 10px rgba(200,151,58,0.35) !important;
                transition: all 0.2s ease !important;
            }
            [data-testid="stDownloadButton"] button:hover {
                background: linear-gradient(135deg, #D4A44A 0%, #B88B38 100%) !important;
                box-shadow: 0 5px 16px rgba(200,151,58,0.45) !important;
                transform: translateY(-1px) !important;
            }

            /* ── Metrics ─────────────────────────────────────────── */
            [data-testid="stMetric"] {
                background: #FFFFFF !important;
                border: 1px solid #DDE4EE !important;
                border-radius: 10px !important;
                padding: 16px 20px !important;
                box-shadow: 0 2px 12px rgba(10,31,61,0.06) !important;
            }
            [data-testid="stMetricLabel"] {
                color: #4B5E78 !important;
                font-size: 0.75rem !important;
                font-weight: 600 !important;
                text-transform: uppercase !important;
                letter-spacing: 0.06em !important;
            }
            [data-testid="stMetricValue"] {
                color: #0A1F3D !important;
                font-size: 1.5rem !important;
                font-weight: 700 !important;
            }

            /* ── Dataframe / Table ───────────────────────────────── */
            [data-testid="stDataFrame"] {
                border-radius: 10px !important;
                overflow: hidden !important;
                border: 1px solid #DDE4EE !important;
                box-shadow: 0 2px 12px rgba(10,31,61,0.05) !important;
            }

            /* ── Alerts ──────────────────────────────────────────── */
            [data-testid="stAlert"] {
                border-radius: 8px !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.875rem !important;
            }

            /* ── Info / Success / Warning / Error ────────────────── */
            div[data-testid="stAlert"][kind="info"] {
                background: #EEF4FF !important;
                border-left: 4px solid #1A56DB !important;
                color: #1A3860 !important;
            }
            div[data-testid="stAlert"][kind="success"] {
                background: #ECFDF5 !important;
                border-left: 4px solid #0D7C4E !important;
                color: #064E3B !important;
            }
            div[data-testid="stAlert"][kind="warning"] {
                background: #FFFBEB !important;
                border-left: 4px solid #D97706 !important;
                color: #78350F !important;
            }
            div[data-testid="stAlert"][kind="error"] {
                background: #FEF2F2 !important;
                border-left: 4px solid #C0392B !important;
                color: #7F1D1D !important;
            }

            /* ── Form ────────────────────────────────────────────── */
            [data-testid="stForm"] {
                background: #FFFFFF !important;
                border: 1px solid #DDE4EE !important;
                border-radius: 12px !important;
                padding: 28px 32px !important;
                box-shadow: 0 2px 16px rgba(10,31,61,0.06) !important;
            }

            /* ── Spinner ─────────────────────────────────────────── */
            .stSpinner > div {
                border-color: #C8973A transparent transparent transparent !important;
            }

            /* ── Horizontal rule ─────────────────────────────────── */
            hr {
                border: none !important;
                border-top: 1px solid #DDE4EE !important;
                margin: 1.5rem 0 !important;
            }

            /* ── Multiselect ─────────────────────────────────────── */
            [data-testid="stMultiSelect"] [data-baseweb="tag"] {
                background-color: #EEF4FF !important;
                color: #1A3860 !important;
                border-radius: 4px !important;
                font-family: 'Inter', sans-serif !important;
                font-size: 0.8rem !important;
                font-weight: 600 !important;
            }

            /* ── Radio buttons ───────────────────────────────────── */
            [data-testid="stRadio"] label {
                text-transform: none !important;
                font-size: 0.875rem !important;
                font-weight: 500 !important;
                color: #0A1F3D !important;
            }

            /* ── Premium card utility class ──────────────────────── */
            .etiqa-card {
                background: #FFFFFF;
                border: 1px solid #DDE4EE;
                border-radius: 12px;
                padding: 24px 28px;
                box-shadow: 0 2px 16px rgba(10,31,61,0.06);
                margin-bottom: 1.2rem;
            }
            .etiqa-section-header {
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 12px 0 10px 0;
                border-bottom: 2px solid #C8973A;
                margin-bottom: 20px;
            }
            .etiqa-section-header span {
                font-size: 0.95rem;
                font-weight: 700;
                color: #0A1F3D;
                letter-spacing: 0.01em;
                text-transform: uppercase;
            }
            .etiqa-kpi-card {
                background: #FFFFFF;
                border: 1px solid #DDE4EE;
                border-radius: 12px;
                padding: 20px 22px;
                box-shadow: 0 2px 12px rgba(10,31,61,0.07);
                text-align: center;
                transition: box-shadow 0.2s ease, transform 0.2s ease;
            }
            .etiqa-kpi-card:hover {
                box-shadow: 0 6px 22px rgba(10,31,61,0.12);
                transform: translateY(-2px);
            }
            .etiqa-kpi-label {
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                color: #4B5E78;
                margin-bottom: 6px;
            }
            .etiqa-kpi-value {
                font-size: 1.6rem;
                font-weight: 800;
                color: #0A1F3D;
                line-height: 1.2;
            }
            .etiqa-kpi-icon {
                font-size: 1.4rem;
                margin-bottom: 8px;
            }

            /* ── Footer ──────────────────────────────────────────── */
            .etiqa-footer {
                text-align: center;
                padding: 32px 0 16px 0;
                color: #8A9ABB;
                font-size: 0.75rem;
                font-family: 'Inter', sans-serif;
                letter-spacing: 0.04em;
                border-top: 1px solid #DDE4EE;
                margin-top: 3rem;
            }
            .etiqa-footer strong {
                color: #C8973A;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_footer() -> None:
    st.markdown(
        "<div class='etiqa-footer'>Made with by <strong>Rifqi Arrayan Muttaqien</strong> &nbsp;|&nbsp; Etiqa Motor Vehicle Insurance System</div>",
        unsafe_allow_html=True,
    )


def ensure_initialized() -> None:
    if "_initialized" not in st.session_state:
        with st.spinner("Initializing insurance system and data..."):
            initialize_database()
            st.session_state["_initialized"] = True


def top_banner() -> None:
    today = date.today().strftime("%d %B %Y")
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #0A1F3D 0%, #1A3860 100%);
            border-radius: 12px;
            padding: 20px 32px;
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            box-shadow: 0 4px 20px rgba(10,31,61,0.18);
        ">
            <div>
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 1.5rem;
                    font-weight: 800;
                    color: #FFFFFF;
                    letter-spacing: -0.01em;
                    line-height: 1.2;
                ">{APP_TITLE}</div>
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 0.8rem;
                    color: #A8BEDB;
                    margin-top: 4px;
                    letter-spacing: 0.03em;
                ">{APP_SUBTITLE}</div>
            </div>
            <div style="text-align: right;">
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 0.7rem;
                    color: #C8973A;
                    font-weight: 700;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                ">System Date</div>
                <div style="
                    font-family: 'Inter', sans-serif;
                    font-size: 0.9rem;
                    color: #FFFFFF;
                    font-weight: 600;
                    margin-top: 2px;
                ">{today}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
