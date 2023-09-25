from process_excel import read_excel_file, get_all_teachers_names
from temp_invoice import create_invoice
from lookups import Enums

df = read_excel_file()
teachers = get_all_teachers_names(df)

for index, teacher in enumerate(teachers):
    create_invoice(df, teacher, Enums.PDF_Path(teacher))
    print(f'Done {index + 1}')
print('Done All')
