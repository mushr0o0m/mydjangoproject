from typing import List
from main.draw_graph import *
from django.core.exceptions import ValidationError
from django.db import models


class MainPage(models.Model):
    job_title = models.CharField(blank=False, max_length=100, default='Название профессии')
    job_description = models.TextField(blank=False, default='Описание профессии')
    thematic_img = models.ImageField(blank=False, default='', upload_to='img/')

    def __str__(self):
        return self.job_title

    def save(self, *args, **kwargs):
        if MainPage.objects.count() <= 1:
            super().save(*args, **kwargs)
        else:
            raise ValidationError('Нельзя добавить больше одной Main page')

    class Meta:
        verbose_name = 'Описание главной страницы'
        verbose_name_plural = 'Описания главной страницы'


class YearAnalysisSkillStatistics(models.Model):
    year_statistics = models.IntegerField('Год статистики', blank=False, default=1970)
    statistics_graph_skills_by_year_img = models.ImageField('График в формате изображения',
                                                            blank=True,
                                                            default='',
                                                            upload_to='img/statistics_graphs/')
    graphic_title = models.CharField('Название графика', blank=True, max_length=100, default='')

    def __str__(self):
        return str(self.year_statistics)

    class Meta:
        ordering = ('-year_statistics',)
        verbose_name = 'Год для выбора ТОП-10 навыков'
        verbose_name_plural = 'Годы для выбора ТОП-10 навыков'


class SkillByYear(models.Model):
    count = models.IntegerField('Количество повторений навыка за определенный год', blank=False)
    name_skill = models.CharField('Название навыка', blank=False, max_length=50)
    year_statistics = models.ForeignKey(YearAnalysisSkillStatistics, related_name='skills', on_delete=models.CASCADE,
                                        verbose_name='Год актуальности данных')

    def __str__(self):
        return f"Название навыка: {self.name_skill}, год актуальности данных: {self.year_statistics}"

    @staticmethod
    def update_or_create_vert_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = YearAnalysisSkillStatistics.objects.get(graphic_title=title)
            graph_file_name = draw_vert_bar_graph(
                [(i, str(item.name_skill), item.count)
                 for i, item in enumerate(SkillByYear.objects.filter(year_statistics=graph).order_by('count'))],
                graph.graphic_title)
            graph.statistics_graph_skills_by_year_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SkillByYear.update_or_create_vert_bar_graph([self.year_statistics.graphic_title])

    def delete(self, *args, **kwargs):
        graph_title = self.year_statistics.graphic_title
        super().delete(*args, **kwargs)
        SkillByYear.update_or_create_vert_bar_graph([graph_title])

    class Meta:
        ordering = ('-year_statistics',)
        verbose_name = 'Статистика по навыку за определенный год'
        verbose_name_plural = 'Статистики по навыкам за определенный год'


class StatisticsGraph(models.Model):
    statistic_graph_title = models.CharField('Название графика', blank=False, max_length=100, default='')
    statistic_graph_img = models.ImageField('График в формате изображения',
                                            blank=True,
                                            default='',
                                            upload_to='img/statistics_graphs/')

    def __str__(self):
        return self.statistic_graph_title

    class Meta:
        verbose_name = 'График статистики'
        verbose_name_plural = 'Графики статистики'


