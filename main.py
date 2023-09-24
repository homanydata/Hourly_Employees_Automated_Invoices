from process_excel import read_excel_file, get_all_employees_names
from temp_invoice import create_invoice
from lookups import Enums

df = read_excel_file()
employees = get_all_employees_names(df)

for employee in employees:
    create_invoice(df, employee, Enums.PDF_Path(employee))

print('Done')