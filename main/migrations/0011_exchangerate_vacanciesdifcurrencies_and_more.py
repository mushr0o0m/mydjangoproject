# Generated by Django 4.1.5 on 2023-01-17 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_skillbyyear_year_statistics'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default='', max_length=7)),
                ('RUR', models.IntegerField()),
                ('USD', models.IntegerField()),
                ('KZT', models.IntegerField()),
                ('BYR', models.IntegerField()),
                ('UAH', models.IntegerField()),
                ('EUR', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='VacanciesDifCurrencies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100)),
                ('salary', models.CharField(default='', max_length=100)),
                ('area_name', models.CharField(default='', max_length=100)),
                ('date', models.CharField(default='', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='VacanciesWithSkills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(default='', max_length=7)),
                ('skill', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
