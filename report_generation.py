# Генерация готового отчета с графиком !!! 
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def save_excel(monthly_df, yearly_df, df_raw, month_cols, out_path):
    with pd.ExcelWriter(out_path, engine='openpyxl') as writer:
        df_raw[['id','manager','last_month'] + month_cols].to_excel(writer, sheet_name='raw_data', index=False)
        monthly_df.to_excel(writer, sheet_name='monthly_by_manager', index=False)
        yearly_df.to_excel(writer, sheet_name='yearly_by_manager', index=False)
    print(f"Отчёт сохранён: {out_path}")


def plot_overall(monthly_df, year):
    plots_dir = Path('plots'); plots_dir.mkdir(exist_ok=True)
    overall = monthly_df[monthly_df['manager']=='ОТДЕЛ_В_ЦЕЛОМ']
    plt.figure(figsize=(10,5))
    plt.plot(overall['month'], overall['first_coef'], label='K1')
    plt.plot(overall['month'], overall['second_coef'], label='K2')
    plt.title(f'Коэффициенты пролонгации отдела ({year})')
    plt.legend(); plt.grid(True); plt.xticks(rotation=45)
    plt.tight_layout(); plt.savefig(plots_dir / f'overall_{year}.png')
