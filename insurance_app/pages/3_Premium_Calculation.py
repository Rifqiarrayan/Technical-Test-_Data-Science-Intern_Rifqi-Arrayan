from __future__ import annotations

import pandas as pd
import streamlit as st

from database import Application, SessionLocal
from premium_engine import calculate_premium
from utils import apply_theme, ensure_initialized, format_currency, top_banner

st.set_page_config(page_title="Premium Calculation", page_icon="💰", layout="wide")
apply_theme()
ensure_initialized()

top_banner()
st.markdown("## Premium Calculator (OJK)")

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
    st.warning("No applications available.")
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

st.markdown("### Premium Summary")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Vehicle Price", format_currency(vehicle_price))
    st.metric("Coverage", app.coverage_type)
with c2:
    st.metric("Area", app.area)
    st.metric("Vehicle Category", str(premium["vehicle_category"]))
with c3:
    st.metric("OJK Rate", f"{premium['ojk_rate']:.2f}%")
    st.metric("Total Premium", format_currency(float(premium["total_premium"])))

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

if additional_coverages:
    st.info("Additional coverages selected: " + ", ".join(additional_coverages))
else:
    st.info("No additional coverages selected.")
