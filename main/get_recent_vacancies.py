from datetime import datetime
from typing import List, Dict, Any
import requests
import concurrent.futures

url = "https://api.hh.ru/vacancies"


def execute_vacancies(vacancies: List[Dict[str, str]] or List[Dict[Dict[str, str], str]]) -> Dict[str, Dict[str, Any]]:
    return dict([
        (
            vacancy["id"],
            {'name': vacancy["name"],
             'area_name': vacancy["area"]["name"],
             'salary': round((vacancy["salary"]["from"] if vacancy["salary"]["from"] else vacancy["salary"]["to"] +
                             vacancy["salary"]["to"] if vacancy["salary"]["to"] else vacancy["salary"]["from"]) / 2),
             'salary_currency': 'руб.' if vacancy["salary"]["currency"] is None or vacancy["salary"]["currency"] == 'RUR'
                else vacancy["salary"]["currency"],
             'salary_gross': 'до вычета налогов' if vacancy["salary"]["gross"] else 'после вычета налогов',
             'employer_name': vacancy["employer"]["name"],
             'published_at': datetime.strptime(vacancy["published_at"], '%Y-%m-%dT%H:%M:%S%z')}
        )
        for vacancy in vacancies
        if vacancy["salary"]
    ])


def execute_detail_info(vacancies: List[Dict[str, str]] or List[Dict[Dict[str, str], str]]):
    return vacancies["id"], {'description': vacancies["description"],
                             'key_skills': ', '.join([item['name'] for item in vacancies['key_skills']])}


def get_vacancies_items(params: dict) -> (List[Dict[str, str]] or List[Dict[Dict[str, str], str]]):
    _request = requests.get(url, params).json()
    return [] if not ('items' in _request) else _request["items"]


def get_vacancies_detail_info(param: str) -> (List[Dict[str, str]] or List[Dict[Dict[str, str], str]]):
    return requests.get(url + '/' + param).json()


def get_recent_vacancies() -> Dict[str, Dict[str, Any]]:
    params1 = [dict(
        specialization=1,
        date_from="2022-12-26T00:00:00",
        date_to="2022-12-26T12:00:00",
        text="Специалист по информационной безопасности OR безопасность OR защита OR information security specialist OR information security OR фахівець служби безпеки OR cyber security",
        search_field="name",
        per_page=15,
        page=0,
    )]

    params2 = [dict(
        specialization=1,
        date_from="2022-12-26T00:12:00",
        date_to="2022-12-27T00:00:00",
        text="Специалист по информационной безопасности OR безопасность OR защита OR information security specialist OR information security OR фахівець служби безпеки OR cyber security",
        search_field="name",
        per_page=15,
        page=0,
    )]

    with concurrent.futures.ProcessPoolExecutor() as executor:
        result = list(executor.map(get_vacancies_items, params1 + params2))
        response_first, response_sec = executor.map(execute_vacancies, result)
        response = {**response_first, **response_sec}
        vacancies_id = [item for item in response.keys()]
        result_detail_info = list(executor.map(get_vacancies_detail_info, vacancies_id))
        response_detail_info = dict(executor.map(execute_detail_info, result_detail_info))
        return dict([(item[0], {**item[1], **response_detail_info[item[0]]}) for item in response.items()])


