# фильтрация и нормализация данных 

import pandas as pd
import numpy as np
from utils import parse_value_cell

def merge_data(prolong, fin):
    prolong['id'] = prolong['id'].astype(str).str.strip()
    fin['id'] = fin['id'].astype(str).str.strip()
    df = pd.merge(prolong[['id','month','AM']], fin, on='id', how='left')
    return df


def prepare_numeric(df, month_cols):
    """Создаёт числовую таблицу отгрузок по проектам"""
    num = df[['id','manager','last_month']].set_index('id').copy()
    for c in month_cols:
        num[c] = df.set_index('id')[c].apply(parse_value_cell)
    # Убираем STOP и NaN → 0
    for c in month_cols:
        num[c] = num[c].replace('STOP', np.nan)
    num[month_cols] = num[month_cols].apply(pd.to_numeric, errors='coerce').fillna(0.0)
    return num