class SkillByAllYear(models.Model):
    count = models.IntegerField('Количество повторений навыка за все время', blank=False)
    name_skill = models.CharField('Название навыка', blank=False, max_length=50)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='skills_by_all_years',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Название навыка: {self.name_skill}, количество повторений навыка за все время: {self.count}"

    @staticmethod
    def update_or_create_vert_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_vert_bar_graph([(i, str(item.name_skill), item.count)
                                                   for i, item in enumerate(SkillByAllYear.objects.order_by('count'))],
                                                  graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SkillByAllYear.update_or_create_vert_bar_graph([self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        SkillByAllYear.update_or_create_vert_bar_graph([graph_title])

    class Meta:
        ordering = ('-count',)
        verbose_name = 'Ститистика по навыку за все время'
        verbose_name_plural = 'Ститистики по навыкам за все время'


class DynamicsSalaryByYears(models.Model):
    avg_salary = models.IntegerField('Cредняя ЗП', blank=False)
    year = models.IntegerField('Год', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='dynamics_salaries',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    @staticmethod
    def update_or_create_hor_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_hor_bar_graph([(i, str(item.year), item.avg_salary)
                                                  for i, item in
                                                  enumerate(DynamicsSalaryByYears.objects.order_by('year'))],
                                                 graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DynamicsSalaryByYears.update_or_create_hor_bar_graph([self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        DynamicsSalaryByYears.update_or_create_hor_bar_graph([graph_title])

    def __str__(self):
        return f"Год: {self.year}, средняя ЗП: {self.avg_salary}"

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Динамика уровня зарплат по годам'
        verbose_name_plural = 'Динамики уровня зарплат по годам'


class DynamicsNumberVacanciesByYears(models.Model):
    count = models.IntegerField('Количество вакансий за определенный год', blank=False)
    year = models.IntegerField('Год', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='dynamics_num_vacancies',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Год: {self.year}, количество вакансий: {self.count}"

    @staticmethod
    def update_or_create_hor_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_hor_bar_graph([(i, str(item.year), item.count)
                                                  for i, item in
                                                  enumerate(DynamicsNumberVacanciesByYears.objects.order_by('year'))],
                                                 graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DynamicsNumberVacanciesByYears.update_or_create_hor_bar_graph([self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        DynamicsNumberVacanciesByYears.update_or_create_hor_bar_graph([graph_title])

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Динамика количества вакансий по годам '
        verbose_name_plural = 'Динамики количества вакансий по годам'


class DynamicsSalaryByYearsSelectedProfession(models.Model):
    avg_salary = models.IntegerField('Средняя ЗП', blank=False)
    year = models.IntegerField('Год', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='dynamics_salaries_sp',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Год: {self.year}, средняя ЗП: {self.avg_salary}"

    @staticmethod
    def update_or_create_hor_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_hor_bar_graph([(i, str(item.year), item.avg_salary)
                                                  for i, item in enumerate(
                    DynamicsSalaryByYearsSelectedProfession.objects.order_by('year'))], graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DynamicsSalaryByYearsSelectedProfession.update_or_create_hor_bar_graph(
            [self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        DynamicsSalaryByYearsSelectedProfession.update_or_create_hor_bar_graph([graph_title])

    class Meta:
        ordering = ('-avg_salary',)
        verbose_name = 'Динамика уровня зарплат по годам для специалистов по информационной безопасности'
        verbose_name_plural = 'Динамики уровня зарплат по годам для специалистов по информационной безопасности'


class DynamicsNumberVacanciesByYearsSelectedProfession(models.Model):
    count = models.IntegerField('Количество вакансий за определенный год', blank=False)
    year = models.IntegerField('Год', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='dynamics_num_vacancies_sp',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Год: {self.year}, количество вакансий: {self.count}"

    @staticmethod
    def update_or_create_hor_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_hor_bar_graph([(i, str(item.year), item.count)
                                                  for i, item in enumerate(
                    DynamicsNumberVacanciesByYearsSelectedProfession.objects.order_by('year'))],
                                                 graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        DynamicsNumberVacanciesByYearsSelectedProfession.update_or_create_hor_bar_graph(
            [self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        DynamicsNumberVacanciesByYearsSelectedProfession.update_or_create_hor_bar_graph([graph_title])

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Динамика количества вакансий по годам для специалистов по информационной безопасности'
        verbose_name_plural = 'Динамики количества вакансий по годам для специалистов по информационной безопасности'


class LevelSalariesByArea(models.Model):
    area_name = models.CharField('Название города', blank=False, max_length=25, default='')
    avg = models.IntegerField('Средняя ЗП', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='level_salaries_by_area',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Название города: {self.area_name}, средняя ЗП: {self.avg}"

    @staticmethod
    def update_or_create_hor_bar_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_hor_bar_graph([(i, str(item.area_name), item.avg)
                                                  for i, item in
                                                  enumerate(LevelSalariesByArea.objects.order_by('-avg'))],
                                                 graph.statistic_graph_title)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        LevelSalariesByArea.update_or_create_hor_bar_graph([self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        LevelSalariesByArea.update_or_create_hor_bar_graph([graph_title])

    class Meta:
        ordering = ('-avg',)
        verbose_name = 'Уровень зарплат по городам'
        verbose_name_plural = 'Уровни зарплат по городам'


class ShareVacanciesByArea(models.Model):
    area_name = models.CharField('Название города', blank=False, max_length=25, default='')
    percent = models.FloatField('Процент', blank=False)
    statistics_graph = models.ForeignKey(StatisticsGraph,
                                         null=True,
                                         related_name='share_vacancies_by_area',
                                         on_delete=models.CASCADE,
                                         verbose_name='Название графика')

    def __str__(self):
        return f"Название города: {self.area_name}, процент: {self.percent}"

    @staticmethod
    def update_or_create_pie_graph(graph_titles: List[str]) -> None:
        for title in graph_titles:
            graph = StatisticsGraph.objects.get(statistic_graph_title=title)
            graph_file_name = draw_pie_graph(
                [(str(item.area_name), item.percent) for item in ShareVacanciesByArea.objects.order_by('percent')],
                graph.statistic_graph_title, ShareVacanciesByArea._meta.get_field('area_name').verbose_name)
            graph.statistic_graph_img = graph_file_name
            graph.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ShareVacanciesByArea.update_or_create_pie_graph([self.statistics_graph.statistic_graph_title])

    def delete(self, *args, **kwargs):
        graph_title = self.statistics_graph.statistic_graph_title
        super().delete(*args, **kwargs)
        ShareVacanciesByArea.update_or_create_pie_graph([graph_title])

    class Meta:
        ordering = ('-percent',)
        verbose_name = 'Доля вакансий по городам'
        verbose_name_plural = 'Доли вакансий по городам'


class ExchangeRate(models.Model):
    date = models.CharField(blank=False, max_length=7, default='')
    USD = models.FloatField(blank=False)
    KZT = models.FloatField(blank=False)
    BYR = models.FloatField(blank=False)
    UAH = models.FloatField(blank=False)
    EUR = models.FloatField(blank=False)


class VacanciesDifCurrencies(models.Model):
    name = models.CharField(blank=False, max_length=100, default='')
    salary = models.IntegerField(blank=False)
    area_name = models.CharField(blank=False, max_length=100, default='')
    date = models.CharField(blank=False, max_length=7, default='')


class VacanciesWithSkills(models.Model):
    date = models.CharField(blank=False, max_length=7, default='')
    skill = models.CharField(blank=False, max_length=100, default='')
