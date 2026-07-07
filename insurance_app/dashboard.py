from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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

# ── Corporate colour palette ──────────────────────────────────────────────────
CORPORATE_COLORS = [
    "#0A1F3D",  # Deep Navy
    "#C8973A",  # Gold
    "#1A56DB",  # Royal Blue
    "#0D7C4E",  # Forest Green
    "#7C3AED",  # Violet
    "#D97706",  # Amber
    "#0369A1",  # Sky Blue
    "#C0392B",  # Crimson
    "#4B5E78",  # Slate
    "#0F766E",  # Teal
]

PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, -apple-system, sans-serif", color="#0A1F3D", size=12),
    plot_bgcolor="#FFFFFF",
    paper_bgcolor="#FFFFFF",
    title_font=dict(family="Inter, sans-serif", size=15, color="#0A1F3D"),
    legend=dict(
        font=dict(family="Inter, sans-serif", size=11, color="#4B5E78"),
        bgcolor="rgba(255,255,255,0.9)",
        bordercolor="#DDE4EE",
        borderwidth=1,
    ),
    margin=dict(t=50, b=40, l=40, r=20),
    xaxis=dict(
        gridcolor="#EDF1F7",
        linecolor="#DDE4EE",
        tickfont=dict(family="Inter, sans-serif", size=11, color="#4B5E78"),
        title_font=dict(family="Inter, sans-serif", size=12, color="#4B5E78"),
    ),
    yaxis=dict(
        gridcolor="#EDF1F7",
        linecolor="#DDE4EE",
        tickfont=dict(family="Inter, sans-serif", size=11, color="#4B5E78"),
        title_font=dict(family="Inter, sans-serif", size=12, color="#4B5E78"),
    ),
)


def _apply_layout(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(title_text=title, **PLOTLY_LAYOUT)
    return fig


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
    fig = px.bar(
        grouped, x="area", y="count", color="area",
        color_discrete_sequence=CORPORATE_COLORS,
        labels={"area": "Area", "count": "Applications"},
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    return _apply_layout(fig, "Applications by Area")


def chart_applications_by_coverage(df: pd.DataFrame):
    grouped = df.groupby("coverage_type").size().reset_index(name="count")
    fig = px.pie(
        grouped, names="coverage_type", values="count",
        color_discrete_sequence=CORPORATE_COLORS,
        hole=0.4,
    )
    fig.update_traces(textfont=dict(family="Inter, sans-serif", size=12))
    return _apply_layout(fig, "Applications by Coverage Type")


def chart_applications_by_status(df: pd.DataFrame):
    grouped = df.groupby("status").size().reset_index(name="count")
    status_colors = {
        "Submitted": "#D97706",
        "Document Verified": "#1A56DB",
        "Underwriting": "#7C3AED",
        "Approved": "#0D7C4E",
        "Rejected": "#C0392B",
        "Policy Issued": "#0369A1",
    }
    grouped["color"] = grouped["status"].map(status_colors).fillna("#4B5E78")
    fig = px.bar(
        grouped, x="status", y="count", color="status",
        color_discrete_map=status_colors,
        labels={"status": "Status", "count": "Applications"},
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    return _apply_layout(fig, "Applications by Status")


def chart_premium_distribution(df: pd.DataFrame):
    fig = px.histogram(
        df, x="total_premium", nbins=30,
        color_discrete_sequence=["#1A56DB"],
        labels={"total_premium": "Total Premium (IDR)"},
        opacity=0.85,
    )
    fig.update_traces(marker_line_color="#0A1F3D", marker_line_width=0.4)
    return _apply_layout(fig, "Premium Distribution")


def chart_brand_distribution(df: pd.DataFrame):
    grouped = df.groupby("brand").size().reset_index(name="count").sort_values("count", ascending=False)
    fig = px.bar(
        grouped, x="brand", y="count", color="brand",
        color_discrete_sequence=CORPORATE_COLORS,
        labels={"brand": "Brand", "count": "Applications"},
    )
    fig.update_traces(marker_line_width=0, opacity=0.92)
    return _apply_layout(fig, "Vehicle Brand Distribution")


def chart_monthly_applications(df: pd.DataFrame):
    grouped = df.groupby("month").size().reset_index(name="count").sort_values("month")
    fig = px.line(
        grouped, x="month", y="count", markers=True,
        labels={"month": "Month", "count": "Applications"},
        color_discrete_sequence=["#0A1F3D"],
    )
    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=8, color="#C8973A", line=dict(width=2, color="#0A1F3D")),
    )
    return _apply_layout(fig, "Monthly Application Trend")


def chart_risk_distribution(df: pd.DataFrame):
    grouped = df.groupby("risk_level").size().reset_index(name="count")
    risk_colors = {"Low": "#0D7C4E", "Medium": "#D97706", "High": "#C0392B"}
    fig = px.pie(
        grouped, names="risk_level", values="count",
        color="risk_level",
        color_discrete_map=risk_colors,
        hole=0.4,
    )
    fig.update_traces(textfont=dict(family="Inter, sans-serif", size=12))
    return _apply_layout(fig, "Risk Level Distribution")
