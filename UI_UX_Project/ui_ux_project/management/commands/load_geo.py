from django.core.management.base import BaseCommand
from ui_ux_project.models import GeoCitySalary, GeoCityVacancyShare

class Command(BaseCommand):
    help = "Загружает данные для страницы 'География'"

    def handle(self, *args, **kwargs):
        # Данные для графика 'Уровень зарплат по городам для UX/UI дизайнеров'
        salary_data = {
            "Москва": 90708.37,
            "Санкт-Петербург": 75115.79,
            "Новосибирск": 68756.29,
            "Екатеринбург": 66909.72,
            "Казань": 63605.24,
            "Краснодар": 57755.23,
            "Нижний Новгород": 56591.13,
            "Самара": 55015.85,
            "Уфа": 54545.56,
            "Ярославль": 53131.84,
        }

        # Данные для графика 'Доля вакансий по городам для UX/UI дизайнеров'
        vacancy_share_data = {
            "Москва": 0.333466,
            "Санкт-Петербург": 0.139116,
            "Новосибирск": 0.029776,
            "Казань": 0.028813,
            "Краснодар": 0.028564,
            "Екатеринбург": 0.028481,
            "Ростов-на-Дону": 0.020759,
            "Нижний Новгород": 0.020111,
            "Воронеж": 0.015677,
            "Уфа": 0.013717,
            "Самара": 0.012754,
            "Челябинск": 0.012239,
            "Ярославль": 0.011409,
            "Красноярск": 0.010280,
            "Другие": 0.294839,
        }

        # Загрузка данных в модель GeoCitySalary
        for city, salary in salary_data.items():
            GeoCitySalary.objects.create(city=city, average_salary=salary)

        # Загрузка данных в модель GeoCityVacancyShare
        for city, share in vacancy_share_data.items():
            GeoCityVacancyShare.objects.create(city=city, vacancy_share=share * 100)  # Преобразуем долю в проценты

        self.stdout.write(self.style.SUCCESS("Данные успешно загружены!"))