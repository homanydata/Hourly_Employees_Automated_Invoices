from process_excel import read_excel_file, get_all_teachers_names
from temp_invoice import create_invoice

def generate():
    try:
        df = read_excel_file()
        teachers = get_all_teachers_names(df)
        result = create_invoice(df, teachers)

    except Exception as e:
        result = str(e)
    finally:
        return result