import datetime
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from process_excel import calculate_total_hours_wage, get_teachers_totals, get_summary_as_text
from lookups import Enums, Errors

def create_invoice(df, names):
    # create pdf
    c = canvas.Canvas(Enums.PDF_Path(), pagesize=landscape(A5))
    
    for index, name in enumerate(names):
        teacher_df = get_teachers_totals(df=df, teacher=name)
        total_hours, total_wage = calculate_total_hours_wage(teacher_df)

        background_image = Enums.Image_Directory()
        image = utils.ImageReader(background_image)
        c.drawImage(image, 0, 0, width=landscape(A5)[0], height=landscape(A5)[1], preserveAspectRatio=True)

        # set arabic font
        arabic_font_path = Enums.Font_Path()
        pdfmetrics.registerFont(TTFont("Arabic", arabic_font_path))

        # set indentation
        indentation = 350

        # add date
        today = str(datetime.datetime.now().date())
        c.setFont('Helvetica', 13)
        c.drawString(indentation + 90, 54, today)

        # teacher sessions summary
        for index, line in enumerate(get_summary_as_text(teacher_df)):
            c.setFont("Arabic", 12)
            reshaped_text = arabic_reshaper.reshape(line)
            bidi_text = get_display(reshaped_text)
            c.drawString(indentation + 5, 240-20*index, bidi_text)
        
        # total amount
        c.setFont("Arabic", 12)
        c.drawString(indentation + 20, 130, str(total_hours))
        
        # teacher name
        c.setFont("Arabic", 12)
        reshaped_text = arabic_reshaper.reshape(name)
        bidi_text = get_display(reshaped_text)
        c.drawString(indentation - len(name)*2, 318, bidi_text)

        # total amount
        c.setFont("Arabic", 14)
        c.drawString(indentation - 10, 85, f'{total_wage:,}')
        
        # new page for another teacher
        if index != len(names) - 1:
            c.showPage()
    try:
        c.save()
    except PermissionError:
        return Errors.PDF_File_Opened
    return 'All invoices are created successfully'
