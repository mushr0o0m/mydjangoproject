from main.models import *
from .vacancies_parser.course_parser import create_exchange_rate_model_from_csv
from .vacancies_parser.vacancies_dif_currencies_parser import create_vacancies_dif_currencies_bulk_from_csv
from .vacancies_parser.vacancies_with_skills_parser import create_vacancies_with_skills_bulk_from_csv


def create_skills_all_year_table() -> [(str, int)]:
    skills_by_all_years = SkillByAllYear.objects.all()
    table = []
    for item in skills_by_all_years:
        name_skill = item.name_skill
        count = item.count
        table.append((name_skill, count))
    return table


def create_skills_year_table(year: int) -> [(str, int)]:
    year_statistic = YearAnalysisSkillStatistics.objects.get(year_statistics=year)
    skills_by_year = SkillByYear.objects.all()
    skills_filtered_by_year = skills_by_year.filter(year_statistics=year_statistic)
    table = []
    for item in skills_filtered_by_year:
        name_skill = item.name_skill
        count = item.count
        table.append((name_skill, count))
    return table


def create_demand_table() -> (int, str, str, str):
    salary_by_year = DynamicsSalaryByYears.objects.all()
    num_by_year = DynamicsNumberVacanciesByYears.objects.all()
    salary_by_year_vac = DynamicsSalaryByYearsSelectedProfession.objects.all()
    num_by_year_vac = \
        DynamicsNumberVacanciesByYearsSelectedProfession.objects.all()

    table = []

    for item in salary_by_year:
        year = item.year
        salary_by_year_row = item.avg_salary
        num_by_year_row = num_by_year.filter(year=year)
        salary_by_year_vac_row = salary_by_year_vac.filter(year=year)
        num_by_year_vac_row = num_by_year_vac.filter(year=year)
        table.append((year,
                      str(salary_by_year_row),
                      str(salary_by_year_vac_row[0].avg_salary) if len(salary_by_year_vac_row) == 1 else '-',
                      str(num_by_year_row[0].count),
                      str(num_by_year_vac_row[0].count) if len(num_by_year_vac_row) == 1 else '-'))
    return table


def create_geography_table() -> ([(str, int)], [(str, str)]):
    level_salaries_by_year = LevelSalariesByArea.objects.all()
    share_vacancies_by_area = ShareVacanciesByArea.objects.all()
    tables = ([], [])
    for item in level_salaries_by_year:
        city = item.area_name
        avg = item.avg
        tables[0].append((city, avg))
    for item in share_vacancies_by_area:
        city = item.area_name
        percent = str(round(item.percent * 100, 2)) + '%'
        tables[1].append((city, percent))
    return tables


def check_or_create_analysis_skill_statistics_by_years() -> None:
    years = YearAnalysisSkillStatistics.objects.all()
    if not (years.exists()):
        model_instances = [YearAnalysisSkillStatistics(
            year_statistics=year,
            graphic_title=f'ТОП-10 навыков за {year} для cпециалиста по информационной безопасности'
        ) for year in range(2015, 2023)]
        YearAnalysisSkillStatistics.objects.bulk_create(model_instances)
    skills_by_year = SkillByYear.objects.all()
    if not (skills_by_year.exists()):
        check_or_create_vacancies_with_skills()
        for year in years:
            skills = VacanciesWithSkills.objects.raw(f"""select
                            id, skill, count(skill) as count
                            from main_vacancieswithskills
                            where STRFTIME('%Y', date || '-01') like {year}
                            group by STRFTIME('%Y', date || '-01'), skill
                            order by count(skill) desc
                             limit 10""")
            model_instances = [SkillByYear(
                count=skill.count,
                name_skill=skill.skill,
                year_statistics=year
            ) for skill in skills]
            SkillByYear.objects.bulk_create(model_instances)
            SkillByYear.update_or_create_vert_bar_graph([year.graphic_title])


