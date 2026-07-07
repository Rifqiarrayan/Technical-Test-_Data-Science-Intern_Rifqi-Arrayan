from __future__ import annotations

from typing import Iterable

import pandas as pd

from config import ADMIN_FEE, OJK_RATES_PATH, STAMP_DUTY


def determine_vehicle_category(vehicle_price: float) -> str:
    if vehicle_price <= 125_000_000:
        return "Cat 1"
    if vehicle_price <= 200_000_000:
        return "Cat 2"
    if vehicle_price <= 400_000_000:
        return "Cat 3"
    if vehicle_price <= 800_000_000:
        return "Cat 4"
    return "Cat 5"


def lookup_ojk_rate(coverage_type: str, area: str, vehicle_price: float) -> float:
    category = determine_vehicle_category(vehicle_price)
    rates = pd.read_csv(OJK_RATES_PATH)
    row = rates[
        (rates["coverage"] == coverage_type)
        & (rates["area"] == area)
        & (rates["vehicle_category"] == category)
        & (rates["min_vehicle_value"] <= vehicle_price)
        & (rates["max_vehicle_value"] >= vehicle_price)
    ]

    if row.empty:
        fallback = rates[
            (rates["coverage"] == coverage_type)
            & (rates["area"] == area)
            & (rates["vehicle_category"] == category)
        ]
        if fallback.empty:
            raise ValueError("Unable to find matching OJK rate.")
        return float(fallback.iloc[0]["premium_rate"])

    return float(row.iloc[0]["premium_rate"])


def calculate_additional_coverage_fee(vehicle_price: float, additional_coverages: Iterable[str]) -> float:
    fee_map = {
        "Flood": 0.0010,
        "Earthquake": 0.0008,
        "Riot": 0.0005,
        "Third Party Liability": 0.0012,
        "Personal Accident": 0.0006,
    }
    return round(sum(vehicle_price * fee_map.get(item, 0.0) for item in additional_coverages), 2)


def calculate_premium(
    vehicle_price: float,
    coverage_type: str,
    area: str,
    additional_coverages: Iterable[str],
) -> dict[str, float | str]:
    rate = lookup_ojk_rate(coverage_type, area, vehicle_price)
    basic_premium = round(vehicle_price * rate / 100, 2)
    additional_fee = calculate_additional_coverage_fee(vehicle_price, additional_coverages)
    total = round(basic_premium + additional_fee + ADMIN_FEE + STAMP_DUTY, 2)

    return {
        "vehicle_category": determine_vehicle_category(vehicle_price),
        "ojk_rate": rate,
        "basic_premium": basic_premium,
        "additional_coverage_fee": additional_fee,
        "admin_fee": float(ADMIN_FEE),
        "stamp_duty": float(STAMP_DUTY),
        "total_premium": total,
    }
