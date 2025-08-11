from fpdf import FPDF
import os
def export_pdf_report(summary_text, output_path=None):
    if output_path is None:
        output_path = os.path.join('/tmp','Finance_Summary.pdf') if os.name != 'nt' else 'Finance_Summary.pdf'
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', size=12)
    # split long text into lines
    for line in summary_text.split('\n'):
        pdf.multi_cell(0, 8, line)
    pdf.output(output_path)
    return output_path
