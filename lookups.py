import datetime
from pathlib import Path

class Enums:
    Hourly_Wage = 3
    English_Columns_Names = ['Name','Date','Start','End','Material']
    
    # directories
    def Excel_File_Directory():
        current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        directory = current_dir / 'records.xlsx'
        return directory
    PDF_Path = lambda name: f'C:/Ali/Github/hourly_employees_automated_invoices/pdf_files/{name}_{datetime.datetime.now().date()}_wage_invoice.pdf'
    Image_Directory = 'C:/Ali/Github/hourly_employees_automated_invoices/resources/background.png'
    Font_Path = 'C:/Ali/Github/hourly_employees_automated_invoices/resources/font.ttf'
class Errors:
    Sorry = lambda e:f"Sorry, the following error happened: {e}"