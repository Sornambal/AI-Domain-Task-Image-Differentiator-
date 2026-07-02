import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

def register_fonts():
    font_path = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "Roboto-Regular.ttf"
    if font_path.exists():
        pdfmetrics.registerFont(TTFont("Roboto", str(font_path)))
        return "Roboto"
    return "Helvetica"

def generate_pdf_report(comparison_data: dict, output_path: str) -> str:
    font_name = register_fonts()
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=20 * mm,
        leftMargin=15 * mm,
        rightMargin=15 * mm,
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Heading1"],
        fontName=font_name,
        fontSize=24,
        textColor=colors.black,
        spaceAfter=10,
    )
    meta_style = ParagraphStyle(
        "ReportMeta",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=10,
        textColor=colors.dimgrey,
        spaceAfter=20,
    )
    header_style = ParagraphStyle(
        "SectionHeader",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=16,
        textColor=colors.black,
        spaceBefore=15,
        spaceAfter=10,
    )
    normal_style = ParagraphStyle(
        "NormalText",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=11,
        textColor=colors.black,
        spaceAfter=5,
        leading=14,
    )
    
    story = []
    
    story.append(Paragraph("CAD Comparison Report", title_style))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on {timestamp}", meta_style))
    
    def add_image(image_url: str):
        if not image_url:
            return
        file_name = image_url.split("/")[-1]
        local_path = Path(__file__).resolve().parents[1] / "uploads" / file_name
        if local_path.exists():
            img = Image(str(local_path), width=180*mm, height=180*mm, kind='proportional')
            story.append(img)
        else:
            story.append(Paragraph(f"[Image not found: {file_name}]", normal_style))
    
    story.append(Paragraph("Reference Drawing", header_style))
    add_image(comparison_data.get("original_a_url", ""))
    
    story.append(Paragraph("Comparison Drawing", header_style))
    add_image(comparison_data.get("original_b_url", ""))
    
    story.append(PageBreak())
    
    story.append(Paragraph("Difference Overlay", header_style))
    add_image(comparison_data.get("diff_visualization_url", ""))
    
    story.append(Paragraph("Heatmap Analysis", header_style))
    add_image(comparison_data.get("heatmap_url", ""))
    
    story.append(PageBreak())
    
    story.append(Paragraph("Difference Statistics", header_style))
    stats = comparison_data.get("statistics", {})
    regions = stats.get("regions", [])
    
    if regions:
        table_data = [["Number", "Location", "Type", "Dimensions", "Area (px)"]]
        for r in regions:
            table_data.append([
                str(r.get("number", "")),
                str(r.get("location", "")),
                str(r.get("type", "")).capitalize(),
                f"{r.get('width', 0)}x{r.get('height', 0)}",
                str(r.get("area_px", "")),
            ])
            
        t = Table(table_data, colWidths=[20*mm, 40*mm, 30*mm, 40*mm, 40*mm])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.black),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,0), font_name),
            ('FONTSIZE', (0,0), (-1,0), 12),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.whitesmoke),
            ('FONTNAME', (0,1), (-1,-1), font_name),
            ('GRID', (0,0), (-1,-1), 1, colors.black),
        ]))
        story.append(t)
    else:
        story.append(Paragraph("No significant differences found.", normal_style))
        
    story.append(Spacer(1, 10*mm))
    
    story.append(Paragraph("AI Summary", header_style))
    ai_summary = comparison_data.get("ai_summary", "No AI summary available.")
    story.append(Paragraph(ai_summary, normal_style))
    
    if regions:
        story.append(Spacer(1, 10*mm))
        story.append(Paragraph("Region Descriptions", header_style))
        for r in regions:
            num = r.get("number")
            desc = r.get("description", "No description generated.")
            story.append(Paragraph(f"<b>Region #{num}:</b> {desc}", normal_style))
            story.append(Spacer(1, 2*mm))

    doc.build(story)
    return output_path
