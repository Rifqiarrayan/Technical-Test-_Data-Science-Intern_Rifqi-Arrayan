from __future__ import annotations

import streamlit as st

from config import ASSETS_DIR
from utils import apply_theme, ensure_initialized, page_footer, top_banner

st.set_page_config(page_title="Home | Etiqa Motor Insurance", page_icon="🏠", layout="wide")
apply_theme()
ensure_initialized()

top_banner()

# ── Hero Section ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #0A1F3D 0%, #1A3860 60%, #0D2244 100%);
        border-radius: 14px;
        padding: 48px 52px;
        margin-bottom: 28px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(10,31,61,0.22);
    ">
        <div style="
            position: absolute; top: 0; right: 0; width: 260px; height: 100%;
            background: linear-gradient(135deg, rgba(200,151,58,0.1) 0%, transparent 70%);
            border-radius: 14px;
        "></div>
        <div style="position: relative; z-index: 1;">
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 0.7rem;
                font-weight: 700;
                letter-spacing: 0.14em;
                text-transform: uppercase;
                color: #C8973A;
                margin-bottom: 12px;
            ">Etiqa Motor Vehicle Insurance</div>
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 2.2rem;
                font-weight: 800;
                color: #FFFFFF;
                line-height: 1.2;
                margin-bottom: 16px;
                letter-spacing: -0.02em;
            ">Protect What Moves You.<br>Drive with Confidence.</div>
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                color: #A8BEDB;
                max-width: 580px;
                line-height: 1.7;
                margin-bottom: 28px;
            ">
                End-to-end motor insurance management — from customer registration to policy issuance,
                powered by OJK-compliant premium calculation and rule-based underwriting.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Coverage Cards ────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
        letter-spacing:0.12em;text-transform:uppercase;color:#C8973A;margin-bottom:10px;">
        Coverage Options
    </div>
    <div style="font-family:'Inter',sans-serif;font-size:1.25rem;font-weight:700;
        color:#0A1F3D;margin-bottom:20px;">
        Choose Your Protection Plan
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2 = st.columns(2)
with c1:
    st.markdown(
        """
        <div style="
            background: #FFFFFF;
            border: 1px solid #DDE4EE;
            border-radius: 12px;
            padding: 28px 30px;
            box-shadow: 0 2px 16px rgba(10,31,61,0.07);
            border-top: 4px solid #0A1F3D;
            height: 100%;
            transition: box-shadow 0.2s ease;
        ">
            <div style="font-size: 2rem; margin-bottom: 12px;">🛡️</div>
            <div style="font-family:'Inter',sans-serif;font-size:1rem;font-weight:700;
                color:#0A1F3D;margin-bottom:10px;">Comprehensive Coverage</div>
            <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;line-height:1.7;">
                Our flagship protection plan covers own damage from accidents, partial losses,
                natural disasters, theft, and a range of additional risks. Ideal for new vehicles
                and high-value assets requiring complete peace of mind.
            </div>
            <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
                <span style="background:#EEF4FF;color:#1A3860;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Own Damage</span>
                <span style="background:#EEF4FF;color:#1A3860;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Theft</span>
                <span style="background:#EEF4FF;color:#1A3860;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Partial Loss</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        """
        <div style="
            background: #FFFFFF;
            border: 1px solid #DDE4EE;
            border-radius: 12px;
            padding: 28px 30px;
            box-shadow: 0 2px 16px rgba(10,31,61,0.07);
            border-top: 4px solid #C8973A;
            height: 100%;
        ">
            <div style="font-size: 2rem; margin-bottom: 12px;">🔒</div>
            <div style="font-family:'Inter',sans-serif;font-size:1rem;font-weight:700;
                color:#0A1F3D;margin-bottom:10px;">Total Loss Only (TLO)</div>
            <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;line-height:1.7;">
                A cost-effective solution designed for total loss or theft scenarios as defined by
                policy terms. Best suited for older vehicles or customers seeking essential
                protection at a competitive premium.
            </div>
            <div style="margin-top:16px;display:flex;gap:8px;flex-wrap:wrap;">
                <span style="background:#FEF9EE;color:#7A4E10;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Total Loss</span>
                <span style="background:#FEF9EE;color:#7A4E10;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Theft</span>
                <span style="background:#FEF9EE;color:#7A4E10;padding:3px 10px;border-radius:4px;
                    font-size:0.72rem;font-weight:600;font-family:'Inter',sans-serif;">Value-Driven</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)

# ── Value Propositions ────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
        letter-spacing:0.12em;text-transform:uppercase;color:#C8973A;margin-bottom:10px;">
        Why Etiqa
    </div>
    <div style="font-family:'Inter',sans-serif;font-size:1.25rem;font-weight:700;
        color:#0A1F3D;margin-bottom:20px;">
        Trusted by Thousands of Policyholders
    </div>
    """,
    unsafe_allow_html=True,
)

v1, v2, v3 = st.columns(3)
for col, icon, title, desc in [
    (v1, "⚡", "Fast Issuance", "Policy issued within minutes after underwriting approval — fully digital, no paperwork."),
    (v2, "📋", "OJK Compliant", "Premium rates calculated strictly following OJK (Otoritas Jasa Keuangan) regulatory guidelines."),
    (v3, "🔍", "Transparent Pricing", "Every premium component — base rate, riders, admin fee, and stamp duty — clearly itemised."),
]:
    with col:
        st.markdown(
            f"""
            <div style="
                background: #FFFFFF;
                border: 1px solid #DDE4EE;
                border-radius: 12px;
                padding: 24px 22px;
                box-shadow: 0 2px 12px rgba(10,31,61,0.06);
                text-align: center;
            ">
                <div style="font-size: 1.8rem; margin-bottom: 10px;">{icon}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:700;
                    color:#0A1F3D;margin-bottom:8px;">{title}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.82rem;color:#4B5E78;line-height:1.65;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-bottom:28px;'></div>", unsafe_allow_html=True)

# ── Workflow Diagram ──────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 0 10px 0;
        border-bottom: 2px solid #C8973A;
        margin-bottom: 20px;
    ">
        <span style="font-size:0.95rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.01em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            📊 &nbsp; End-to-End Process Flow
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.graphviz_chart(
    """
    digraph G {
        rankdir=LR;
        graph [bgcolor="transparent", pad="0.4"];
        node [shape=box, style="filled,rounded", fillcolor="#0A1F3D", fontcolor="#FFFFFF",
              fontname="Inter", fontsize=11, width=1.6, height=0.55, penwidth=0];
        edge [color="#C8973A", penwidth=1.8, arrowsize=0.8];

        A [label="Customer\nRegistration"];
        B [label="Vehicle\nInformation"];
        C [label="Coverage\nSelection"];
        D [label="Premium\nCalculation"];
        E [label="Application\nSubmission"];
        F [label="Document\nVerification"];
        G [label="Underwriting"];
        H [label="Approval /\nRejection"];
        I [label="Policy\nIssuance"];
        J [label="Analytics\nDashboard"];

        A -> B -> C -> D -> E -> F -> G -> H -> I -> J;
    }
    """
)

st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
_, cta_col, _ = st.columns([2, 1, 2])
with cta_col:
    if st.button("Start New Application", type="primary", use_container_width=True):
        try:
            st.switch_page("pages/2_New_Application.py")
        except Exception:
            st.info("Open the New Application page from the sidebar to begin.")

page_footer()
