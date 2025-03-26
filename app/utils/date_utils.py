from datetime import datetime,date

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%d/%m/%Y').date()
    except ValueError:
        raise ValueError("Data no formato invalido. Utilize o formato dd/MM/yyyy.")

def format_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime('%d/%m/%Y')
    return date_obj 
