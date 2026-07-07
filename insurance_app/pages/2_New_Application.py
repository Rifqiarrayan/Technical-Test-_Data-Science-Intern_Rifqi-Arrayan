from __future__ import annotations

from datetime import date

import streamlit as st

from config import ADDITIONAL_COVERAGES, AREAS, COVERAGE_TYPES, INDONESIAN_BRANDS
from database import create_application_with_related_records
from utils import apply_theme, ensure_initialized, page_footer, status_badge, top_banner

st.set_page_config(page_title="New Application | Etiqa Motor Insurance", page_icon="📝", layout="wide")
apply_theme()
ensure_initialized()

top_banner()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="margin-bottom:8px;">
        <div style="font-family:'Inter',sans-serif;font-size:0.7rem;font-weight:700;
            letter-spacing:0.12em;text-transform:uppercase;color:#C8973A;margin-bottom:6px;">
            Step 1 of 5 &nbsp;·&nbsp; Application Form
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:1.45rem;font-weight:700;color:#0A1F3D;">
            New Insurance Application
        </div>
        <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#4B5E78;margin-top:4px;">
            Please complete all sections below accurately. Fields marked are required.
        </div>
    </div>
    <hr style="border:none;border-top:1px solid #DDE4EE;margin:16px 0 24px 0;">
    """,
    unsafe_allow_html=True,
)

with st.form("new_application_form"):

    # ── Section 1: Customer Information ──────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:20px;">
            <span style="font-size:1.1rem;">👤</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Customer Information
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name = st.text_input("Full Name")
        nik = st.text_input("NIK", max_chars=16)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        birth_date = st.date_input(
            "Birth Date",
            value=date(1995, 1, 1),
            min_value=date(1950, 1, 1),
            max_value=date.today(),
        )
        phone = st.text_input("Phone")
        email = st.text_input("Email")
    with c3:
        address = st.text_area("Address", height=105)

    st.markdown("<div style='margin:8px 0;'></div>", unsafe_allow_html=True)

    # ── Section 2: Vehicle Information ───────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:20px;">
            <span style="font-size:1.1rem;">🚗</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Vehicle Information
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    v1, v2, v3 = st.columns(3)
    with v1:
        brand = st.selectbox("Brand", INDONESIAN_BRANDS)
        model = st.text_input("Model")
        year = st.number_input(
            "Year",
            min_value=1995,
            max_value=date.today().year,
            value=2020,
        )
    with v2:
        plate_number = st.text_input("Plate Number")
        vehicle_type = st.selectbox(
            "Vehicle Type",
            ["SUV", "Sedan", "Hatchback", "MPV", "EV", "Pickup"],
        )
        vehicle_usage = st.selectbox("Vehicle Usage", ["Private", "Commercial"])
    with v3:
        vehicle_price = st.number_input(
            "Vehicle Price (IDR)",
            min_value=50_000_000,
            max_value=2_000_000_000,
            value=250_000_000,
            step=5_000_000,
        )
        area = st.selectbox("Area", AREAS)

    st.markdown("<div style='margin:8px 0;'></div>", unsafe_allow_html=True)

    # ── Section 3: Coverage Selection ────────────────────────────────────────
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;padding:10px 0 8px 0;
            border-bottom:2px solid #C8973A;margin-bottom:20px;">
            <span style="font-size:1.1rem;">🛡️</span>
            <span style="font-size:0.9rem;font-weight:700;color:#0A1F3D;
                letter-spacing:0.03em;text-transform:uppercase;font-family:'Inter',sans-serif;">
                Coverage Selection
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    coverage_type = st.radio("Coverage Type", COVERAGE_TYPES, horizontal=True)
    additional_coverages = st.multiselect(
        "Additional Coverage (Riders)",
        ADDITIONAL_COVERAGES,
    )

    st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)
    submitted = st.form_submit_button("Submit Application", type="primary")

# ── Result ────────────────────────────────────────────────────────────────────
if submitted:
    required = [full_name, nik, phone, email, address, model, plate_number]
    if any(not str(item).strip() for item in required):
        st.error("⚠️  Please complete all required fields before submitting.")
    else:
        try:
            application_id = create_application_with_related_records(
                {
                    "full_name": full_name,
                    "nik": nik,
                    "gender": gender,
                    "birth_date": birth_date,
                    "phone": phone,
                    "email": email,
                    "address": address,
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "plate_number": plate_number.upper(),
                    "vehicle_type": vehicle_type,
                    "vehicle_usage": vehicle_usage,
                    "vehicle_price": float(vehicle_price),
                    "area": area,
                    "coverage_type": coverage_type,
                    "additional_coverages": additional_coverages,
                }
            )
            st.markdown(
                f"""
                <div style="
                    background:#ECFDF5;
                    border:1px solid #6EE7B7;
                    border-left:4px solid #0D7C4E;
                    border-radius:8px;
                    padding:20px 24px;
                    margin-top:16px;
                ">
                    <div style="font-family:'Inter',sans-serif;font-size:0.95rem;
                        font-weight:700;color:#064E3B;margin-bottom:8px;">
                        ✅ Application Submitted Successfully
                    </div>
                    <div style="font-family:'Inter',sans-serif;font-size:0.875rem;color:#065F46;">
                        Your application has been recorded. Proceed to
                        <strong>Premium Calculation</strong> to view your premium breakdown.
                    </div>
                    <div style="margin-top:12px;font-family:'Inter',sans-serif;
                        font-size:0.8rem;color:#047857;">
                        Application ID:
                        <span style="font-weight:700;background:#D1FAE5;padding:2px 10px;
                            border-radius:4px;color:#065F46;">{application_id}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(status_badge("Submitted"), unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"Failed to submit application: {exc}")

page_footer()
