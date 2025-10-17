# Сборка проекта


import argparse
from data_loader import load_data, normalize_financial
from preprocessing import merge_data, prepare_numeric
from calculations import calc_all
from report_generation import save_excel, plot_overall

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prolongations', required=True)
    parser.add_argument('--financial', required=True)
    parser.add_argument('--out', default='report.xlsx')
    parser.add_argument('--year', type=int, default=2023)
    args = parser.parse_args()

    prolong, financial = load_data(args.prolongations, args.financial)
    fin, month_cols = normalize_financial(financial)

    df = merge_data(prolong, fin)
    df['manager'] = df['AM'].fillna(df.get('Account', 'Не указан'))
    df['last_month'] = df['month'].apply(lambda x: x if isinstance(x,str) and '-' in x else None)

    num = prepare_numeric(df, month_cols)

    months_year = [m for m in month_cols if str(args.year) in m]
    managers = sorted(num['manager'].dropna().unique().tolist())
    managers.append('ОТДЕЛ_В_ЦЕЛОМ')

    monthly_df = calc_all(num, months_year, managers, month_cols)

    yearly_df = (monthly_df
                 .groupby('manager', as_index=False)
                 .agg({'first_coef':'mean','second_coef':'mean'})
                 .rename(columns={'first_coef':'avg_K1','second_coef':'avg_K2'}))

    save_excel(monthly_df, yearly_df, df, month_cols, args.out)
    plot_overall(monthly_df, args.year)

    print("monthly_df preview:")    
    print(monthly_df.head())


if __name__ == '__main__':
    main()
