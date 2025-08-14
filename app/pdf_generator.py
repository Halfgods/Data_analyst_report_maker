import os
import io
import base64
from datetime import datetime
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import pandas as pd

def generate_summary_stats_table(stats_data: Dict[str, Any]) -> List[List[str]]:
    """
    Convert descriptive statistics into a table format for PDF.
    """
    if not stats_data:
        return [["No statistical data available"]]
    
    table_data = [["Column", "Count", "Mean", "Std", "Min", "25%", "50%", "75%", "Max"]]
    
    for column, stats in stats_data.items():
        if isinstance(stats, dict) and 'count' in stats:
            row = [
                str(column),
                str(round(stats.get('count', 0))),
                str(round(stats.get('mean', 0), 2)) if stats.get('mean') is not None else "N/A",
                str(round(stats.get('std', 0), 2)) if stats.get('std') is not None else "N/A",
                str(round(stats.get('min', 0), 2)) if stats.get('min') is not None else "N/A",
                str(round(stats.get('25%', 0), 2)) if stats.get('25%') is not None else "N/A",
                str(round(stats.get('50%', 0), 2)) if stats.get('50%') is not None else "N/A",
                str(round(stats.get('75%', 0), 2)) if stats.get('75%') is not None else "N/A",
                str(round(stats.get('max', 0), 2)) if stats.get('max') is not None else "N/A"
            ]
            table_data.append(row)
    
    return table_data

def generate_correlation_table(corr_data: Dict[str, Any]) -> List[List[str]]:
    """
    Convert correlation matrix into a table format for PDF.
    """
    if not corr_data:
        return [["No correlation data available"]]
    
    # Get column names
    columns = list(corr_data.keys())
    if not columns:
        return [["No correlation data available"]]
    
    # Create header row
    table_data = [[""] + columns]
    
    # Create data rows
    for row_col in columns:
        row = [row_col]
        for col_col in columns:
            corr_val = corr_data.get(row_col, {}).get(col_col, 0)
            if isinstance(corr_val, (int, float)):
                row.append(str(round(corr_val, 3)))
            else:
                row.append("N/A")
        table_data.append(row)
    
    return table_data

def embed_chart_images(session_dir: str, chart_urls: Dict[str, List[str]]) -> List[str]:
    """
    Get list of chart image paths for embedding in PDF.
    """
    chart_paths = []
    
    for chart_type, urls in chart_urls.items():
        for url in urls:
            # Convert URL to file path
            chart_name = url.split('/')[-1]  # Extract filename from URL
            chart_path = os.path.join(session_dir, chart_name)
            if os.path.exists(chart_path):
                chart_paths.append(chart_path)
    
    return chart_paths

