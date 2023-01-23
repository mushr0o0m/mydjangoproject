import os

import pandas as pd
from main.models import ExchangeRate


def create_exchange_rate_model_from_csv(csv_file_name: str) -> None:
    """
    Создаёт таблицу ExchangeRate из CSV-файла
    :param csv_file_name: название файла csv из  корня проекта
    :return: None
    """
    df = pd.read_csv(os.path.join('main', 'vacancies_parser', 'csv_data', csv_file_name))
    df_records = df.to_dict('records')
    model_instances = [ExchangeRate(
        date=record['date'],
        USD=record['USD'],
        KZT=record['KZT'],
        BYR=record['BYR'],
        UAH=record['UAH'],
        EUR=record['EUR'],
    ) for record in df_records]

    ExchangeRate.objects.bulk_create(model_instances)
