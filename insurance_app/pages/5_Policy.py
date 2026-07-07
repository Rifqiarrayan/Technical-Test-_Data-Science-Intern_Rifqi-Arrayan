from __future__ import annotations

import streamlit as st

from database import Application, Policy, SessionLocal
from policy_generator import generate_policy_number, policy_dates, generate_policy_pdf
from utils import apply_theme, ensure_initialized, format_currency, page_footer, status_badge, top_banner

st.set_page_config(
    page_title="Policy Issuance | Etiqa Motor Insurance",
    page_icon="📄",
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
            Step 4 of 5 &nbsp;·&nbsp; Policy Issuance
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1.45rem;font-weight:700;color:#0A1F3D;">
            Policy Document
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;margin-top:4px;">
            Official policy certificate is generated upon approval. Download the PDF for your records.
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #DDE4EE;margin:16px 0 24px 0;">
    """,
    unsafe_allow_html=True,
)

with SessionLocal() as session:
    apps = session.query(Application).filter(Application.status.in_(["Approved", "Policy Issued"])).all()

if not apps:
    st.warning("No approved applications available yet. Complete the underwriting step first.")
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

    # ── Policy Issued badge ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="
            background: linear-gradient(135deg, #0D7C4E 0%, #065F46 100%);
            border-radius: 10px;
            padding: 14px 24px;
            margin-bottom: 24px;
            display: inline-flex;
            align-items: center;
            gap: 12px;
            box-shadow: 0 3px 12px rgba(13,124,78,0.25);
        ">
            <span style="font-size:1.4rem;">✅</span>
            <div>
                <div style="font-family:'Inter',sans-serif;font-size:0.65rem;font-weight:700;
                    letter-spacing:0.12em;text-transform:uppercase;color:#6EE7B7;margin-bottom:2px;">
                    Policy Status
                </div>
                <div style="font-family:'Inter',sans-serif;font-size:1rem;font-weight:800;
                    color:#FFFFFF;letter-spacing:0.02em;">
                    POLICY ISSUED
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Policy document card ──────────────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:20px;">
            <span style="font-size:1.1rem;">📄</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Policy Details
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:10px;padding:20px 24px;">
                <div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;
                    letter-spacing:0.1em;text-transform:uppercase;color:#4B5E78;margin-bottom:14px;">
                    Policy Information
                </div>
                <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
                    <tr>
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;width:45%;">Policy Number</td>
                        <td style="font-size:0.875rem;font-weight:700;color:#0A1F3D;padding:7px 0;">
                            {policy.policy_number}
                        </td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Issue Date</td>
                        <td style="font-size:0.875rem;font-weight:600;color:#0A1F3D;padding:7px 0;">{policy.issue_date}</td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Effective Date</td>
                        <td style="font-size:0.875rem;font-weight:600;color:#0A1F3D;padding:7px 0;">{policy.effective_date}</td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Expiry Date</td>
                        <td style="font-size:0.875rem;font-weight:600;color:#C0392B;padding:7px 0;">{policy.expiry_date}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:10px;padding:20px 24px;">
                <div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;
                    letter-spacing:0.1em;text-transform:uppercase;color:#4B5E78;margin-bottom:14px;">
                    Insured Details
                </div>
                <table style="width:100%;border-collapse:collapse;font-family:'Inter',sans-serif;">
                    <tr>
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;width:45%;">Customer</td>
                        <td style="font-size:0.875rem;font-weight:700;color:#0A1F3D;padding:7px 0;">{app.customer.full_name}</td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Vehicle</td>
                        <td style="font-size:0.875rem;font-weight:600;color:#0A1F3D;padding:7px 0;">
                            {app.vehicle.brand} {app.vehicle.model} ({app.vehicle.year})
                        </td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Coverage</td>
                        <td style="font-size:0.875rem;font-weight:600;color:#0A1F3D;padding:7px 0;">{app.coverage_type}</td>
                    </tr>
                    <tr style="border-top:1px solid #EDF1F7;">
                        <td style="font-size:0.78rem;color:#4B5E78;padding:7px 0;">Annual Premium</td>
                        <td style="font-size:0.95rem;font-weight:800;color:#C8973A;padding:7px 0;">
                            {format_currency(float(policy.premium_amount))}
                        </td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top:24px;'></div>", unsafe_allow_html=True)

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

    # ── Download CTA ──────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:10px;
            padding:20px 24px;display:flex;align-items:center;gap:16px;margin-bottom:8px;">
            <span style="font-size:2rem;">📥</span>
            <div>
                <div style="font-family:'Inter',sans-serif;font-size:0.9rem;font-weight:700;
                    color:#0A1F3D;margin-bottom:4px;">Download Your Policy Certificate</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:#4B5E78;">
                    Official PDF document for your records. Keep it safe as proof of coverage.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.download_button(
        label="📄  Download Policy PDF",
        data=pdf_data,
        file_name=f"{policy.policy_number}.pdf",
        mime="application/pdf",
        type="primary",
    )

page_footer()
