from __future__ import annotations

from datetime import datetime


def evaluate_underwriting(
    vehicle_year: int,
    vehicle_price: float,
    coverage_type: str,
    vehicle_usage: str,
) -> dict[str, int | str]:
    current_year = datetime.now().year
    vehicle_age = max(current_year - vehicle_year, 0)

    score = 0
    score += 2 if vehicle_age > 10 else 1 if vehicle_age > 5 else 0
    score += 2 if vehicle_price > 1_000_000_000 else 1 if vehicle_price > 500_000_000 else 0
    score += 2 if vehicle_usage == "Commercial" else 0
    score += 1 if coverage_type == "Comprehensive" else 0

    if score <= 2:
        return {
            "vehicle_age": vehicle_age,
            "risk_level": "Low",
            "decision": "Approved",
            "notes": "Low risk profile, no survey required.",
        }
    if score <= 4:
        return {
            "vehicle_age": vehicle_age,
            "risk_level": "Medium",
            "decision": "Need Survey",
            "notes": "Medium risk profile, survey required before final approval.",
        }
    return {
        "vehicle_age": vehicle_age,
        "risk_level": "High",
        "decision": "Rejected",
        "notes": "High risk profile beyond underwriting appetite.",
    }
