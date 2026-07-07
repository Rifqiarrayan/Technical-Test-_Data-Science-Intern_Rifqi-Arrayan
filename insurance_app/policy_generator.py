from __future__ import annotations

import io
from datetime import date, timedelta
from uuid import uuid4

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def generate_policy_number() -> str:
    today = date.today()
    return f"ETQ-MTR-{today.strftime('%Y%m')}-{str(uuid4())[:8].upper()}"


def policy_dates() -> dict[str, date]:
    issue = date.today()
    return {
        "issue_date": issue,
        "effective_date": issue,
        "expiry_date": issue + timedelta(days=365),
    }


def generate_policy_pdf(policy_data: dict[str, str | float]) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Etiqa Insurance Indonesia", styles["Title"]))
    elements.append(Paragraph("Motor Vehicle Insurance Policy", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    table_data = [
        ["Policy Number", str(policy_data["policy_number"])],
        ["Issue Date", str(policy_data["issue_date"])],
        ["Effective Date", str(policy_data["effective_date"])],
        ["Expiry Date", str(policy_data["expiry_date"])],
        ["Application ID", str(policy_data["application_id"])],
        ["Customer Name", str(policy_data["customer_name"])],
        ["NIK", str(policy_data["nik"])],
        ["Vehicle", f"{policy_data['brand']} {policy_data['model']} ({policy_data['year']})"],
        ["Plate Number", str(policy_data["plate_number"])],
        ["Coverage", str(policy_data["coverage_type"])],
        ["Total Premium", f"IDR {float(policy_data['total_premium']):,.0f}"],
        ["Policy Status", str(policy_data.get("status", "Issued"))],
    ]

    details_table = Table(table_data, colWidths=[50 * mm, 110 * mm])
    details_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EAF2FF")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#0B2B5C")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B8C8E5")),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(details_table)
    elements.append(Spacer(1, 16))
    elements.append(
        Paragraph(
            "This policy is generated digitally and valid without a wet signature.",
            styles["Italic"],
        )
    )

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
