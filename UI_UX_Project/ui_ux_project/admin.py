from django.contrib import admin
from .models import *


@admin.register(SalaryDynamic)
class SalaryDynamicAdmin(admin.ModelAdmin):
    list_display = ("year", "average_salary", "profession")
    list_filter = ("year", "profession")
    search_fields = ("year", "profession")


@admin.register(VacancyDynamic)
class VacancyDynamicAdmin(admin.ModelAdmin):
    list_display = ("year", "vacancy_count", "profession")
    list_filter = ("year", "profession")
    search_fields = ("year", "profession")


@admin.register(CitySalary)
class CitySalaryAdmin(admin.ModelAdmin):
    list_display = ("city", "average_salary")
    search_fields = ("city",)


@admin.register(CityVacancyShare)
class CityVacancyShareAdmin(admin.ModelAdmin):
    list_display = ("city", "vacancy_share")
    search_fields = ("city",)


@admin.register(TopSkills)
class TopSkillsAdmin(admin.ModelAdmin):
    list_display = ("year", "skill", "count")
    list_filter = ("year",)
    search_fields = ("skill",)


@admin.register(ChartImage)
class ChartImageAdmin(admin.ModelAdmin):
    list_display = ('chart_type', 'year', 'image')  
    list_filter = ('chart_type', 'year')  
    search_fields = ('chart_type', 'year') 


@admin.register(DemandSalary)
class DemandSalaryAdmin(admin.ModelAdmin):
    list_display = ("year", "average_salary")
    list_filter = ("year",)
    search_fields = ("year",)


@admin.register(DemandVacancy)
class DemandVacancyAdmin(admin.ModelAdmin):
    list_display = ("year", "vacancy_count")
    list_filter = ("year",)
    search_fields = ("year",)

@admin.register(GeoCitySalary)
class GeoCitySalaryAdmin(admin.ModelAdmin):
    list_display = ('city', 'average_salary')
    search_fields = ('city',)
    list_editable = ('average_salary',)


@admin.register(GeoCityVacancyShare)
class GeoCityVacancyShareAdmin(admin.ModelAdmin):
    list_display = ('city', 'vacancy_share')
    search_fields = ('city',)
    list_editable = ('vacancy_share',)


@admin.register(TopUXUISkills)
class TopUXUISkillsAdmin(admin.ModelAdmin):
    list_display = ("year", "skill", "count")
    list_filter = ("year",)
    search_fields = ("skill",)