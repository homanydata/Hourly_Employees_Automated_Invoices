import datetime
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib import utils
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display
from process_excel import calculate_total_hours_wage, get_teachers_totals, get_summary_as_text
from lookups import Enums

def create_invoice(df, name, path):
    teacher_df = get_teachers_totals(df=df, teacher=name)
    total_hours, total_wage = calculate_total_hours_wage(teacher_df)

    # create pdf
    c = canvas.Canvas(path, pagesize=landscape(A5))
    background_image = Enums.Image_Directory
    image = utils.ImageReader(background_image)
    c.drawImage(image, 0, 0, width=landscape(A5)[0], height=landscape(A5)[1], preserveAspectRatio=True)

    # set arabic font
    arabic_font_path = Enums.Font_Path
    pdfmetrics.registerFont(TTFont("Arabic", arabic_font_path))

    # set indentation
    indentation = 350

    # add date
    today = str(datetime.datetime.now().date())
    c.setFont('Helvetica', 13)
    c.drawString(indentation + 85, 304, today)

    # teacher sessions summary
    for index, line in enumerate(get_summary_as_text(teacher_df)):
        c.setFont("Arabic", 12)
        reshaped_text = arabic_reshaper.reshape(line)
        bidi_text = get_display(reshaped_text)
        c.drawString(indentation + 5, 230-20*index, bidi_text)
    
    # total amount
    c.setFont("Arabic", 12)
    c.drawString(indentation + 20, 120, str(total_hours))
    
    # teacher name
    c.setFont("Arabic", 12)
    reshaped_text = arabic_reshaper.reshape(name)
    bidi_text = get_display(reshaped_text)
    c.drawString(indentation - len(bidi_text)*6, 75, bidi_text)

    # total amount
    c.setFont("Arabic", 12)
    c.drawString(indentation + 100, 52, str(total_wage))

    c.save()
