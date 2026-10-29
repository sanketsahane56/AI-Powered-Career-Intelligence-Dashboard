"""
CareerIQ - Executive PDF Report Generator
Generates clean, professionally formatted executive career intelligence PDF reports
using ReportLab with scorecards, skill breakdowns, role matches, and action plans.
"""

import io
from datetime import datetime
from typing import Dict, Any
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class ReportGenerator:
    """Builds downloadable PDF analysis reports."""

    @classmethod
    def generate_pdf(cls, analysis_data: Dict[str, Any], metadata: Dict[str, Any]) -> io.BytesIO:
        """Constructs an in-memory PDF binary stream."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        
        # Custom styles
        brand_color = colors.HexColor("#0B132B")
        accent_blue = colors.HexColor("#2563EB")
        text_dark = colors.HexColor("#0F172A")
        text_muted = colors.HexColor("#64748B")
        bg_card = colors.HexColor("#F8FAFC")
        border_color = colors.HexColor("#E2E8F0")

        title_style = ParagraphStyle(
            "ReportTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=brand_color
        )
        subtitle_style = ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=14,
            textColor=text_muted
        )
        h2_style = ParagraphStyle(
            "H2Style",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=brand_color,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            "BodyDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=13.5,
            textColor=text_dark
        )
        small_style = ParagraphStyle(
            "SmallDark",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=11.5,
            textColor=text_muted
        )
        bold_style = ParagraphStyle(
            "BoldDark",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=13.5,
            textColor=text_dark
        )

        story = []

        # 1. Header with Brand & Meta
        candidate_name = metadata.get("candidate_name", "Candidate")
        today_str = datetime.now().strftime("%B %d, %Y")
        
        header_table = Table(
            [
                [
                    Paragraph("<b>CareerIQ</b> &bull; Career Intelligence Report", title_style),
                    Paragraph(f"<b>Date:</b> {today_str}<br/><b>Candidate:</b> {candidate_name}", subtitle_style)
                ]
            ],
            colWidths=[360, 180]
        )
        header_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceBefore=0, spaceAfter=14))

        # 2. Executive Scorecard
        score = analysis_data.get("overall_score", 0)
        score_color = colors.HexColor("#10B981") if score >= 80 else (colors.HexColor("#F59E0B") if score >= 60 else colors.HexColor("#EF4444"))
        score_label = "EXCEPTIONAL FIT" if score >= 80 else ("SOLID COMPETENCY" if score >= 60 else "NEEDS OPTIMIZATION")

        score_box_style = ParagraphStyle(
            "ScoreBadge",
            fontName="Helvetica-Bold",
            fontSize=32,
            leading=36,
            alignment=1,
            textColor=score_color
        )
        score_sub_style = ParagraphStyle(
            "ScoreSub",
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            alignment=1,
            textColor=score_color
        )

        top_role = "Candidate"
        top_fit = 0
        roles = analysis_data.get("role_matches", [])
        primary_domain = analysis_data.get("primary_domain", "")
        if roles:
            top_role = roles[0].get("role", "Candidate")
            top_fit = roles[0].get("fit_percentage", 0)
            if not primary_domain:
                primary_domain = roles[0].get("domain", "General")

        domain_str = f"<b>Target Domain:</b> <font color='#475569'><b>{primary_domain}</b></font><br/>" if primary_domain else ""
        summary_p = Paragraph(
            f"<b>Primary Role Match:</b> <font color='#2563EB'><b>{top_role}</b></font> ({top_fit}% market alignment)<br/>"
            f"{domain_str}"
            f"<b>Total Verified Skills:</b> {analysis_data.get('skills', {}).get('total_count', 0)} competencies cataloged<br/>"
            f"<b>Quantified Metric Count:</b> {analysis_data.get('metrics', {}).get('count', 0)} measurable outcomes detected<br/>"
            f"<b>ATS Action Voice:</b> {analysis_data.get('verbs', {}).get('strong_count', 0)} high-impact verbs identified",
            body_style
        )

        score_table = Table(
            [
                [
                    [Paragraph(f"{score}", score_box_style), Paragraph(score_label, score_sub_style)],
                    summary_p
                ]
            ],
            colWidths=[140, 400]
        )
        score_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), colors.HexColor("#F1F5F9")),
            ("BACKGROUND", (1, 0), (1, 0), bg_card),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 1, border_color),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 14))

        # 3. Transparent Dimension Breakdown
        story.append(Paragraph("ATS Dimension Score Breakdown", h2_style))
        dims = analysis_data.get("dimensions", {})

        dim_rows = [
            [
                Paragraph("<b>Evaluation Dimension</b>", bold_style),
                Paragraph("<b>Weight</b>", bold_style),
                Paragraph("<b>Score</b>", bold_style),
                Paragraph("<b>Observation & Evidence</b>", bold_style)
            ]
        ]
        for key, dim in dims.items():
            d_score = dim.get("score", 0)
            status_color = "#10B981" if d_score >= 80 else ("#F59E0B" if d_score >= 60 else "#EF4444")
            dim_rows.append([
                Paragraph(f"<b>{dim.get('name')}</b>", body_style),
                Paragraph(dim.get("weight", "-"), small_style),
                Paragraph(f"<font color='{status_color}'><b>{d_score}/100</b></font>", bold_style),
                Paragraph(dim.get("detail", ""), small_style)
            ])

        dim_table = Table(dim_rows, colWidths=[160, 50, 60, 270])
        dim_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(dim_table)
        story.append(Spacer(1, 14))

        # 4. Top Career Role Alignments
        story.append(Paragraph("Market Career Role Compatibility", h2_style))
        role_rows = [
            [
                Paragraph("<b>Target Role Profile</b>", bold_style),
                Paragraph("<b>Match Fit</b>", bold_style),
                Paragraph("<b>Matched Core Skills</b>", bold_style),
                Paragraph("<b>High-Value Gaps</b>", bold_style)
            ]
        ]
        for r in roles[:4]:
            fit = r.get("fit_percentage", 0)
            fit_color = "#10B981" if fit >= 70 else ("#F59E0B" if fit >= 50 else "#64748B")
            matched = ", ".join(r.get("matched_core", [])[:5]) or "None"
            missing = ", ".join(r.get("missing_core", [])[:4]) or "None"
            role_rows.append([
                Paragraph(f"<b>{r.get('role')}</b>", body_style),
                Paragraph(f"<font color='{fit_color}'><b>{fit}%</b></font>", bold_style),
                Paragraph(matched, small_style),
                Paragraph(missing, small_style)
            ])

        role_table = Table(role_rows, colWidths=[150, 60, 165, 165])
        role_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E2E8F0")),
            ("BOX", (0, 0), (-1, -1), 1, border_color),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))
        story.append(role_table)
        story.append(Spacer(1, 14))

        # 5. Technical Skills Inventory
        story.append(Paragraph("Verified Skills Inventory by Domain", h2_style))
        skills_by_cat = analysis_data.get("skills", {}).get("by_category", {})
        skill_paragraphs = []
        for cat, cat_skills in list(skills_by_cat.items())[:6]:
            skill_badges = ", ".join(cat_skills)
            skill_paragraphs.append([
                Paragraph(f"<b>{cat}</b>", bold_style),
                Paragraph(skill_badges, body_style)
            ])

        if skill_paragraphs:
            skills_table = Table(skill_paragraphs, colWidths=[150, 390])
            skills_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg_card),
                ("BOX", (0, 0), (-1, -1), 1, border_color),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, border_color),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.append(skills_table)
            story.append(Spacer(1, 14))

        # 6. Actionable ATS Optimization Plan
        story.append(Paragraph("Actionable ATS Optimization Plan", h2_style))
        actions = analysis_data.get("action_plan", [])
        action_rows = []
        for idx, act in enumerate(actions, 1):
            action_rows.append([
                Paragraph(f"<b>{idx}.</b>", bold_style),
                Paragraph(act, body_style)
            ])

        if action_rows:
            action_table = Table(action_rows, colWidths=[20, 520])
            action_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))
            story.append(action_table)

        # Footer note
        story.append(Spacer(1, 18))
        story.append(HRFlowable(width="100%", thickness=0.5, color=border_color, spaceBefore=0, spaceAfter=8))
        story.append(Paragraph(
            "<b>CareerIQ Disclaimer:</b> Scoring is based on standard applicant tracking system (ATS) heuristics and market taxonomy comparisons. "
            "Scores do not guarantee employment offers.",
            small_style
        ))

        doc.build(story)
        buffer.seek(0)
        return buffer
