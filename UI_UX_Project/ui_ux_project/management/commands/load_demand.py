from django.core.management.base import BaseCommand
from ui_ux_project.models import DemandSalary, DemandVacancy

class Command(BaseCommand):
    help = 'Загружает данные для страницы "Востребованность"'

    def handle(self, *args, **kwargs):
        # Данные для графика 'Динамика уровня зарплат для UX/UI дизайнеров'
        salary_data = {
            2007: 26684.82,
            2008: 41290.62,
            2009: 40491.98,
            2010: 42274.25,
            2011: 46458.86,
            2012: 54116.49,
            2013: 49846.48,
            2014: 52203.69,
            2015: 51020.28,
            2016: 60798.56,
            2017: 63587.51,
            2018: 67567.65,
            2019: 74640.74,
            2020: 81934.93,
            2021: 76053.86,
            2022: 72855.12,
            2023: 73832.75,
            2024: 83894.18,
        }

        # Данные для графика 'Динамика количества вакансий для UX/UI дизайнеров'
        vacancy_data = {
            2007: 56,
            2008: 437,
            2009: 499,
            2010: 796,
            2011: 971,
            2012: 1206,
            2013: 1359,
            2014: 1506,
            2015: 2833,
            2016: 2278,
            2017: 2216,
            2018: 2418,
            2019: 2399,
            2020: 2601,
            2021: 7859,
            2022: 10267,
            2023: 12281,
            2024: 8234,
        }

        # Загрузка данных в модель DemandSalary
        for year, salary in salary_data.items():
            DemandSalary.objects.create(year=year, average_salary=salary)

        # Загрузка данных в модель DemandVacancy
        for year, count in vacancy_data.items():
            DemandVacancy.objects.create(year=year, vacancy_count=count)

        self.stdout.write(self.style.SUCCESS('Данные успешно загружены!'))