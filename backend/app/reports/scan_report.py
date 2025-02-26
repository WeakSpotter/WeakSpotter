from io import BytesIO
from xml.sax.saxutils import escape

from app.models.result import Severity
from app.models.scan import Scan
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# Custom colors
DARK_GRAY = colors.HexColor("#333333")
LIGHT_GRAY = colors.HexColor("#F5F5F5")
PRIMARY_COLOR = colors.HexColor("#1a73e8")

# Custom styles
styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        spaceAfter=30,
        textColor=PRIMARY_COLOR,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        name="SectionHeader",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=DARK_GRAY,
        borderPadding=(0, 0, 8, 0),  # top, right, bottom, left
        borderWidth=0,
        borderColor=PRIMARY_COLOR,
    )
)
styles.add(
    ParagraphStyle(
        name="ResultTitle",
        parent=styles["Heading3"],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=5,
        textColor=DARK_GRAY,
    )
)
styles.add(
    ParagraphStyle(
        name="NormalText",
        parent=styles["Normal"],
        fontSize=10,
        textColor=DARK_GRAY,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    )
)

# Severity styling
severity_colors = {
    Severity.critical: colors.HexColor("#DC3545"),  # Red
    Severity.error: colors.HexColor("#FD7E14"),  # Orange
    Severity.warning: colors.HexColor("#FFC107"),  # Yellow
    Severity.info: colors.HexColor("#28A745"),  # Green
    Severity.debug: colors.HexColor("#6C757D"),  # Gray
}


def create_severity_badge(severity: Severity) -> str:
    """Create a styled severity badge."""
    color = f"{severity_colors[severity].hexval()}"  # Get the hex color value
    return f'<font color="{color}"><b>{severity.name.upper()}</b></font>'


def generate_scan_report(scan: Scan) -> BytesIO:
    """Generate a beautifully styled PDF report for a scan."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=25 * mm,
        leftMargin=25 * mm,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
    )

    story = []

    # Title
    story.append(Paragraph("Security Scan Report", styles["CustomTitle"]))

    # Scan Information Table
    story.append(Paragraph("Scan Overview", styles["SectionHeader"]))

    scan_info = [
        ["Target URL", scan.url],
        ["Scan Date", scan.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")],
        ["Security Score", f"{scan.score:.1f}/100"],
    ]

    scan_info_table = Table(
        scan_info,
        colWidths=[120, 350],
        style=TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_GRAY),
                ("TEXTCOLOR", (0, 0), (-1, -1), DARK_GRAY),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
                ("TOPPADDING", (0, 0), (-1, -1), 12),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("GRID", (0, 0), (-1, -1), 1, colors.white),
            ]
        ),
    )
    story.append(scan_info_table)
    story.append(Spacer(1, 20))

    # Results Section
    if scan.results:
        story.append(Paragraph("Security Findings", styles["SectionHeader"]))

        # Sort results by severity and score
        sorted_results = sorted(
            scan.results, key=lambda x: (-x.severity.value, -x.score)
        )

        for result in sorted_results:
            # Escape user-provided content
            safe_title = escape(result.title)
            safe_short_description = (
                escape(result.short_description) if result.short_description else ""
            )
            safe_description = escape(result.description) if result.description else ""
            safe_recommendation = (
                escape(result.recommendation) if result.recommendation else ""
            )

            result_data = [
                [
                    Paragraph(f"{safe_title}", styles["ResultTitle"]),
                    Paragraph(
                        f"{create_severity_badge(result.severity)} Score Impact: {result.score:+d}",
                        ParagraphStyle(
                            "SeverityStyle",
                            parent=styles["Normal"],
                            alignment=TA_CENTER,
                        ),
                    ),
                ]
            ]

            if result.short_description:
                result_data.append(
                    [
                        Paragraph(safe_short_description, styles["NormalText"]),
                        Paragraph("", styles["NormalText"]),
                    ]
                )

            if result.description:
                result_data.append(
                    [
                        Paragraph(
                            f"<b>Details:</b><br/>{safe_description}",
                            styles["NormalText"],
                        ),
                        Paragraph("", styles["NormalText"]),
                    ]
                )

            if result.recommendation:
                result_data.append(
                    [
                        Paragraph(
                            f"<b>Recommendation:</b><br/>{safe_recommendation}",
                            styles["NormalText"],
                        ),
                        Paragraph("", styles["NormalText"]),
                    ]
                )

            result_table = Table(
                result_data,
                colWidths=[380, 90],
                style=TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                        ("TEXTCOLOR", (0, 0), (-1, -1), DARK_GRAY),
                        ("ALIGN", (0, 0), (0, 0), "LEFT"),
                        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
                        ("SPAN", (0, 1), (1, 1)),  # Merge cells for description
                        ("SPAN", (0, 2), (1, 2)),  # Merge cells for details
                        ("SPAN", (0, 3), (1, 3)),  # Merge cells for recommendation
                        ("LEFTPADDING", (0, 0), (-1, -1), 10),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                        ("TOPPADDING", (0, 0), (-1, -1), 10),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                        ("GRID", (0, 0), (-1, -1), 1, colors.white),
                    ]
                ),
            )
            story.append(result_table)
            story.append(Spacer(1, 10))
    else:
        story.append(
            Paragraph(
                "No security issues were found during the scan.", styles["NormalText"]
            )
        )

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