def generate_pdf_report(
    session_id: str,
    csv_metadata: Dict[str, Any],
    analysis_results: Dict[str, Any],
    ai_commentary: str,
    session_dir: str,
    chart_urls: Dict[str, List[str]] = None
) -> str:
    """
    Generate a comprehensive PDF report from analysis data.
    Returns the path to the generated PDF file.
    """
    
    # Create PDF filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"data_analysis_report_{session_id[:8]}_{timestamp}.pdf"
    pdf_path = os.path.join(session_dir, pdf_filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=18
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e40af'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=20,
        spaceAfter=10
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#374151'),
        spaceBefore=15,
        spaceAfter=8
    )
    
    body_style = styles['Normal']
    body_style.fontSize = 10
    body_style.leading = 12
    
    # Build PDF content
    story = []
    
    # Title
    story.append(Paragraph("Data Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    # Report metadata
    report_info = f"""
    <b>Session ID:</b> {session_id}<br/>
    <b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>
    <b>Report Type:</b> Comprehensive Data Analysis
    """
    story.append(Paragraph(report_info, body_style))
    story.append(Spacer(1, 30))
    
    # Dataset Overview
    story.append(Paragraph("Dataset Overview", heading_style))
    
    if csv_metadata and csv_metadata.get('files'):
        file_info = csv_metadata['files'][0]  # First file info
        dataset_info = f"""
        <b>Filename:</b> {file_info.get('filename', 'Unknown')}<br/>
        <b>Total Rows:</b> {file_info.get('rows', 'Unknown'):,}<br/>
        <b>Total Columns:</b> {len(file_info.get('columns', []))}<br/>
        <b>Data Types:</b> {len(file_info.get('inferred_types', {}))} detected
        """
        story.append(Paragraph(dataset_info, body_style))
        
        # Column information
        if file_info.get('columns'):
            story.append(Paragraph("Columns", subheading_style))
            columns_text = ", ".join(file_info['columns'][:20])  # First 20 columns
            if len(file_info['columns']) > 20:
                columns_text += f", ... and {len(file_info['columns']) - 20} more"
            story.append(Paragraph(columns_text, body_style))
    
    story.append(Spacer(1, 20))
    
    # Statistical Analysis
    story.append(Paragraph("Statistical Analysis", heading_style))
    
    if analysis_results.get('descriptive_statistics'):
        story.append(Paragraph("Descriptive Statistics", subheading_style))
        stats_table_data = generate_summary_stats_table(analysis_results['descriptive_statistics'])
        
        if len(stats_table_data) > 1:  # Has data beyond header
            stats_table = Table(stats_table_data)
            stats_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(stats_table)
        story.append(Spacer(1, 15))
    
    # Correlation Analysis
    if analysis_results.get('correlation_matrix'):
        story.append(Paragraph("Correlation Matrix", subheading_style))
        corr_table_data = generate_correlation_table(analysis_results['correlation_matrix'])
        
        if len(corr_table_data) > 1:  # Has data beyond header
            corr_table = Table(corr_table_data)
            corr_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f3f4f6')),
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f3f4f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#1f2937')),
                ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1f2937')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(corr_table)
        story.append(Spacer(1, 20))
    
    # Data Visualization
    if chart_urls:
        story.append(Paragraph("Data Visualizations", heading_style))
        chart_paths = embed_chart_images(session_dir, chart_urls)
        
        for i, chart_path in enumerate(chart_paths[:6]):  # Limit to 6 charts to avoid oversized PDF
            try:
                # Add chart image
                img = Image(chart_path)
                img.drawHeight = 3 * inch
                img.drawWidth = 4 * inch
                story.append(img)
                story.append(Spacer(1, 10))
                
                # Page break after every 2 charts
                if (i + 1) % 2 == 0 and i < len(chart_paths) - 1:
                    story.append(PageBreak())
            except Exception as e:
                story.append(Paragraph(f"Chart could not be loaded: {os.path.basename(chart_path)}", body_style))
                story.append(Spacer(1, 10))
    
    # AI Analysis
    if ai_commentary:
        story.append(PageBreak())
        story.append(Paragraph("AI-Powered Insights", heading_style))
        
        # Clean and format AI commentary
        ai_text = ai_commentary.replace('\n', '<br/>')
        if len(ai_text) > 3000:  # Truncate very long commentary
            ai_text = ai_text[:3000] + "... [truncated]"
        
        story.append(Paragraph(ai_text, body_style))
        story.append(Spacer(1, 20))
    
    # Data Quality Summary
    if analysis_results.get('data_quality'):
        dq = analysis_results['data_quality']
        story.append(Paragraph("Data Quality Assessment", heading_style))
        
        quality_info = f"""
        <b>Total Records:</b> {dq.get('total_rows', 'Unknown'):,}<br/>
        <b>Total Features:</b> {dq.get('total_columns', 'Unknown')}<br/>
        <b>Missing Values:</b> {dq.get('missing_values_total', 0)}<br/>
        <b>Duplicate Records:</b> {dq.get('duplicate_rows', 0)}<br/>
        <b>Completeness:</b> {round((1 - dq.get('missing_values_total', 0) / max(dq.get('total_rows', 1) * dq.get('total_columns', 1), 1)) * 100, 2)}%
        """
        story.append(Paragraph(quality_info, body_style))
    
    # Footer
    story.append(Spacer(1, 30))
    footer_text = f"Report generated by DataLens AI Analytics Platform | Session: {session_id}"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.gray,
        alignment=TA_CENTER
    )
    story.append(Paragraph(footer_text, footer_style))
    
    # Build PDF
    doc.build(story)
    
    return pdf_path

def get_pdf_report_info(pdf_path: str) -> Dict[str, Any]:
    """
    Get information about the generated PDF report.
    """
    if not os.path.exists(pdf_path):
        return {"error": "PDF file not found"}
    
    file_size = os.path.getsize(pdf_path)
    return {
        "filename": os.path.basename(pdf_path),
        "file_path": pdf_path,
        "size_bytes": file_size,
        "size_mb": round(file_size / (1024 * 1024), 2),
        "created_at": datetime.fromtimestamp(os.path.getctime(pdf_path)).isoformat()
    }
