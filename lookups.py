import datetime
from pathlib import Path
import os

class Enums:
    Hourly_Wage = 300000
    English_Columns_Names = ['Name','Date','Start','End','Material']
    
    # directories
    def Excel_File_Directory():
        current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        directory = current_dir / 'records.xlsx'
        return directory
    
    def Month_Summary_Excel():
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        directory = current_dir / f'{month}-{year}_summary_excel.xlsx'
        return directory
    
    def PDF_Path():
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        current_directory = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        folder_dir = str(current_directory) + '/pdf_files'
        
        if not os.path.exists(folder_dir):
            os.makedirs(folder_dir)
        
        directory = str(folder_dir) + f'/invoices_{month}_{year}.pdf'
        return directory
    
    def Image_Directory():
        current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        directory = current_dir / 'resources/background.png'
        return directory
    
    def Font_Path():
        current_dir = Path(__file__).parent if '__file__' in locals() else Path.cwd()
        directory = current_dir / 'resources/font.ttf'
        return directory
    
class Errors:
    Sorry = lambda e:f"Sorry, the following error happened: {e}"
    Data_Saved = 'Data saved!'
    Invalid_Date = 'Sorry, the date you entered is invalid'
    Invalid_Start_Time = 'Sorry, the start time you entered is invalid'
    Invalid_End_Time = 'Sorry, the end time you entered is invalid'
    Missing_Data = "Please make sure to fill all data needed before submitting"
    Excel_File_Opened = 'Please you need to close the excel file before submitting'
    PDF_File_Opened = 'Please you need to close the pdf file before submitting'
    Empty_Excel_File = 'The Excel File is Empty!'