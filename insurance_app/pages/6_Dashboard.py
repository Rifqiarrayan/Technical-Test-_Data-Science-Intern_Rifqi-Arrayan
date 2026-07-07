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
from utils import apply_theme, ensure_initialized, format_currency, top_banner

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")
apply_theme()
ensure_initialized()

top_banner()
st.markdown("## Business Analytics Dashboard")

data = load_dashboard_data()
merged = data["merged"]

coverage_filter = st.multiselect(
    "Coverage Filter",
    options=sorted(merged["coverage_type"].dropna().unique().tolist()),
    default=sorted(merged["coverage_type"].dropna().unique().tolist()),
)
area_filter = st.multiselect(
    "Area Filter",
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

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Customers", int(data["customers"].shape[0]))
c2.metric("Total Applications", int(kpis["total_applications"]))
c3.metric("Approved Applications", int((filtered["status"] == "Approved").sum()))
c4.metric("Rejected Applications", int((filtered["status"] == "Rejected").sum()))

c5, c6, c7 = st.columns(3)
c5.metric("Issued Policies", int(data["policies"].shape[0]))
c6.metric("Average Premium", format_currency(kpis["avg_premium"]))
c7.metric("Average Vehicle Price", format_currency(kpis["avg_vehicle_price"]))

r1c1, r1c2 = st.columns(2)
r1c1.plotly_chart(chart_applications_by_area(filtered), use_container_width=True)
r1c2.plotly_chart(chart_applications_by_coverage(filtered), use_container_width=True)

r2c1, r2c2 = st.columns(2)
r2c1.plotly_chart(chart_applications_by_status(filtered), use_container_width=True)
r2c2.plotly_chart(chart_premium_distribution(filtered.dropna(subset=["total_premium"])), use_container_width=True)

r3c1, r3c2 = st.columns(2)
r3c1.plotly_chart(chart_brand_distribution(filtered), use_container_width=True)
r3c2.plotly_chart(chart_monthly_applications(filtered.dropna(subset=["month"])), use_container_width=True)

st.plotly_chart(chart_risk_distribution(filtered.dropna(subset=["risk_level"])), use_container_width=True)

st.markdown("### Data Preview")
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
