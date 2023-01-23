# Generated by Django 4.1.5 on 2023-01-18 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_skillbyallyear'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareVacanciesByArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(default='', max_length=25, verbose_name='Название города')),
                ('percent', models.FloatField(verbose_name='Процент')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='share_vacancies_by_area', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Доля вакансий по городам',
                'verbose_name_plural': 'Доли вакансий по городам',
                'ordering': ('percent',),
            },
        ),
        migrations.CreateModel(
            name='LevelSalariesByArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(default='', max_length=25, verbose_name='Название города')),
                ('avg', models.IntegerField(verbose_name='Средняя ЗП')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='level_salaries_by_area', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Уровень зарплат по городам',
                'verbose_name_plural': 'Уровни зарплат по городам',
                'ordering': ('avg',),
            },
        ),
        migrations.CreateModel(
            name='DynamicsSalaryByYearsSelectedProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_salary', models.IntegerField(verbose_name='Средняя ЗП')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamics_salaries_sp', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Динамика уровня зарплат по годам для специалистов по информационной безопасности',
                'verbose_name_plural': 'Динамики уровня зарплат по годам для специалистов по информационной безопасности',
                'ordering': ('-avg_salary',),
            },
        ),
        migrations.CreateModel(
            name='DynamicsSalaryByYears',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avg_salary', models.IntegerField(verbose_name='Cредняя ЗП')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamics_salaries', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Динамика уровня зарплат по годам',
                'verbose_name_plural': 'Динамики уровня зарплат по годам',
                'ordering': ('-year',),
            },
        ),
        migrations.CreateModel(
            name='DynamicsNumberVacanciesByYearsSelectedProfession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество вакансий за определенный год')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamics_num_vacancies_sp', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Динамика количества вакансий по годам для специалистов по информационной безопасности',
                'verbose_name_plural': 'Динамики количества вакансий по годам для специалистов по информационной безопасности',
                'ordering': ('-year',),
            },
        ),
        migrations.CreateModel(
            name='DynamicsNumberVacanciesByYears',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(verbose_name='Количество вакансий за определенный год')),
                ('year', models.IntegerField(verbose_name='Год')),
                ('statistics_graph', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='dynamics_num_vacancies', to='main.statisticsgraph', verbose_name='Название графика')),
            ],
            options={
                'verbose_name': 'Динамика количества вакансий по годам ',
                'verbose_name_plural': 'Динамики количества вакансий по годам',
                'ordering': ('-year',),
            },
        ),
    ]