def check_or_create_analysis_skill_statistics_by_all_years() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='ТОП-10 навыков за все для cпециалиста по информационной безопасности')
    skills_by_all_years = SkillByAllYear.objects.all()
    if not (skills_by_all_years.exists()):
        check_or_create_vacancies_with_skills()
        skills = VacanciesWithSkills.objects.raw(f"""select
                            id, skill, count(skill) as count
                            from main_vacancieswithskills
                            group by skill
                            order by count(skill) desc
                             limit 10""")
        model_instances = [SkillByAllYear(
            count=skill.count,
            name_skill=skill.skill,
            statistics_graph=graph
        ) for skill in skills]
        SkillByAllYear.objects.bulk_create(model_instances)
        SkillByAllYear.update_or_create_vert_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_dynamics_salary_by_years() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Динамика уровня зарплат по годам')
    data = DynamicsSalaryByYears.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select 
                        id,
                        STRFTIME('%Y', date || '-01') AS 'year',
                        round(avg(salary)) as avg_salary 
                        from main_vacanciesdifcurrencies
                        group by year""")
        model_instances = [DynamicsSalaryByYears(
            avg_salary=vacancy.avg_salary,
            year=vacancy.year,
            statistics_graph=graph
        ) for vacancy in vacancies]
        DynamicsSalaryByYears.objects.bulk_create(model_instances)
        DynamicsSalaryByYears.update_or_create_hor_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_dynamics_number_vacancies_by_years() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Динамика количества вакансий по годам')
    data = DynamicsNumberVacanciesByYears.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select 
                            id,
                            STRFTIME('%Y', date || '-01') AS 'year',
                            count(salary) as count
                            from main_vacanciesdifcurrencies
                            group by year """)
        model_instances = [DynamicsNumberVacanciesByYears(
            count=vacancy.count,
            year=vacancy.year,
            statistics_graph=graph
        ) for vacancy in vacancies]
        DynamicsNumberVacanciesByYears.objects.bulk_create(model_instances)
        DynamicsNumberVacanciesByYears.update_or_create_hor_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_dynamics_salary_by_years_selected_profession() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Динамика уровня зарплат по годам для cпециалиста по информационной безопасности')
    data = DynamicsSalaryByYearsSelectedProfession.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vac_name = 'Специалист по информационной безопасности'
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select 
                            id,
                            STRFTIME('%Y', date || '-01') AS 'year',
                            round(avg(salary)) as avg_salary
                            from main_vacanciesdifcurrencies
                            where name like '%{vac_name}%'
                            group by year""")
        model_instances = [DynamicsSalaryByYearsSelectedProfession(
            avg_salary=vacancy.avg_salary,
            year=vacancy.year,
            statistics_graph=graph
        ) for vacancy in vacancies]
        DynamicsSalaryByYearsSelectedProfession.objects.bulk_create(model_instances)
        DynamicsSalaryByYearsSelectedProfession.update_or_create_hor_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_dynamics_number_vacancies_by_years_selected_profession() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Динамика количества вакансий по годам для cпециалиста по информационной безопасности')
    data = DynamicsNumberVacanciesByYearsSelectedProfession.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vac_name = 'Специалист по информационной безопасности'
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select 
                                id,
                                STRFTIME('%Y', date || '-01') AS 'year',
                                count(salary) as count
                                from main_vacanciesdifcurrencies
                                where name like '%{vac_name}%'
                                group by year""")
        model_instances = [DynamicsNumberVacanciesByYearsSelectedProfession(
            count=vacancy.count,
            year=vacancy.year,
            statistics_graph=graph
        ) for vacancy in vacancies]
        DynamicsNumberVacanciesByYearsSelectedProfession.objects.bulk_create(model_instances)
        DynamicsNumberVacanciesByYearsSelectedProfession.update_or_create_hor_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_level_salaries_by_area() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Уровень зарплат по городам (в порядке убывания)')
    data = LevelSalariesByArea.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select 
                                    area_name, avg, id from
                                    (select area_name, id, round(avg(salary)) as avg,
                                     count(salary) as count
                                    from main_vacanciesdifcurrencies
                                    group by area_name
                                    order by avg desc)
                                    where count > (select count(*) from main_vacanciesdifcurrencies) * 0.01
                                    limit 10""")
        model_instances = [LevelSalariesByArea(
            area_name=vacancy.area_name,
            avg=vacancy.avg,
            statistics_graph=graph
        ) for vacancy in vacancies]
        LevelSalariesByArea.objects.bulk_create(model_instances)
        LevelSalariesByArea.update_or_create_hor_bar_graph([graph.statistic_graph_title])
    return graph


def check_or_create_share_vacancies_by_area() -> StatisticsGraph:
    graph, created = StatisticsGraph.objects.get_or_create(
        statistic_graph_title='Доля вакансий по городам (в порядке убывания)')
    data = ShareVacanciesByArea.objects.all()
    if not (data.exists()):
        check_or_create_vacancies_dif_currencies()
        vacancies = VacanciesDifCurrencies.objects.raw(f"""select id,
                                        area_name,
                                        round(cast(count as real) / (select count(*) from main_vacanciesdifcurrencies), 4)
                                         as percent from
                                        (select id, area_name, count(salary) as count
                                        from main_vacanciesdifcurrencies
                                        group by area_name
                                        order by count desc)
                                        limit 10""")
        model_instances = [ShareVacanciesByArea(
            area_name=vacancy.area_name,
            percent=vacancy.percent,
            statistics_graph=graph
        ) for vacancy in vacancies]
        ShareVacanciesByArea.objects.bulk_create(model_instances)
        ShareVacanciesByArea.update_or_create_pie_graph([graph.statistic_graph_title])
    return graph


def check_or_create_vacancies_dif_currencies() -> None:
    all_currencies = ExchangeRate.objects.all()
    if not (all_currencies.exists()):
        create_exchange_rate_model_from_csv('currencies.csv')
    all_vacancies_dif_currencies = VacanciesDifCurrencies.objects.all()
    if not (all_vacancies_dif_currencies.exists()):
        create_vacancies_dif_currencies_bulk_from_csv('vacancies.csv')


def check_or_create_vacancies_with_skills() -> None:
    all_vacancies_with_skills = VacanciesWithSkills.objects.all()
    if not (all_vacancies_with_skills.exists()):
        create_vacancies_with_skills_bulk_from_csv('vacancies.csv')
