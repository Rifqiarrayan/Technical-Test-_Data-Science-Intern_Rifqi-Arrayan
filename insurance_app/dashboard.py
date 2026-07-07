from __future__ import annotations

import pandas as pd
import plotly.express as px
from sqlalchemy import func

from database import (
    Application,
    Customer,
    Policy,
    PremiumResult,
    SessionLocal,
    UnderwritingResult,
    Vehicle,
)


def load_dashboard_data() -> dict[str, pd.DataFrame]:
    with SessionLocal() as session:
        customers = pd.read_sql(session.query(Customer).statement, session.bind)
        vehicles = pd.read_sql(session.query(Vehicle).statement, session.bind)
        applications = pd.read_sql(session.query(Application).statement, session.bind)
        premium_results = pd.read_sql(session.query(PremiumResult).statement, session.bind)
        underwriting = pd.read_sql(session.query(UnderwritingResult).statement, session.bind)
        policies = pd.read_sql(session.query(Policy).statement, session.bind)

    merged = applications.merge(
        vehicles[["id", "brand", "vehicle_price", "area", "year"]],
        left_on="vehicle_id",
        right_on="id",
        how="left",
        suffixes=("", "_vehicle"),
    ).merge(
        premium_results[["application_id", "total_premium"]],
        left_on="id",
        right_on="application_id",
        how="left",
        suffixes=("", "_premium"),
    ).merge(
        underwriting[["application_id", "risk_level", "decision"]],
        left_on="id",
        right_on="application_id",
        how="left",
        suffixes=("", "_uw"),
    )

    merged["submitted_at"] = pd.to_datetime(merged["submitted_at"], errors="coerce")
    merged["month"] = merged["submitted_at"].dt.to_period("M").astype(str)

    return {
        "customers": customers,
        "vehicles": vehicles,
        "applications": applications,
        "premium_results": premium_results,
        "underwriting": underwriting,
        "policies": policies,
        "merged": merged,
    }


def get_kpis(data: dict[str, pd.DataFrame]) -> dict[str, float]:
    apps = data["applications"]
    premiums = data["premium_results"]
    vehicles = data["vehicles"]
    policies = data["policies"]

    return {
        "total_customers": float(len(data["customers"])),
        "total_applications": float(len(apps)),
        "approved_applications": float((apps["status"] == "Approved").sum()),
        "rejected_applications": float((apps["status"] == "Rejected").sum()),
        "issued_policies": float(len(policies)),
        "avg_premium": float(premiums["total_premium"].mean() if not premiums.empty else 0),
        "avg_vehicle_price": float(vehicles["vehicle_price"].mean() if not vehicles.empty else 0),
    }


def chart_applications_by_area(df: pd.DataFrame):
    grouped = df.groupby("area").size().reset_index(name="count")
    return px.bar(grouped, x="area", y="count", color="area", title="Applications by Area")


def chart_applications_by_coverage(df: pd.DataFrame):
    grouped = df.groupby("coverage_type").size().reset_index(name="count")
    return px.pie(grouped, names="coverage_type", values="count", title="Applications by Coverage")


def chart_applications_by_status(df: pd.DataFrame):
    grouped = df.groupby("status").size().reset_index(name="count")
    return px.bar(grouped, x="status", y="count", color="status", title="Applications by Status")


def chart_premium_distribution(df: pd.DataFrame):
    return px.histogram(df, x="total_premium", nbins=30, title="Premium Distribution")


def chart_brand_distribution(df: pd.DataFrame):
    grouped = df.groupby("brand").size().reset_index(name="count")
    return px.bar(grouped, x="brand", y="count", color="brand", title="Vehicle Brand Distribution")


def chart_monthly_applications(df: pd.DataFrame):
    grouped = df.groupby("month").size().reset_index(name="count").sort_values("month")
    return px.line(grouped, x="month", y="count", markers=True, title="Monthly Applications")


def chart_risk_distribution(df: pd.DataFrame):
    grouped = df.groupby("risk_level").size().reset_index(name="count")
    return px.pie(grouped, names="risk_level", values="count", title="Risk Level Distribution")
