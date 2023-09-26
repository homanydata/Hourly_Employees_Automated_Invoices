# from pathlib import Path
import datetime
import PySimpleGUI as sg
import pandas as pd
from process_excel import insert_record
from generate_invoices import generate

# Add some color to the window
sg.theme('DarkTeal9')

hour_list = [i for i in range(0, 24)]
minute_list = [i for i in range(0, 60)]
day_list = [i for i in range(1, 32)]
month_list = [i for i in range(1, 13)]
year_list = [i for i in range(2023, 2100)]

today = datetime.datetime.now()
this_year, this_month, this_day = today.year, today.month, today.day

time_default_dict = {'Hour':10, 'Min':30, 'Year':this_year, 'Month':this_month, 'Day':this_day}
time_layout = [
        [
        sg.Spin(minute_list, initial_value=30, key='Start-Min', s=3),
        sg.Text(':', justification='right'),
        sg.Spin(hour_list, initial_value=10, key='Start-Hour', s=3),
        sg.Text(text=':بداية الحصة', justification='right')
        ],
        [
        sg.Spin(minute_list, initial_value=30, key='End-Min', s=3),
        sg.Text(':', justification='right'),
        sg.Spin(hour_list, initial_value=11, key='End-Hour', s=3),
        sg.Text(':انتهاء الحصة', justification='right')
        ]
    ]
date_layout = [
        [sg.Text(':التاريخ', justification='right')],
        [sg.Spin(year_list, initial_value=this_year, key='Year'), sg.Text(f':السنة', justification='right'),
        sg.Spin(month_list, initial_value=this_month, key='Month'), sg.Text(':الشهر', justification='right'),
        sg.Spin(day_list, initial_value=this_day, key='Day'), sg.Text(':اليوم', justification='right')
        ]
    ]
intro_layout = [
        [sg.Text(':رجاء ادخل المعلومات التالية لتسجيل حصة', justification='right')],
        [sg.InputText(key='Name', justification='right'), sg.Text(':الاسم', justification='right')],
        [sg.InputText(key='Material', justification='right'), sg.Text(':المادة', justification='right')]
    ]
layout = [
    [sg.Column(intro_layout, element_justification='right', expand_x=True)],
    [sg.Column(date_layout, element_justification='right', expand_x=True)],
    [sg.Column(time_layout, element_justification='right', expand_x=True)],
    [sg.Submit(), sg.Button('Clear'), sg.Button('اعداد الايصالات'), sg.Exit()]
]

window = sg.Window('Simple data entry form', layout)

def clear_input():
    for key in values:
        if key == 'End-Hour':
            window[key](11)
        elif key.split('-')[0] in ['Start','End']:
            window[key](time_default_dict[key.split('-')[1]])
        elif key in ['Year','Month','Day']:
            window[key](time_default_dict[key])
        else:
            window[key]('')
    return None

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Clear':
        clear_input()
    if event == 'Submit':
        result = insert_record(values)
        sg.popup(result)
        clear_input()
    if event == 'Generate':
        clear_input()
        result = generate()
        sg.popup(result)
window.close()
