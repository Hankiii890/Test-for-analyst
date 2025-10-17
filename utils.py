# вспомогательное 
import re 
import numpy as np 

months_ru = {
    'янв':1,'фев':2,'мар':3,'апр':4,'май':5,'мая':5,'июн':6,'июл':7,'авг':8,
    'сен':9,'окт':10,'ноя':11,'дек':12
    }


def normalize_colname_to_ym(colname):
    """Преобразует название столбца ('Январь 2023', '2023-01') -> 'YYYY-MM'"""
    s = str(colname).strip().lower()
    ym = re.search(r'20\\d{2}', s)
    if not ym:
        return None
    year = int(ym.group(0))
    mnum = re.search(r'\\b(0?[1-9]|1[0-2])\\b', s)
    if mnum:
        month = int(mnum.group(1))
        return f"{year}-{month:02d}"
    for k,v in months_ru.items():
        if k in s:
            return f"{year}-{v:02d}"
    return None


def parse_value_cell(v):
    """Парсит ячейку из financial_data.csv"""
    if v is None or v != v:  # NaN
        return np.nan
    s = str(v).strip().lower()
    if s in ('в ноль', 'вноль', '0', '0.0'):
        return 0.0
    if s in ('стоп', 'stop', 'end', 'энд'):
        return 'STOP'
    try:
        return float(s.replace(' ', '').replace(',', '.'))
    except Exception:
        return np.nan
