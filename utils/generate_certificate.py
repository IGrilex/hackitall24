# utils/generate_certificate.py

from fpdf import FPDF
from io import BytesIO
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Optional: Add a header to each page
        pass

    def footer(self):
        # Optional: Add a footer to each page
        pass

def create_certificate(first_name, last_name, level, date):
    pdf = PDF()
    pdf.add_page()

    # Set up fonts
    pdf.set_font("Arial", 'B', 24)
    
    # Title
    pdf.cell(0, 20, "Certificate of Achievement", ln=True, align='C')

    # Spacer
    pdf.ln(10)

    # Subtitle
    pdf.set_font("Arial", '', 16)
    pdf.cell(0, 10, "This certificate is proudly presented to", ln=True, align='C')

    # Spacer
    pdf.ln(10)

    # User's Name
    pdf.set_font("Arial", 'B', 22)
    full_name = f"{first_name} {last_name}"
    pdf.cell(0, 10, full_name, ln=True, align='C')

    # Spacer
    pdf.ln(10)

    # Description
    pdf.set_font("Arial", '', 16)
    pdf.multi_cell(0, 10, "For outstanding participation and contribution.", align='C')

    # Spacer
    pdf.ln(20)

    # Level
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, f"User Level: {level}", ln=True, align='C')

    # Spacer
    pdf.ln(20)

    # Date
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, f"Awarded on {date}", ln=True, align='C')

    # Optional: Add signatures or logos
    # Example: Add a line for signature
    pdf.ln(30)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "__________________________", ln=True, align='C')
    pdf.cell(0, 5, "Signature", ln=True, align='C')

    # Save PDF to a BytesIO object
    pdf_buffer = BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)

    return pdf_buffer
