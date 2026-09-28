"""
PDF generation utilities for receipts and reports
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from pathlib import Path
from config import Config

def generate_fee_receipt(payment):
    """Generate a PDF receipt for fee payment"""
    # Create filename
    filename = f"Receipt_{payment.receipt_number}.pdf"
    filepath = Config.EXPORT_FOLDER / filename
    
    # Create PDF
    doc = SimpleDocTemplate(str(filepath), pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#292044'),
        spaceAfter=30,
        alignment=1  # Center
    )
    
    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#292044'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("OXFORD NOTES", title_style))
    story.append(Paragraph("Fee Payment Receipt", header_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Receipt info
    receipt_data = [
        ['Receipt Number:', payment.receipt_number],
        ['Date:', payment.payment_date.strftime('%d %B %Y')],
        ['', '']
    ]
    
    receipt_table = Table(receipt_data, colWidths=[2*inch, 4*inch])
    receipt_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#292044')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(receipt_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Student details
    story.append(Paragraph("Student Details", header_style))
    
    student = payment.student
    student_data = [
        ['Student ID:', student.student_id],
        ['Name:', f"{student.first_name} {student.last_name}"],
        ['Course:', student.course or 'N/A'],
        ['Batch:', student.batch or 'N/A'],
        ['', '']
    ]
    
    student_table = Table(student_data, colWidths=[2*inch, 4*inch])
    student_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#292044')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(student_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Payment details
    story.append(Paragraph("Payment Details", header_style))
    
    payment_data = [
        ['Description', 'Amount'],
        ['Fee Payment', f'₹ {payment.amount:.2f}'],
        ['', ''],
        ['Total Amount', f'₹ {payment.amount:.2f}']
    ]
    
    payment_table = Table(payment_data, colWidths=[4*inch, 2*inch])
    payment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#292044')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -2), 0.5, colors.grey),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.HexColor('#292044')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 12),
    ]))
    
    story.append(payment_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Additional info
    info_data = [
        ['Payment Mode:', payment.payment_mode.upper()],
    ]
    
    if payment.transaction_id:
        info_data.append(['Transaction ID:', payment.transaction_id])
    
    if payment.remarks:
        info_data.append(['Remarks:', payment.remarks])
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#292044')),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    story.append(info_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=1
    )
    
    story.append(Paragraph("This is a computer-generated receipt.", footer_style))
    story.append(Paragraph(f"Generated on {datetime.now().strftime('%d %B %Y at %I:%M %p')}", footer_style))
    
    # Build PDF
    doc.build(story)
    
    return filepath
