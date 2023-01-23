import os
import pandas as pd
from main.models import VacanciesDifCurrencies
from django.db import connection


def apply_to_currency(row: pd.Series) -> int or None:
    if row['salary_currency'] == 'RUR':
        return round(row['salary'])
    with connection.cursor() as cur:
        cur.execute(f"""SELECT * FROM main_exchangerate WHERE date = '{row['date']}'""")
        valutes = dict(zip([col[0] for col in cur.description], cur.fetchone()))
        if row['salary_currency'] not in valutes or valutes[row['salary_currency']] is None:
            return None
    return round(row['salary'] * valutes[row['salary_currency']])


def create_vacancies_dif_currencies_bulk_from_csv(csv_file_name: str) -> None:
    df = pd.read_csv(os.path.join('main', 'vacancies_parser', 'csv_data', csv_file_name), low_memory=False)
    df = df.dropna(subset=['name', 'salary_currency', 'area_name', 'published_at']) \
        .dropna(subset=['salary_from', 'salary_to'], how='all').reset_index(drop=True)
    df = df[['name', 'salary_currency', 'area_name', 'published_at', 'salary_from', 'salary_to']]
    df['date'] = df['published_at'].str[:7]
    df['salary'] = df[['salary_from', 'salary_to']].mean(axis=1)
    df['salary'] = df.apply(axis=1, func=apply_to_currency)
    df = df[['name', 'salary', 'area_name', 'date']].dropna()
    df_records = df.to_dict('records')

    model_instances = [VacanciesDifCurrencies(
        name=record['name'],
        salary=record['salary'],
        area_name=record['area_name'],
        date=record['date'],
    ) for record in df_records]

    VacanciesDifCurrencies.objects.bulk_create(model_instances)
