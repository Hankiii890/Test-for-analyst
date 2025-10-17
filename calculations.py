# расчет коэффициентов и ПРОЛОНГАЦИИ 
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calc_for_month(df, target_month, month_cols):
    """Вычисляет коэффициенты пролонгации за конкретный месяц"""
    dt = datetime.strptime(target_month, "%Y-%m")
    m_prev = (dt - relativedelta(months=1)).strftime('%Y-%m')
    m_prev2 = (dt - relativedelta(months=2)).strftime('%Y-%m')

    # --- 1-й месяц ---
    df_prev = df[df['last_month'] == m_prev].copy()
    if df_prev.empty:
        return {'month': target_month, 'first_coef': np.nan, 'second_coef': np.nan}

    df_prev['base_first'] = df_prev[m_prev]
    df_prev['num_first'] = df_prev[target_month]
    sum_base_first = df_prev['base_first'].sum()
    sum_num_first = df_prev['num_first'].sum()
    k1 = sum_num_first / sum_base_first if sum_base_first > 0 else np.nan

    # --- 2-й месяц ---
    df_prev2 = df[df['last_month'] == m_prev2].copy()
    if not df_prev2.empty:
        df_prev2 = df_prev2[df_prev2[m_prev] == 0]
        df_prev2['base_second'] = df_prev2[m_prev2]
        df_prev2['num_second'] = df_prev2[target_month]
        sum_base_second = df_prev2['base_second'].sum()
        sum_num_second = df_prev2['num_second'].sum()
        k2 = sum_num_second / sum_base_second if sum_base_second > 0 else np.nan
    else:
        k2 = np.nan

    return {
        'month': target_month,
        'first_coef': round(k1,4) if k1==k1 else np.nan,
        'second_coef': round(k2,4) if k2==k2 else np.nan
    }


def calc_all(num, months_year, managers, month_cols):
    # Если колонка manager отсутствует, но есть AM или Account — переименовать
    if 'manager' not in num.columns:
        if 'AM' in num.columns:
            num = num.rename(columns={'AM': 'manager'})
        elif 'Account' in num.columns:
            num = num.rename(columns={'Account': 'manager'})
        else:
            num['manager'] = 'Не указан'

    rows = []
    for mgr in managers:
        sub = num[num['manager'] == mgr] if mgr != 'ОТДЕЛ_В_ЦЕЛОМ' else num
        for m in months_year:
            r = calc_for_month(sub, m, month_cols)
            r['manager'] = mgr
            rows.append(r)
    return pd.DataFrame(rows)