from reportlab.lib.pagesizes import A5, landscape
from reportlab.pdfgen import canvas
from process_excel import calculate_total_wage, get_employees_totals, get_summary_as_text

def create_invoice(df, name, path):
    employee_df = get_employees_totals(df=df, employee=name)
    total = calculate_total_wage(employee_df)

    # Create a PDF document
    c = canvas.Canvas(path, pagesize=landscape(A5))

    # Invoice title
    c.setFont("Helvetica-Bold", 24)
    c.drawString(250, 350, "Invoice")

    # Set school name (sample) in the top right corner
    school_name = "ABC School"
    c.setFont("Helvetica", 12)
    c.drawString(50, 300, f"School: {school_name}")

    # teacher sessions summary
    c.setFont("Helvetica", 12)
    c.drawString(50, 285, f"Teacher {name} Sessions Summary:")
    for index, line in enumerate(get_summary_as_text(employee_df)):
        c.setFont("Helvetica", 8)
        c.drawString(50, 260-15*index, line)
        c.line(50, 260 - 15*index - 3, 150, 260 - 15 * index - 3)

    # Teacher name
    c.setFont("Helvetica", 12)
    c.drawString(80, 100, f"Teacher: {name}")

    # Total amount
    c.drawString(200, 100, f"Total Wage: ${total}")

    # Box around teacher name and total
    c.rect(50, 80, 450, 50)  # Adjust the dimensions as needed

    # Thank you message
    c.setFont("Helvetica", 12)
    c.drawString(50, 150, "Thank you for your hard work and dedication!")

    # Signature line
    c.setFont("Helvetica", 12)
    c.drawString(400, 50, "Signature:")
    c.line(470, 50, 570, 50)  # Line for signature

    # Save the PDF
    c.save()
