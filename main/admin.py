from django.contrib import admin
from main.models import *
from django.contrib import messages
from django.utils.translation import ngettext


class YearAnalysisSkillStatisticsAdmin(admin.ModelAdmin):
    list_display = ('year_statistics',)
    search_fields = ('year_statistics',)
    ordering = ['year_statistics']


class SkillByYearAdmin(admin.ModelAdmin):
    list_display = ('year_statistics', 'name_skill', 'count')
    list_filter = ('year_statistics', 'name_skill', 'count')
    search_fields = ('year_statistics', 'name_skill')
    ordering = ['-year_statistics', '-count', 'name_skill']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.year_statistics.graphic_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        SkillByYear.update_or_create_vert_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class StatisticsGraphAdmin(admin.ModelAdmin):
    list_display = ('statistic_graph_title',)
    search_fields = ('statistic_graph_title',)


class SkillByAllYearAdmin(admin.ModelAdmin):
    list_display = ('name_skill', 'count')
    list_filter = ('count', 'name_skill')
    search_fields = ('name_skill',)
    ordering = ['-count', 'name_skill']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        SkillByAllYear.update_or_create_vert_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class DynamicsSalaryByYearsAdmin(admin.ModelAdmin):
    list_display = ('year', 'avg_salary')
    list_filter = ('year',)
    search_fields = ('year',)
    ordering = ['year']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        DynamicsSalaryByYears.update_or_create_hor_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class DynamicsNumberVacanciesByYearsAdmin(admin.ModelAdmin):
    list_display = ('year', 'count')
    list_filter = ('year',)
    search_fields = ('year',)
    ordering = ['year']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        DynamicsNumberVacanciesByYears.update_or_create_hor_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class DynamicsSalaryByYearsSelectedProfessionAdmin(admin.ModelAdmin):
    list_display = ('year', 'avg_salary')
    list_filter = ('year',)
    search_fields = ('year',)
    ordering = ['year']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        DynamicsSalaryByYearsSelectedProfession.update_or_create_hor_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class DynamicsNumberVacanciesByYearsSelectedProfessionAdmin(admin.ModelAdmin):
    list_display = ('year', 'count')
    list_filter = ('year',)
    search_fields = ('year',)
    ordering = ['year']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        DynamicsNumberVacanciesByYearsSelectedProfession.update_or_create_hor_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class LevelSalariesByAreaAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'avg')
    list_filter = ('area_name',)
    search_fields = ('area_name',)
    ordering = ['-avg']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        LevelSalariesByArea.update_or_create_hor_bar_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


class ShareVacanciesByAreaAdmin(admin.ModelAdmin):
    list_display = ('area_name', 'percent')
    list_filter = ('area_name',)
    search_fields = ('area_name',)
    ordering = ['-percent']
    actions = ['delete_selected']

    def delete_selected(self, request, obj):
        graph_titles = [item.statistics_graph.statistic_graph_title for item in obj.all()]

        deleted = obj.all().delete()
        self.message_user(request, ngettext(
            '%d элемент был удален успешно.',
            '%d элементa(-ов) было удалено успешно.',
            deleted[0],
        ) % deleted[0], messages.SUCCESS)
        ShareVacanciesByArea.update_or_create_pie_graph(graph_titles)

    delete_selected.short_description = 'Удалить выбранные элементы (Без дополнительного предупреждения)'


admin.site.register(MainPage)
admin.site.register(YearAnalysisSkillStatistics, YearAnalysisSkillStatisticsAdmin)
admin.site.register(SkillByYear, SkillByYearAdmin)
admin.site.register(StatisticsGraph, StatisticsGraphAdmin)
admin.site.register(SkillByAllYear, SkillByAllYearAdmin)
admin.site.register(DynamicsSalaryByYears, DynamicsSalaryByYearsAdmin)
admin.site.register(DynamicsNumberVacanciesByYears, DynamicsNumberVacanciesByYearsAdmin)
admin.site.register(DynamicsSalaryByYearsSelectedProfession, DynamicsSalaryByYearsSelectedProfessionAdmin)
admin.site.register(DynamicsNumberVacanciesByYearsSelectedProfession,
                    DynamicsNumberVacanciesByYearsSelectedProfessionAdmin)
admin.site.register(LevelSalariesByArea, LevelSalariesByAreaAdmin)
admin.site.register(ShareVacanciesByArea, ShareVacanciesByAreaAdmin)
