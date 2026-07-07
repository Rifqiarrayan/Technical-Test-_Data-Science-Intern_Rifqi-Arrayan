from __future__ import annotations

from datetime import date

import streamlit as st

from config import ADDITIONAL_COVERAGES, AREAS, COVERAGE_TYPES, INDONESIAN_BRANDS
from database import create_application_with_related_records
from utils import apply_theme, ensure_initialized, status_badge, top_banner

st.set_page_config(page_title="New Application", page_icon="📝", layout="wide")
apply_theme()
ensure_initialized()

top_banner()
st.markdown("## New Insurance Application")

with st.form("new_application_form"):
    st.markdown("### Customer Information")
    c1, c2, c3 = st.columns(3)
    with c1:
        full_name = st.text_input("Full Name")
        nik = st.text_input("NIK", max_chars=16)
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        birth_date = st.date_input("Birth Date", value=date(1995, 1, 1), min_value=date(1950, 1, 1), max_value=date.today())
        phone = st.text_input("Phone")
        email = st.text_input("Email")
    with c3:
        address = st.text_area("Address", height=105)

    st.markdown("### Vehicle Information")
    v1, v2, v3 = st.columns(3)
    with v1:
        brand = st.selectbox("Brand", INDONESIAN_BRANDS)
        model = st.text_input("Model")
        year = st.number_input("Year", min_value=1995, max_value=date.today().year, value=2020)
    with v2:
        plate_number = st.text_input("Plate Number")
        vehicle_type = st.selectbox("Vehicle Type", ["SUV", "Sedan", "Hatchback", "MPV", "EV", "Pickup"])
        vehicle_usage = st.selectbox("Vehicle Usage", ["Private", "Commercial"])
    with v3:
        vehicle_price = st.number_input("Vehicle Price (IDR)", min_value=50_000_000, max_value=2_000_000_000, value=250_000_000, step=5_000_000)
        area = st.selectbox("Area", AREAS)

    st.markdown("### Coverage Selection")
    coverage_type = st.radio("Coverage", COVERAGE_TYPES, horizontal=True)
    additional_coverages = st.multiselect("Additional Coverage", ADDITIONAL_COVERAGES)

    submitted = st.form_submit_button("Submit Application", type="primary")

if submitted:
    required = [full_name, nik, phone, email, address, model, plate_number]
    if any(not str(item).strip() for item in required):
        st.error("Please complete all required fields.")
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
            st.success("Application submitted successfully.")
            st.markdown(f"Application ID: **{application_id}**")
            st.markdown(status_badge("Submitted"), unsafe_allow_html=True)
        except Exception as exc:
            st.error(f"Failed to submit application: {exc}")
