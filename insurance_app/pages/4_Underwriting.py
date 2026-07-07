from __future__ import annotations

import streamlit as st

from database import Application, SessionLocal, UnderwritingResult
from underwriting import evaluate_underwriting
from utils import apply_theme, ensure_initialized, page_footer, status_badge, top_banner

st.set_page_config(
    page_title="Underwriting | Etiqa Motor Insurance",
    page_icon="🧾",
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
            Step 3 of 5 &nbsp;·&nbsp; Risk Assessment
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1.45rem;font-weight:700;color:#0A1F3D;">
            Underwriting (Rule-Based)
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;margin-top:4px;">
            Automated risk assessment based on vehicle age, price, coverage type, and usage classification.
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #DDE4EE;margin:16px 0 24px 0;">
    """,
    unsafe_allow_html=True,
)

with SessionLocal() as session:
    apps = (
        session.query(Application)
        .filter(
            Application.status.in_(
                ["Submitted", "Document Verified", "Underwriting", "Approved", "Rejected"]
            )
        )
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

    # ── Application summary panel ─────────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:16px;">
            <span style="font-size:1.1rem;">📁</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Application Summary
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f"""
            <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:8px;padding:14px 16px;">
                <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:6px;">Customer</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.95rem;font-weight:700;color:#0A1F3D;">{app.customer.full_name}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:#4B5E78;margin-top:4px;">Vehicle: {app.vehicle.brand} {app.vehicle.model}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
            <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:8px;padding:14px 16px;">
                <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:6px;">Coverage & Usage</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.95rem;font-weight:700;color:#0A1F3D;">{app.coverage_type}</div>
                <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:#4B5E78;margin-top:4px;">Usage: {app.vehicle.vehicle_usage}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div style="background:#F7F9FC;border:1px solid #DDE4EE;border-radius:8px;padding:14px 16px;">
                <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:6px;">Current Status</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(status_badge(app.status), unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin:20px 0;'></div>", unsafe_allow_html=True)

    # ── Action button ─────────────────────────────────────────────────────────
    if st.button("▶  Run Underwriting Decision", type="primary"):
        result = evaluate_underwriting(
            vehicle_year=app.vehicle.year,
            vehicle_price=float(app.vehicle.vehicle_price),
            coverage_type=app.coverage_type,
            vehicle_usage=app.vehicle.vehicle_usage,
        )

        app.status = "Underwriting"
        existing = (
            session.query(UnderwritingResult)
            .filter(UnderwritingResult.application_id == app.id)
            .first()
        )
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

        # Determine visual accent per decision
        decision = result["decision"]
        risk_level = result["risk_level"]

        if decision == "Approved":
            border_color = "#0D7C4E"
            bg_color = "#ECFDF5"
            icon = "✅"
            text_color = "#064E3B"
            risk_colors = {"Low": "#0D7C4E", "Medium": "#D97706", "High": "#C0392B"}
        elif decision == "Rejected":
            border_color = "#C0392B"
            bg_color = "#FEF2F2"
            icon = "❌"
            text_color = "#7F1D1D"
            risk_colors = {"Low": "#0D7C4E", "Medium": "#D97706", "High": "#C0392B"}
        else:
            border_color = "#D97706"
            bg_color = "#FFFBEB"
            icon = "🔍"
            text_color = "#78350F"
            risk_colors = {"Low": "#0D7C4E", "Medium": "#D97706", "High": "#C0392B"}

        risk_color = risk_colors.get(risk_level, "#4B5E78")

        st.markdown(
            f"""
            <div style="
                background:{bg_color};
                border:1px solid {border_color};
                border-left:5px solid {border_color};
                border-radius:10px;
                padding:24px 28px;
                margin-top:20px;
            ">
                <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
                    letter-spacing:0.1em;text-transform:uppercase;color:#4B5E78;margin-bottom:12px;">
                    Underwriting Result
                </div>
                <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
                    <span style="font-size:1.8rem;">{icon}</span>
                    <div>
                        <div style="font-family:'Inter',sans-serif;font-size:1.2rem;
                            font-weight:800;color:{border_color};">{decision}</div>
                        <div style="font-family:'Inter',sans-serif;font-size:0.8rem;color:#4B5E78;margin-top:2px;">
                            Vehicle Age: <strong>{result['vehicle_age']} year(s)</strong>
                        </div>
                    </div>
                </div>
                <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px;">
                    <div style="background:#FFFFFF;border:1px solid #DDE4EE;border-radius:8px;
                        padding:10px 18px;min-width:140px;">
                        <div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;
                            letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:4px;">Risk Level</div>
                        <div style="font-family:'Inter',sans-serif;font-size:1rem;
                            font-weight:700;color:{risk_color};">{risk_level}</div>
                    </div>
                    <div style="background:#FFFFFF;border:1px solid #DDE4EE;border-radius:8px;
                        padding:10px 18px;flex:1;">
                        <div style="font-family:'Inter',sans-serif;font-size:0.68rem;font-weight:700;
                            letter-spacing:0.08em;text-transform:uppercase;color:#4B5E78;margin-bottom:4px;">Underwriting Notes</div>
                        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:{text_color};">{result["notes"]}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(status_badge(app.status), unsafe_allow_html=True)

# ── Status Flow ───────────────────────────────────────────────────────────────
steps = [
    "Submitted",
    "Document Verified",
    "Underwriting",
    "Approved / Rejected",
    "Policy Issued",
]

step_items = ""
for i, step in enumerate(steps):
    arrow = "<span style='color:#C8973A;font-size:1.1rem;padding:0 8px;'>→</span>" if i < len(steps) - 1 else ""
    step_items += (
        f"<span style='background:#EEF4FF;border:1px solid #C8D8F0;border-radius:6px;"
        f"padding:6px 14px;font-family:Inter,sans-serif;font-size:0.78rem;"
        f"font-weight:600;color:#1A3860;white-space:nowrap;'>{step}</span>"
        + arrow
    )

st.markdown(
    f"""
    <div style="margin-top:28px;">
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:16px;">
            <span style="font-size:1.1rem;">🔄</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Application Status Flow
            </span>
        </div>
        <div style="display:flex;align-items:center;flex-wrap:wrap;gap:4px;margin-bottom:8px;">
            {step_items}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

page_footer()
