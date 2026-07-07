from __future__ import annotations

import streamlit as st

from dashboard import (
    chart_applications_by_area,
    chart_applications_by_coverage,
    chart_applications_by_status,
    chart_brand_distribution,
    chart_monthly_applications,
    chart_premium_distribution,
    chart_risk_distribution,
    get_kpis,
    load_dashboard_data,
)
from utils import apply_theme, ensure_initialized, format_currency, page_footer, top_banner

st.set_page_config(
    page_title="Dashboard | Etiqa Motor Insurance",
    page_icon="📊",
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
            Step 5 of 5 &nbsp;·&nbsp; Executive Analytics
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1.45rem;font-weight:700;color:#0A1F3D;">
            Business Analytics Dashboard
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;margin-top:4px;">
            Real-time portfolio overview — applications, premiums, risk distribution, and policy metrics.
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #DDE4EE;margin:16px 0 20px 0;">
    """,
    unsafe_allow_html=True,
)

data = load_dashboard_data()
merged = data["merged"]

# ── Filters ───────────────────────────────────────────────────────────────────
with st.expander("🔽  Filter Data", expanded=True):
    f1, f2 = st.columns(2)
    with f1:
        coverage_filter = st.multiselect(
            "Coverage Type",
            options=sorted(merged["coverage_type"].dropna().unique().tolist()),
            default=sorted(merged["coverage_type"].dropna().unique().tolist()),
        )
    with f2:
        area_filter = st.multiselect(
            "Area",
            options=sorted(merged["area"].dropna().unique().tolist()),
            default=sorted(merged["area"].dropna().unique().tolist()),
        )

filtered = merged[
    merged["coverage_type"].isin(coverage_filter)
    & merged["area"].isin(area_filter)
]

kpis = get_kpis(
    {
        **data,
        "applications": filtered,
        "premium_results": data["premium_results"][
            data["premium_results"]["application_id"].isin(filtered["id"].dropna().tolist())
        ],
        "vehicles": data["vehicles"][data["vehicles"]["id"].isin(filtered["vehicle_id"].dropna().tolist())],
    }
)

# ── KPI Row 1 ─────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1rem;">📈</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Portfolio Overview
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
kpi_defs_row1 = [
    (c1, "👥", "Total Customers", int(data["customers"].shape[0])),
    (c2, "📋", "Total Applications", int(kpis["total_applications"])),
    (c3, "✅", "Approved", int((filtered["status"] == "Approved").sum())),
    (c4, "❌", "Rejected", int((filtered["status"] == "Rejected").sum())),
]
for col, icon, label, value in kpi_defs_row1:
    with col:
        st.markdown(
            f"""
            <div class="etiqa-kpi-card">
                <div class="etiqa-kpi-icon">{icon}</div>
                <div class="etiqa-kpi-label">{label}</div>
                <div class="etiqa-kpi-value">{value:,}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-bottom:12px;'></div>", unsafe_allow_html=True)

c5, c6, c7 = st.columns(3)
kpi_defs_row2 = [
    (c5, "📄", "Issued Policies", int(data["policies"].shape[0]), False),
    (c6, "💰", "Average Premium", format_currency(kpis["avg_premium"]), True),
    (c7, "🚗", "Avg Vehicle Price", format_currency(kpis["avg_vehicle_price"]), True),
]
for col, icon, label, value, is_currency in kpi_defs_row2:
    with col:
        st.markdown(
            f"""
            <div class="etiqa-kpi-card" style="border-top:3px solid #C8973A;">
                <div class="etiqa-kpi-icon">{icon}</div>
                <div class="etiqa-kpi-label">{label}</div>
                <div class="etiqa-kpi-value" style="font-size:1.25rem;">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("<div style='margin-bottom:24px;'></div>", unsafe_allow_html=True)

# ── Charts Row 1 ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1rem;">📊</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Geographic & Coverage Analysis
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
r1c1, r1c2 = st.columns(2)
r1c1.plotly_chart(chart_applications_by_area(filtered), use_container_width=True)
r1c2.plotly_chart(chart_applications_by_coverage(filtered), use_container_width=True)

# ── Charts Row 2 ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1rem;">💼</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Status & Premium Analysis
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
r2c1, r2c2 = st.columns(2)
r2c1.plotly_chart(chart_applications_by_status(filtered), use_container_width=True)
r2c2.plotly_chart(chart_premium_distribution(filtered.dropna(subset=["total_premium"])), use_container_width=True)

# ── Charts Row 3 ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1rem;">🚗</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Vehicle Brand & Monthly Trend
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
r3c1, r3c2 = st.columns(2)
r3c1.plotly_chart(chart_brand_distribution(filtered), use_container_width=True)
r3c2.plotly_chart(chart_monthly_applications(filtered.dropna(subset=["month"])), use_container_width=True)

# ── Risk Distribution ─────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;">
        <span style="font-size:1rem;">⚠️</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Risk Portfolio Distribution
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.plotly_chart(chart_risk_distribution(filtered.dropna(subset=["risk_level"])), use_container_width=True)

# ── Data Preview ──────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 6px 0;
        border-bottom:2px solid #C8973A;margin-bottom:16px;margin-top:16px;">
        <span style="font-size:1rem;">🗂️</span>
        <span style="font-size:0.85rem;font-weight:700;color:#0A1F3D;
            letter-spacing:0.04em;text-transform:uppercase;font-family:'Inter',sans-serif;">
            Data Preview
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.dataframe(
    filtered[
        [
            "application_id",
            "coverage_type",
            "area",
            "status",
            "brand",
            "vehicle_price",
            "total_premium",
            "risk_level",
        ]
    ].sort_values("application_id"),
    use_container_width=True,
    hide_index=True,
)

page_footer()
