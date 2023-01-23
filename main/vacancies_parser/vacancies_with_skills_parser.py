import os

import pandas as pd
from main.models import VacanciesWithSkills


def create_df_skill_date(row: pd.Series, thin_df: pd.DataFrame) -> None:
    key_skills = row['key_skills'].split('\n')
    for skill in key_skills:
        thin_df.loc[len(thin_df.index)] = [skill, row['date']]


def create_vacancies_with_skills_bulk_from_csv(csv_file_name: str) -> None:
    pd.set_option('display.expand_frame_repr', False)
    df = pd.read_csv(os.path.join('main', 'vacancies_parser', 'csv_data', csv_file_name), low_memory=False)
    df = df.dropna(subset=['name', 'key_skills', 'published_at'])
    thin_df = pd.DataFrame(columns=['skill', 'date'])
    df = df[df['name'] == 'Специалист по информационной безопасности']
    df['date'] = df['published_at'].str[:7]
    df.apply(lambda row: create_df_skill_date(row, thin_df), axis=1)

    thin_df_records = thin_df.to_dict('records')

    model_instances = [VacanciesWithSkills(
        date=record['date'],
        skill=record['skill']
    ) for record in thin_df_records]

    VacanciesWithSkills.objects.bulk_create(model_instances)
