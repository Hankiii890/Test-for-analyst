# Скрипт загрузки и очистки данных
import pandas as pd 
import re 
from utils import normalize_colname_to_ym 


def load_data(prolongations_path, finansial_path):
    prolong = pd.read_csv(prolongations_path, dtype=str)
    financial = pd.read_csv(finansial_path, dtype=str)
    prolong.columns = prolong.columns.str.strip()
    financial.columns = financial.columns.str.strip()
    return prolong, financial


def normalize_financial(financial):
    """Переименовывает месячные колонки в формат YYYY-MM"""
    month_candidates = [c for c in financial.columns if re.search(r'20\\d{2}', str(c))]
    colmap = {c: normalize_colname_to_ym(c) for c in month_candidates}
    rename = {k:v for k,v in colmap.items() if v is not None}
    fin = financial.rename(columns=rename)
    month_cols = sorted([c for c in fin.columns if re.match(r'20\\d{2}-\\d{2}', str(c))])
    return fin, month_cols