from django.shortcuts import render
from .models import *
from . import services
from . import get_recent_vacancies


def index(request):
    main_page = MainPage.objects.first()

    return render(request, 'main/index.html', {'page_content': main_page})


def demand(request):
    salary_by_year_graph = services.check_or_create_dynamics_salary_by_years()
    num_by_year_graph = services.check_or_create_dynamics_number_vacancies_by_years()
    salary_by_year_vac_graph = services.check_or_create_dynamics_salary_by_years_selected_profession()
    num_by_year_vac_graph = services.check_or_create_dynamics_number_vacancies_by_years_selected_profession()

    return render(request, 'main/demand.html', {'table': services.create_demand_table(),
                                                'salary_by_year_graph': salary_by_year_graph,
                                                'num_by_year_graph': num_by_year_graph,
                                                'salary_by_year_vac_graph': salary_by_year_vac_graph,
                                                'num_by_year_vac_graph': num_by_year_vac_graph})


def geography(request):
    level_salaries_graph = services.check_or_create_level_salaries_by_area()
    share_vacancies_graph = services.check_or_create_share_vacancies_by_area()

    return render(request, 'main/geography.html', {'level_salaries_graph': level_salaries_graph,
                                                   'share_vacancies_graph': share_vacancies_graph,
                                                   'tables': services.create_geography_table()})


def skills(request):
    year_form = 2022
    if request.method == 'GET':
        year_request = request.GET.get('year')
        year_form = year_request if year_request is not None else year_form
    services.check_or_create_analysis_skill_statistics_by_years()
    skill_by_all_years = services.check_or_create_analysis_skill_statistics_by_all_years()

    years = YearAnalysisSkillStatistics.objects.all()
    return render(request, 'main/skills.html', {'table_by_all_year': services.create_skills_all_year_table(),
                                                'skill_by_all_years': skill_by_all_years,
                                                'table_by_year': services.create_skills_year_table(year_form),
                                                'year_form': YearAnalysisSkillStatistics.objects.get(year_statistics=year_form),
                                                'years': years})


def recent_vacancies(request):
    return render(request, 'main/recent_vacancies.html', {'vacancies': get_recent_vacancies.get_recent_vacancies()})