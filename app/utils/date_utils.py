from datetime import datetime,date

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Data no formato invalido. Utilize o formato yyyy-MM-dd.")

def format_date(date_obj):
    if isinstance(date_obj, date):
        return date_obj.strftime('%Y-%m-%d')
    return date_obj 
