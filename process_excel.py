import pandas as pd
from lookups import Enums

def read_excel_file():
    df = pd.read_excel(Enums.Excel_File_Directory)
    columns = df.columns
    df = df.rename(columns={col:new_col for col, new_col in zip(columns, Enums.English_Columns_Names)})
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df['Start'] = pd.to_datetime(df['Start'], format='%H:%M:%S').dt.time
    df['End'] = pd.to_datetime(df['End'], format='%H:%M:%S').dt.time
    # add duration column
    df['Duration'] = (pd.to_datetime(df['End'].astype(str), format='%H:%M:%S') - 
                    pd.to_datetime(df['Start'].astype(str), format='%H:%M:%S')).dt.total_seconds() // 60
    return df

def get_all_teachers_names(df:pd.DataFrame):
    return df.Name.unique()

def get_teachers_totals(df:pd.DataFrame, teacher:str):
    teacher_df = df[df.Name == teacher]
    grouped_df = teacher_df[['Material','Duration']].groupby('Material').sum().reset_index()
    grouped_df = grouped_df.rename(columns={'Duration':'Total Duration'})
    grouped_df['Total Hours'] = grouped_df['Total Duration']//30 / 2
    return grouped_df

def calculate_total_hours_wage(df):
    total_hours = df['Total Hours'].sum()
    total_wage = total_hours * Enums.Hourly_Wage
    return total_hours, total_wage

def get_summary_as_text(df):
    text_lines = []

    for index, row in df.iterrows():
        # extract the values from the first and second columns
        col1_value = row[df.columns[0]]
        col2_value = str(int(row[df.columns[1]]))

        # create a text line in the desired format and add it to the list
        text_line = col1_value + " "*(33 - len(col1_value) - len(col2_value)) + col2_value + " دقيقة"
        text_lines.append(text_line)

    return text_lines