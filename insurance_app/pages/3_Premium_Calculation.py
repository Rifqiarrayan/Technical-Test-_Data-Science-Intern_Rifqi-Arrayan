from __future__ import annotations

import pandas as pd
import streamlit as st

from database import Application, SessionLocal
from premium_engine import calculate_premium
from utils import apply_theme, ensure_initialized, format_currency, page_footer, top_banner

st.set_page_config(
    page_title="Premium Calculation | Etiqa Motor Insurance",
    page_icon="💰",
    layout="wide",
)
apply_theme()
ensure_initialized()

top_banner()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:8px;">
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
            letter-spacing:0.12em;text-transform:uppercase;color:#C8973A;margin-bottom:6px;">
            Step 2 of 5 &nbsp;·&nbsp; Premium Calculation (OJK)
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1.45rem;font-weight:700;color:#0A1F3D;">
            Premium Calculator
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;margin-top:4px;">
            Rates are calculated in accordance with OJK (Otoritas Jasa Keuangan) regulatory guidelines.
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #DDE4EE;margin:16px 0 24px 0;">
    """,
    unsafe_allow_html=True,
)

with SessionLocal() as session:
    rows = (
        session.query(
            Application.application_id,
            Application.coverage_type,
            Application.area,
        )
        .all()
    )

if not rows:
    st.warning("No applications available. Please submit an application first.")
    st.stop()

app_options = {row.application_id: row for row in rows}
selected_app_id = st.selectbox("Select Application ID", list(app_options.keys()))

with SessionLocal() as session:
    app = session.query(Application).filter(Application.application_id == selected_app_id).first()
    if app is None:
        st.error("Application not found.")
        st.stop()

    vehicle_price = float(app.vehicle.vehicle_price)
    additional_coverages = app.additional_coverages or []
    premium = calculate_premium(
        vehicle_price=vehicle_price,
        coverage_type=app.coverage_type,
        area=app.area,
        additional_coverages=additional_coverages,
    )

st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

# ── Summary KPI cards ─────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
        border-bottom:2px solid #C8973A;margin-bottom:20px;">
        <span style="font-size:1.1rem;">📊</span>
        <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Premium Summary
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Vehicle Price", format_currency(vehicle_price))
    st.metric("Coverage Type", app.coverage_type)
with c2:
    st.metric("Area", app.area)
    st.metric("Vehicle Category", str(premium["vehicle_category"]))
with c3:
    st.metric("OJK Rate", f"{premium['ojk_rate']:.2f}%")
    st.metric("Total Premium", format_currency(float(premium["total_premium"])))

# ── Total Premium highlight ───────────────────────────────────────────────────
st.markdown(
    f"""
    <div style="
        background: linear-gradient(135deg, #0A1F3D 0%, #1A3860 100%);
        border-radius: 12px;
        padding: 24px 32px;
        margin: 24px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(10,31,61,0.18);
    ">
        <div>
            <div style="font-family:'Inter',sans-serif;font-size:0.72rem;font-weight:700;
                letter-spacing:0.1em;text-transform:uppercase;color:#A8BEDB;margin-bottom:6px;">
                Annual Premium Payable
            </div>
            <div style="font-family:'Inter',sans-serif;font-size:0.85rem;color:#CBD8E8;">
                Coverage: <strong style="color:#FFFFFF;">{app.coverage_type}</strong>
                &nbsp;·&nbsp; Area: <strong style="color:#FFFFFF;">{app.area}</strong>
            </div>
        </div>
        <div style="text-align:right;">
            <div style="font-family:'Inter',sans-serif;font-size:2rem;font-weight:800;
                color:#C8973A;line-height:1.1;">
                {format_currency(float(premium["total_premium"]))}
            </div>
            <div style="font-family:'Inter',sans-serif;font-size:0.75rem;color:#A8BEDB;margin-top:4px;">
                OJK Rate: {premium['ojk_rate']:.2f}%
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Breakdown table ───────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1.1rem;">📋</span>
        <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Premium Component Breakdown
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

summary_df = pd.DataFrame(
    {
        "Component": [
            "Basic Premium",
            "Additional Coverage Fee",
            "Administration Fee",
            "Stamp Duty",
            "Total Premium",
        ],
        "Amount": [
            premium["basic_premium"],
            premium["additional_coverage_fee"],
            premium["admin_fee"],
            premium["stamp_duty"],
            premium["total_premium"],
        ],
    }
)
summary_df["Amount"] = summary_df["Amount"].map(lambda x: format_currency(float(x)))
st.dataframe(summary_df, use_container_width=True, hide_index=True)

# ── Additional coverages ──────────────────────────────────────────────────────
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
if additional_coverages:
    pills = "".join(
        f"<span style='background:#EEF4FF;color:#1A3860;padding:4px 12px;border-radius:4px;"
        f"font-size:0.78rem;font-weight:600;font-family:Inter,sans-serif;"
        f"margin-right:6px;margin-bottom:6px;display:inline-block;'>{cov}</span>"
        for cov in additional_coverages
    )
    st.markdown(
        f"""
        <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:10px;
            padding:16px 20px;margin-bottom:12px;">
            <div style="font-family:'Inter',sans-serif;font-size:0.75rem;font-weight:700;
                letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:10px;">
                Additional Riders Selected
            </div>
            <div>{pills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="background:#FFFBEB;border:1px solid #FDE68A;border-left:4px solid #D97706;
            border-radius:8px;padding:14px 18px;font-family:'Inter',sans-serif;
            font-size:0.875rem;color:#78350F;">
            No additional riders selected for this application.
        </div>
        """,
        unsafe_allow_html=True,
    )

page_footer()
