"""
PDF Report Generator for Smart Resume Analyzer.
Generates professional PDF reports with evaluation results.
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from typing import Optional
import os


def generate_pdf_report(
    session_data,
    output_path: str,
) -> str:
    """
    Generate a PDF report from evaluation results.
    
    Args:
        session_data: SessionData object with resume, JD, and evaluation
        output_path: Path to save the PDF file
    
    Returns:
        Path to generated PDF file
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72,
    )
    
    # Build the document
    story = []
    styles = _get_custom_styles()
    
    # Header
    story.append(Paragraph("Smart Resume & Job Fit Analysis Report", styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
        styles['Subtitle']
    ))
    story.append(Spacer(1, 30))
    
    # Score Overview
    if session_data.evaluation:
        eval_result = session_data.evaluation
        
        # Main Score
        story.append(Paragraph("Overall Job Fit Score", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        score = eval_result.job_fit_score
        score_color = _get_score_color(score)
        score_text = f'<font size="36" color="{score_color}"><b>{score}/100</b></font>'
        story.append(Paragraph(score_text, styles['CenterText']))
        story.append(Paragraph(
            f'<font color="{score_color}">{_get_score_label(score)}</font>',
            styles['CenterText']
        ))
        story.append(Spacer(1, 20))
        
        # Score Breakdown Table
        story.append(Paragraph("Score Breakdown", styles['Heading2']))
        story.append(Spacer(1, 8))
        
        breakdown = eval_result.score_breakdown
        breakdown_data = [
            ['Category', 'Score', 'Weight'],
            ['Required Skills', f"{breakdown.required_skills_score:.1f}%", '40%'],
            ['Preferred Skills', f"{breakdown.optional_skills_score:.1f}%", '25%'],
            ['Experience Match', f"{breakdown.experience_depth_score:.1f}%", '25%'],
            ['Education Match', f"{breakdown.education_match_score:.1f}%", '10%'],
        ]
        
        breakdown_table = Table(breakdown_data, colWidths=[3*inch, 1.5*inch, 1*inch])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3B82F6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F3F4F6')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 25))
        
        # Skills Analysis
        story.append(Paragraph("Skills Analysis", styles['Heading1']))
        story.append(Spacer(1, 12))
        
        # Matched Skills
        # Matched Skills
        # Safely handle Enum or string for match_type
        def get_val(obj):
            return getattr(obj, "value", str(obj))

        matched_skills = [m for m in eval_result.skill_matches if get_val(m.match_type) == 'matched']
        if matched_skills:
            story.append(Paragraph("✓ Matched Skills", styles['Heading2']))
            story.append(Spacer(1, 6))
            for skill in matched_skills:
                priority = "Required" if get_val(skill.jd_priority) == 'required' else "Preferred"
                evidence_text = f" - Evidence: \"{skill.evidence[:50]}...\"" if skill.evidence and len(skill.evidence) > 50 else f" - Evidence: \"{skill.evidence}\"" if skill.evidence else ""
                story.append(Paragraph(
                    f"• <b>{skill.canonical_name}</b> ({priority}){evidence_text}",
                    styles['Normal']
                ))
            story.append(Spacer(1, 12))
        
        # Missing Skills
        missing_skills = [m for m in eval_result.skill_matches if get_val(m.match_type) == 'missing']
        if missing_skills:
            story.append(Paragraph("✗ Missing Skills", styles['Heading2']))
            story.append(Spacer(1, 6))
            for skill in missing_skills:
                priority = "Required" if get_val(skill.jd_priority) == 'required' else "Preferred"
                story.append(Paragraph(
                    f"• <b>{skill.canonical_name}</b> ({priority})",
                    styles['Normal']
                ))
            story.append(Spacer(1, 12))
        
        # Improvement Suggestions
        if eval_result.improvement_suggestions:
            story.append(PageBreak())
            story.append(Paragraph("Improvement Suggestions", styles['Heading1']))
            story.append(Spacer(1, 12))
            
            for i, suggestion in enumerate(eval_result.improvement_suggestions, 1):
                # Priority badge (1=High, 5=Low)
                priority_val = suggestion.priority
                if priority_val <= 2:
                    p_color = '#EF4444' # High
                elif priority_val <= 3:
                    p_color = '#F59E0B' # Medium
                else:
                    p_color = '#10B981' # Low
                
                story.append(Paragraph(
                    f"<font color=\"{p_color}\"><b>{i}. {suggestion.category.upper()}</b></font>",
                    styles['Normal']
                ))
                story.append(Paragraph(suggestion.suggestion, styles['Normal']))
                if suggestion.evidence_gap:
                    story.append(Paragraph(f"   → Gap: {suggestion.evidence_gap}", styles['Normal']))
                if suggestion.affected_skills:
                    skills_text = ", ".join(suggestion.affected_skills)
                    story.append(Paragraph(f"   → Affected: {skills_text}", styles['Normal']))
                story.append(Spacer(1, 10))
    
    # Footer disclaimer
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB')))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "<i>This analysis is for informational purposes only. The scores and suggestions "
        "are generated by a rule-based system and should be used as guidance, not as the "
        "sole factor in hiring decisions.</i>",
        styles['Disclaimer']
    ))
    
    # Build PDF
    doc.build(story)
    return output_path


def _get_custom_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()
    
    # helper to add or update
    def add_or_update(utils_style):
        if utils_style.name in styles:
            # Update existing properties
            existing = styles[utils_style.name]
            existing.__dict__.update(utils_style.__dict__)
        else:
            styles.add(utils_style)
    
    add_or_update(ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=6,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1F2937'),
    ))
    
    add_or_update(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#6B7280'),
    ))
    
    # Heading1 and Heading2 already exist, so we update them
    add_or_update(ParagraphStyle(
        name='Heading1',
        parent=styles['Heading1'],
        fontSize=16,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.HexColor('#1F2937'),
    ))
    
    add_or_update(ParagraphStyle(
        name='Heading2',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.HexColor('#374151'),
    ))
    
    add_or_update(ParagraphStyle(
        name='CenterText',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=14,
    ))
    
    add_or_update(ParagraphStyle(
        name='Disclaimer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#9CA3AF'),
        alignment=TA_CENTER,
    ))
    
    return styles


def _get_score_color(score: int) -> str:
    """Get color for score display."""
    if score >= 80:
        return '#10B981'  # Green
    elif score >= 60:
        return '#3B82F6'  # Blue
    elif score >= 40:
        return '#F59E0B'  # Yellow
    else:
        return '#EF4444'  # Red


def _get_score_label(score: int) -> str:
    """Get label for score."""
    if score >= 80:
        return 'Excellent Match'
    elif score >= 60:
        return 'Good Match'
    elif score >= 40:
        return 'Moderate Match'
    else:
        return 'Needs Improvement'
