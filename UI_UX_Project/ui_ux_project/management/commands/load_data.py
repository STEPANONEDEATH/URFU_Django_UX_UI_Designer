import pandas as pd
from django.core.management.base import BaseCommand
from ui_ux_project.models import SalaryDynamic, VacancyDynamic, CitySalary, CityVacancyShare, TopSkills

class Command(BaseCommand):
    help = 'Load all data into Django models'

    def handle(self, *args, **kwargs):
        self.clear_old_data()
        self.load_salary_data()
        self.load_vacancy_data()
        self.load_city_salary_data()
        self.load_city_vacancy_share_data()
        self.load_top_skills_data()

        self.stdout.write(self.style.SUCCESS('All data loaded successfully!'))

    def clear_old_data(self):
        """Очистка старых данных."""
        SalaryDynamic.objects.all().delete()
        VacancyDynamic.objects.all().delete()
        CitySalary.objects.all().delete()
        CityVacancyShare.objects.all().delete()
        TopSkills.objects.all().delete()

    def load_salary_data(self):
        """Загрузка данных для SalaryDynamic (Динамика уровня зарплат по годам)."""
        salary_data = {
            2007: 38916.885701,
            2008: 43646.407060,
            2009: 42492.194506,
            2010: 43846.582528,
            2011: 47451.858542,
            2012: 48243.134306,
            2013: 51510.701029,
            2014: 49547.762714,
            2015: 52696.590135,
            2016: 55290.796335,
            2017: 60935.931003,
            2018: 58335.140804,
            2019: 69467.910076,
            2020: 73445.599431,
            2021: 81822.702563,
            2022: 90188.434455,
            2023: 95201.207781,
            2024: 107221.650630,
        }
        for year, salary in salary_data.items():
            SalaryDynamic.objects.create(year=year, average_salary=salary)

    def load_vacancy_data(self):
        """Загрузка данных для VacancyDynamic (Динамика количества вакансий по годам)."""
        vacancy_data = {
            2007: 2196,
            2008: 17549,
            2009: 17709,
            2010: 29093,
            2011: 36700,
            2012: 44153,
            2013: 59954,
            2014: 66835,
            2015: 70039,
            2016: 75143,
            2017: 82823,
            2018: 131701,
            2019: 115086,
            2020: 127968,
            2021: 190904,
            2022: 188526,
            2023: 129538,
            2024: 84691,
        }
        for year, count in vacancy_data.items():  # Исправлено: убраны кавычки
            VacancyDynamic.objects.create(year=year, vacancy_count=count)

    def load_city_salary_data(self):
        """Загрузка данных для CitySalary (Уровень зарплат по городам)."""
        city_salary_data = {
            "Москва": 93345.985295,
            "Санкт-Петербург": 77494.781147,
            "Новосибирск": 74259.503327,
            "Екатеринбург": 73762.254412,
            "Казань": 65733.706753,
            "Краснодар": 63776.910146,
            "Самара": 61235.149047,
            "Нижний Новгород": 60660.632333,
            "Челябинск": 60114.931853,
            "Уфа": 60114.108198,
        }
        for city, salary in city_salary_data.items():
            CitySalary.objects.create(city=city, average_salary=salary)

    def load_city_vacancy_share_data(self):
        """Загрузка данных для CityVacancyShare (Доля вакансий по городам)."""
        city_share_data = {
            "Москва": 0.297933,
            "Санкт-Петербург": 0.112625,
            "Новосибирск": 0.027697,
            "Екатеринбург": 0.024814,
            "Казань": 0.024749,
            "Нижний Новгород": 0.022393,
            "Краснодар": 0.021212,
            "Ростов-на-Дону": 0.020451,
            "Самара": 0.015026,
            "Воронеж": 0.014557,
            "Красноярск": 0.013557,
            "Уфа": 0.013097,
            "Пермь": 0.012482,
            "Челябинск": 0.011824,
            "Другие": 0.367583,
        }
        for city, share in city_share_data.items():
            CityVacancyShare.objects.create(city=city, vacancy_share=share)

    def load_top_skills_data(self):
        """Загрузка данных для TopSkills (Топ-20 навыков по годам)."""
        skills_data = {
            2015: [
                {"skill": "JavaScript", "count": 1247},
                {"skill": "HTML", "count": 1099},
                {"skill": "PHP", "count": 1082},
                {"skill": "jQuery", "count": 951},
                {"skill": "MySQL", "count": 927},
                {"skill": "CSS", "count": 908},
                {"skill": "HTML5", "count": 822},
                {"skill": "Git", "count": 774},
                {"skill": "Ведение переговоров", "count": 758},
                {"skill": "CSS3", "count": 691},
                {"skill": "Активные продажи", "count": 609},
                {"skill": "Работа в команде", "count": 604},
                {"skill": "PHP5", "count": 603},
                {"skill": "Поиск и привлечение клиентов", "count": 600},
                {"skill": "Ajax", "count": 593},
                {"skill": "ООП", "count": 571},
                {"skill": "Пользователь ПК", "count": 549},
                {"skill": "Управление проектами", "count": 545},
                {"skill": "Грамотная речь", "count": 538},
                {"skill": "Телефонные переговоры", "count": 526},
            ],
            2016: [
                {"skill": "JavaScript", "count": 4583},
                {"skill": "HTML", "count": 3910},
                {"skill": "PHP", "count": 3640},
                {"skill": "CSS", "count": 3291},
                {"skill": "jQuery", "count": 3237},
                {"skill": "Git", "count": 3132},
                {"skill": "MySQL", "count": 2917},
                {"skill": "Ведение переговоров", "count": 2761},
                {"skill": "HTML5", "count": 2558},
                {"skill": "Работа в команде", "count": 2519},
                {"skill": "Пользователь ПК", "count": 2305},
                {"skill": "ООП", "count": 2196},
                {"skill": "Поиск и привлечение клиентов", "count": 2113},
                {"skill": "CSS3", "count": 2056},
                {"skill": "Активные продажи", "count": 1992},
                {"skill": "Управление проектами", "count": 1880},
                {"skill": "Телефонные переговоры", "count": 1857},
                {"skill": "Грамотная речь", "count": 1836},
                {"skill": "SQL", "count": 1829},
                {"skill": "1С-Битрикс", "count": 1790},
            ],
            2017: [
                {"skill": "JavaScript", "count": 5959},
                {"skill": "HTML", "count": 5079},
                {"skill": "PHP", "count": 4692},
                {"skill": "CSS", "count": 4497},
                {"skill": "Git", "count": 4214},
                {"skill": "MySQL", "count": 4025},
                {"skill": "Ведение переговоров", "count": 3814},
                {"skill": "jQuery", "count": 3434},
                {"skill": "HTML5", "count": 3212},
                {"skill": "Пользователь ПК", "count": 2852},
                {"skill": "Активные продажи", "count": 2775},
                {"skill": "Работа в команде", "count": 2767},
                {"skill": "Управление проектами", "count": 2703},
                {"skill": "B2B Продажи", "count": 2606},
                {"skill": "ООП", "count": 2567},
                {"skill": "Грамотная речь", "count": 2428},
                {"skill": "Телефонные переговоры", "count": 2425},
                {"skill": "SQL", "count": 2394},
                {"skill": "Деловая переписка", "count": 2374},
                {"skill": "CSS3", "count": 2262},
            ],
            2018: [
                {"skill": "JavaScript", "count": 8158},
                {"skill": "HTML", "count": 6882},
                {"skill": "PHP", "count": 6213},
                {"skill": "Git", "count": 6186},
                {"skill": "CSS", "count": 6039},
                {"skill": "Ведение переговоров", "count": 5801},
                {"skill": "MySQL", "count": 5172},
                {"skill": "Работа в команде", "count": 5168},
                {"skill": "Пользователь ПК", "count": 5112},
                {"skill": "Активные продажи", "count": 4300},
                {"skill": "Грамотная речь", "count": 4291},
                {"skill": "Деловая переписка", "count": 4198},
                {"skill": "Управление проектами", "count": 4184},
                {"skill": "Телефонные переговоры", "count": 4141},
                {"skill": "jQuery", "count": 4022},
                {"skill": "HTML5", "count": 3913},
                {"skill": "B2B Продажи", "count": 3757},
                {"skill": "SQL", "count": 3595},
                {"skill": "Деловое общение", "count": 3383},
                {"skill": "Навыки продаж", "count": 3237},
            ],
            2019: [
                {"skill": "JavaScript", "count": 7912},
                {"skill": "Пользователь ПК", "count": 7079},
                {"skill": "Git", "count": 6542},
                {"skill": "Работа в команде", "count": 6427},
                {"skill": "HTML", "count": 6397},
                {"skill": "Ведение переговоров", "count": 6191},
                {"skill": "Грамотная речь", "count": 6167},
                {"skill": "CSS", "count": 5552},
                {"skill": "PHP", "count": 5448},
                {"skill": "Активные продажи", "count": 4721},
                {"skill": "MySQL", "count": 4547},
                {"skill": "SQL", "count": 4392},
                {"skill": "Управление проектами", "count": 4290},
                {"skill": "Телефонные переговоры", "count": 4279},
                {"skill": "Деловая переписка", "count": 4030},
                {"skill": "Деловое общение", "count": 4024},
                {"skill": "B2B Продажи", "count": 3902},
                {"skill": "Linux", "count": 3505},
                {"skill": "Навыки продаж", "count": 3301},
                {"skill": "ООП", "count": 3231},
            ],
            2020: [
                {"skill": "Пользователь ПК", "count": 13256},
                {"skill": "Грамотная речь", "count": 11846},
                {"skill": "Работа в команде", "count": 11132},
                {"skill": "Git", "count": 9847},
                {"skill": "JavaScript", "count": 9326},
                {"skill": "Активные продажи", "count": 9226},
                {"skill": "HTML", "count": 7205},
                {"skill": "SQL", "count": 6775},
                {"skill": "CSS", "count": 6514},
                {"skill": "Деловое общение", "count": 6420},
                {"skill": "PHP", "count": 6266},
                {"skill": "Ведение переговоров", "count": 6168},
                {"skill": "Телефонные переговоры", "count": 6039},
                {"skill": "Linux", "count": 5913},
                {"skill": "MySQL", "count": 5868},
                {"skill": "Клиентоориентированность", "count": 5464},
                {"skill": "Английский язык", "count": 5331},
                {"skill": "Навыки продаж", "count": 5183},
                {"skill": "Холодные продажи", "count": 4934},
                {"skill": "B2B Продажи", "count": 4796},
            ],
            2021: [
                {"skill": "Работа в команде", "count": 27121},
                {"skill": "Грамотная речь", "count": 25693},
                {"skill": "Пользователь ПК", "count": 21467},
                {"skill": "Git", "count": 14962},
                {"skill": "JavaScript", "count": 12557},
                {"skill": "Деловое общение", "count": 11711},
                {"skill": "Активные продажи", "count": 11438},
                {"skill": "SQL", "count": 10787},
                {"skill": "Ведение переговоров", "count": 10683},
                {"skill": "Английский язык", "count": 10271},
                {"skill": "Телефонные переговоры", "count": 9688},
                {"skill": "HTML", "count": 9309},
                {"skill": "Грамотность", "count": 9197},
                {"skill": "Linux", "count": 8919},
                {"skill": "Клиентоориентированность", "count": 8425},
                {"skill": "Adobe Photoshop", "count": 8397},
                {"skill": "PHP", "count": 8385},
                {"skill": "Деловая переписка", "count": 8153},
                {"skill": "CSS", "count": 8104},
                {"skill": "MySQL", "count": 7983},
            ],
            2022: [
                {"skill": "Работа в команде", "count": 26663},
                {"skill": "Пользователь ПК", "count": 18936},
                {"skill": "Грамотная речь", "count": 14757},
                {"skill": "Git", "count": 11514},
                {"skill": "SQL", "count": 9183},
                {"skill": "Техническое обслуживание", "count": 8855},
                {"skill": "JavaScript", "count": 8746},
                {"skill": "Linux", "count": 8193},
                {"skill": "Adobe Photoshop", "count": 8096},
                {"skill": "Работа в условиях многозадачности", "count": 7547},
                {"skill": "Английский язык", "count": 7007},
                {"skill": "Грамотность", "count": 6999},
                {"skill": "PHP", "count": 6707},
                {"skill": "Работа с большим объемом информации", "count": 6582},
                {"skill": "Настройка ПК", "count": 6484},
                {"skill": "1С программирование", "count": 6465},
                {"skill": "Управление проектами", "count": 6407},
                {"skill": "HTML", "count": 5920},
                {"skill": "MySQL", "count": 5899},
                {"skill": "1С: Предприятие 8", "count": 5822},
            ],
            2023: [
                {"skill": "Работа в команде", "count": 11253},
                {"skill": "Грамотная речь", "count": 10358},
                {"skill": "Пользователь ПК", "count": 9226},
                {"skill": "Git", "count": 6877},
                {"skill": "Adobe Photoshop", "count": 6653},
                {"skill": "SQL", "count": 6409},
                {"skill": "Linux", "count": 5505},
                {"skill": "Техническая поддержка", "count": 5447},
                {"skill": "JavaScript", "count": 5203},
                {"skill": "Работа с большим объемом информации", "count": 5172},
                {"skill": "1С программирование", "count": 5091},
                {"skill": "Настройка ПК", "count": 5040},
                {"skill": "PHP", "count": 4698 }, 
                {"skill": "Управление проектами","count": 4608 },
                {"skill": "1С: Предприятие 8","count": 4352 },
                {"skill": "Настройка сетевых подключений","count": 4325 },
                {"skill": "Аналитическое мышление","count": 4310 },
                {"skill": "Деловое общение","count": 4259 },
                {"skill": "Деловая переписка","count": 4187 },
                {"skill": "Настройка ПО","count": 4107 },
            ],
            2024: [
                {"skill": "Техническая поддержка","count": 5228 },
                {"skill": "SQL","count": 4778 },
                {"skill": "Настройка ПК","count": 4565 },
                {"skill": "Грамотная речь","count": 4270 },
                {"skill": "Пользователь ПК","count": 4015 },
                {"skill": "Adobe Photoshop","count": 3845 },
                {"skill": "Работа с большим объемом информации","count": 3844 },
                {"skill": "Аналитическое мышление","count": 3841 },
                {"skill": "Настройка сетевых подключений","count": 3816 },
                {"skill": "Работа в команде","count": 3788 },
                {"skill": "Git","count": 3764 },
                {"skill": "Настройка ПО","count": 3672 },
                {"skill": "Linux","count": 3353 },
                {"skill": "Деловая коммуникация","count": 3334 },
                {"skill": "Информационные технологии","count": 3323 },
                {"skill": "Деловое общение","count": 3298 },
                {"skill": "Деловая переписка","count": 3225 },
                {"skill": "JavaScript","count": 3139 },
                {"skill": "1С программирование","count": 2965 },
                {"skill": "Администрирование сетевого оборудования","count": 2869 },
            ],
       }
        for year, skills in skills_data.items():
            for skill_data in skills:
                TopSkills.objects.create(year=year, **skill_data)