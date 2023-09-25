import datetime

class Enums:
    Hourly_Wage = 3
    English_Columns_Names = ['Name','Date','Start','End','Material']
    
    # directories
    Excel_File_Directory = "C:/Ali/GitHub/hourly_employees_automated_invoices/records.xlsx"
    PDF_Path = lambda name: f'C:/Ali/GitHub/hourly_employees_automated_invoices/pdf_files/{name}_{datetime.datetime.now().date()}_wage_invoice.pdf'
    Image_Directory = 'C:/Ali/GitHub/hourly_employees_automated_invoices/resources/background.png'
    Font_Path = 'C:/Ali/GitHub/hourly_employees_automated_invoices/resources/font.ttf'
