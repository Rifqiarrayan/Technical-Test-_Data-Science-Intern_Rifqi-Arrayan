from __future__ import annotations

import streamlit as st

from database import Application, SessionLocal, UnderwritingResult
from underwriting import evaluate_underwriting
from utils import apply_theme, status_badge, top_banner, ensure_initialized

st.set_page_config(page_title="Underwriting", page_icon="🧾", layout="wide")
apply_theme()
ensure_initialized()

top_banner()
st.markdown("## Underwriting (Rule-Based)")

with SessionLocal() as session:
    apps = (
        session.query(Application)
        .filter(Application.status.in_(["Submitted", "Document Verified", "Underwriting", "Approved", "Rejected"]))
        .all()
    )

if not apps:
    st.warning("No applications available for underwriting review.")
    st.stop()

selected_map = {app.application_id: app for app in apps}
selected_id = st.selectbox("Select Application", list(selected_map.keys()))

with SessionLocal() as session:
    app = session.query(Application).filter(Application.application_id == selected_id).first()
    if app is None:
        st.error("Application not found.")
        st.stop()

    c1, c2, c3 = st.columns(3)
    with c1:
        st.write(f"Customer: **{app.customer.full_name}**")
        st.write(f"Vehicle: **{app.vehicle.brand} {app.vehicle.model}**")
    with c2:
        st.write(f"Coverage: **{app.coverage_type}**")
        st.write(f"Usage: **{app.vehicle.vehicle_usage}**")
    with c3:
        st.write("Current Status")
        st.markdown(status_badge(app.status), unsafe_allow_html=True)

    if st.button("Run Underwriting Decision", type="primary"):
        result = evaluate_underwriting(
            vehicle_year=app.vehicle.year,
            vehicle_price=float(app.vehicle.vehicle_price),
            coverage_type=app.coverage_type,
            vehicle_usage=app.vehicle.vehicle_usage,
        )

        app.status = "Underwriting"
        existing = session.query(UnderwritingResult).filter(UnderwritingResult.application_id == app.id).first()
        if existing:
            existing.vehicle_age = int(result["vehicle_age"])
            existing.risk_level = str(result["risk_level"])
            existing.decision = str(result["decision"])
            existing.notes = str(result["notes"])
        else:
            session.add(
                UnderwritingResult(
                    application_id=app.id,
                    vehicle_age=int(result["vehicle_age"]),
                    risk_level=str(result["risk_level"]),
                    decision=str(result["decision"]),
                    notes=str(result["notes"]),
                )
            )

        if result["decision"] == "Approved":
            app.status = "Approved"
        elif result["decision"] == "Rejected":
            app.status = "Rejected"
        else:
            app.status = "Underwriting"

        session.commit()

        st.success("Underwriting process completed.")
        st.markdown(f"Risk Level: **{result['risk_level']}**")
        st.markdown(f"Decision: **{result['decision']}**")
        st.info(str(result["notes"]))
        st.markdown(status_badge(app.status), unsafe_allow_html=True)

st.markdown("### Status Flow")
st.markdown("Submitted → Document Verified → Underwriting → Approved/Rejected → Policy Issued")
