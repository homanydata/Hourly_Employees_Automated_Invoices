import pandas as pd
from lookups import Enums
import time

def read_excel_file():
    df = pd.read_excel(Enums.Excel_File_Directory)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y', errors='coerce')
    df['Start'] = pd.to_datetime(df['Start'], format='%H:%M:%S').dt.time
    df['End'] = pd.to_datetime(df['End'], format='%H:%M:%S').dt.time
    # add duration column
    df['Duration'] = (pd.to_datetime(df['End'].astype(str), format='%H:%M:%S') - 
                    pd.to_datetime(df['Start'].astype(str), format='%H:%M:%S')).dt.total_seconds() // 60
    return df

def get_all_employees_names(df:pd.DataFrame):
    return df['Name'].to_list()

def get_employees_totals(df:pd.DataFrame, employee:str):
    employee_df = df[df.Name == employee]
    grouped_df = employee_df[['Material','Duration']].groupby('Material').sum().reset_index()
    grouped_df = grouped_df.rename(columns={'Duration':'Total Duration'})
    grouped_df['Total Hours'] = grouped_df['Total Duration']//30 / 2
    return grouped_df

def calculate_total_wage(df):
    total_hours = df['Total Hours'].sum()
    total_wage = total_hours * Enums.Hourly_Wage
    return total_wage

def get_summary_as_text(df):
    # Create an empty list to store the text lines
    text_lines = []

    # Iterate through the DataFrame rows
    for index, row in df.iterrows():
        # Extract the values from the first and second columns
        col1_value = row[df.columns[0]]
        col2_value = row[df.columns[1]]

        # Create a text line in the desired format and add it to the list
        text_line = f"{col1_value.capitalize()}: {int(col2_value)} mins"
        text_lines.append(text_line)

    return text_lines