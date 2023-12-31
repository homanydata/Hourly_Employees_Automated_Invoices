import pandas as pd
from lookups import Enums, Errors
import datetime
import os

def read_excel_file():
    path = Enums.Excel_File_Directory()
    if not os.path.exists(path=path):
        df = pd.DataFrame()
        df.to_excel(path, index=False)
        raise Exception(Errors.Empty_Excel_File)
    
    df = pd.read_excel(path)
    
    if df.empty:
        raise Exception(Errors.Empty_Excel_File)
    
    columns = df.columns
    df = df.rename(columns={col:new_col for col, new_col in zip(columns, Enums.English_Columns_Names)})
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df['Start'] = pd.to_datetime(df['Start'], format='%H:%M:%S').dt.time
    df['End'] = pd.to_datetime(df['End'], format='%H:%M:%S').dt.time
    
    # filter on this month
    df = df[(df['Date'].dt.month == datetime.datetime.now().month) & (df['Date'].dt.year == datetime.datetime.now().year)]

    # add duration column
    df['Duration'] = (pd.to_datetime(df['End'].astype(str), format='%H:%M:%S') - 
                    pd.to_datetime(df['Start'].astype(str), format='%H:%M:%S')).dt.total_seconds() // 60
    print(df)
    return df

def get_all_teachers_names(df:pd.DataFrame):
    return df.Name.unique()

def get_teachers_totals(df:pd.DataFrame, teacher:str):
    teacher_df = df[df.Name == teacher]
    grouped_df = teacher_df[['Material','Duration']].groupby('Material').sum().reset_index()
    grouped_df = grouped_df.rename(columns={'Duration':'Total Duration'})
    grouped_df['Total Hours'] = grouped_df['Total Duration']//45
    return grouped_df

def calculate_total_hours_wage(df):
    total_hours = df['Total Hours'].sum()
    total_wage = int(total_hours * Enums.Hourly_Wage)
    return total_hours, total_wage

def get_summary_as_text(df):
    text_lines = []

    for index, row in df.iterrows():
        # extract the values from the first and second columns
        col1_value = row[df.columns[0]]
        col2_value = str(int(row[df.columns[2]]))

        # create a text line in the desired format and add it to the list
        text_line = col1_value + " "*(33 - len(col1_value) - len(col2_value)) + col2_value + " حصة"
        text_lines.append(text_line)

    return text_lines

def get_month_summary():
    try:
        df = read_excel_file()
    except:
        return Errors.Empty_Excel_File
    summary = df[['Name','Material','Duration']].groupby(['Name','Material']).sum().reset_index()
    summary = summary.rename(columns={'Name':'المدرّس','Material':'المادة','Duration':'عدد الحصص'})
    summary_excel_dir = Enums.Month_Summary_Excel()
    summary.to_excel(summary_excel_dir, index=False)
    return "Summary Saved as Excel"

def insert_record(values:dict):
    try:
        date = datetime.date(year=values['Year'],month=values['Month'],day=values['Day'])
    except:
        return Errors.Invalid_Date
    try:
        start = datetime.time(hour=values['Start-Hour'],minute=values['Start-Min'])
    except Exception as e:
        print(str(e))
        return Errors.Invalid_Start_Time
    try:
        end = datetime.time(hour=values['End-Hour'],minute=values['End-Min'])
        if end <= start: raise Exception()
    except:
        return Errors.Invalid_End_Time
    
    name = values['Name']
    material = values['Material']
    
    if not name or not material:
        return Errors.Missing_Data

    new_record = {'الاسم':name, 'التاريخ':date, 'بداية الحصة':start, 'نهاية الحصة':end, 'المادة':material}
    
    EXCEL_FILE = Enums.Excel_File_Directory()
    # Load the data if the file exists, if not, create a new DataFrame
    if EXCEL_FILE.exists():
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame()
    try:
        new_record = pd.DataFrame(new_record, index=[0])
        df = pd.concat([df, new_record], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
    except PermissionError:
        return Errors.Excel_File_Opened
    except Exception as e:
        return str(e)
    return Errors.Data_Saved
