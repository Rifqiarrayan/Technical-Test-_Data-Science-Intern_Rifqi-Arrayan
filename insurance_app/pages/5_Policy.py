from __future__ import annotations

import streamlit as st

from database import Application, Policy, SessionLocal
from policy_generator import generate_policy_number, policy_dates, generate_policy_pdf
from utils import apply_theme, ensure_initialized, format_currency, status_badge, top_banner

st.set_page_config(page_title="Policy", page_icon="📄", layout="wide")
apply_theme()
ensure_initialized()

top_banner()
st.markdown("## Policy Issuance")

with SessionLocal() as session:
    apps = session.query(Application).filter(Application.status.in_(["Approved", "Policy Issued"])).all()

if not apps:
    st.warning("No approved applications available yet.")
    st.stop()

selected_id = st.selectbox("Select Approved Application", [item.application_id for item in apps])

with SessionLocal() as session:
    app = session.query(Application).filter(Application.application_id == selected_id).first()
    if app is None:
        st.error("Application not found.")
        st.stop()

    premium = app.premium_result.total_premium if app.premium_result else 0.0

    if app.policy:
        policy = app.policy
    else:
        policy_info = policy_dates()
        policy = Policy(
            application_id=app.id,
            policy_number=generate_policy_number(),
            issue_date=policy_info["issue_date"],
            effective_date=policy_info["effective_date"],
            expiry_date=policy_info["expiry_date"],
            premium_amount=float(premium),
            status="Issued",
            generated_pdf=False,
        )
        session.add(policy)
        app.status = "Policy Issued"
        session.commit()
        session.refresh(policy)

    st.markdown(status_badge("Policy Issued"), unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"Policy Number: **{policy.policy_number}**")
        st.markdown(f"Issue Date: **{policy.issue_date}**")
        st.markdown(f"Effective Date: **{policy.effective_date}**")
        st.markdown(f"Expiry Date: **{policy.expiry_date}**")
    with c2:
        st.markdown(f"Customer: **{app.customer.full_name}**")
        st.markdown(f"Vehicle: **{app.vehicle.brand} {app.vehicle.model} ({app.vehicle.year})**")
        st.markdown(f"Coverage: **{app.coverage_type}**")
        st.markdown(f"Premium: **{format_currency(float(policy.premium_amount))}**")

    pdf_data = generate_policy_pdf(
        {
            "policy_number": policy.policy_number,
            "issue_date": policy.issue_date,
            "effective_date": policy.effective_date,
            "expiry_date": policy.expiry_date,
            "application_id": app.application_id,
            "customer_name": app.customer.full_name,
            "nik": app.customer.nik,
            "brand": app.vehicle.brand,
            "model": app.vehicle.model,
            "year": app.vehicle.year,
            "plate_number": app.vehicle.plate_number,
            "coverage_type": app.coverage_type,
            "total_premium": float(policy.premium_amount),
            "status": policy.status,
        }
    )

    policy.generated_pdf = True
    session.commit()

    st.download_button(
        label="Download Policy PDF",
        data=pdf_data,
        file_name=f"{policy.policy_number}.pdf",
        mime="application/pdf",
        type="primary",
    )
