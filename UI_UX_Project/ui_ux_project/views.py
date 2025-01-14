from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Avg, Count, Sum
from .models import *
from .utils import *
import pandas as pd
import requests
from django.core.paginator import Paginator
from bs4 import BeautifulSoup


class MainPageView(TemplateView):
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Динамика зарплат по годам
        context['salary_dynamics'] = SalaryDynamic.objects.values('year').annotate(
            average_salary=Avg('average_salary')
        ).order_by('year')

        # Динамика количества вакансий по годам (исправлено на Sum)
        context['vacancy_dynamics'] = VacancyDynamic.objects.values('year').annotate(
            vacancy_count=Sum('vacancy_count') 
        ).order_by('year')

        # Уровень зарплат по городам
        context['city_salary'] = CitySalary.objects.values('city').annotate(
            average_salary=Avg('average_salary')
        ).order_by('-average_salary')

        # Доля вакансий по городам
        context['city_share'] = CityVacancyShare.objects.values('city').annotate(
            vacancy_share=Avg('vacancy_share')
        ).order_by('-vacancy_share')

        # Топ-20 навыков
        selected_year = self.request.GET.get('year', 2024)  # По умолчанию 2024 год
        context['top_skills'] = TopSkills.objects.filter(year=selected_year).order_by('-count')[:20]
        context['selected_year'] = selected_year
        context['years'] = TopSkills.objects.values_list('year', flat=True).distinct().order_by('year')

        return context


class DemandView(TemplateView):
    template_name = 'demand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Динамика зарплат по годам
        context['demand_salary'] = SalaryDynamic.objects.values('year').annotate(
            average_salary=Avg('average_salary')
        ).order_by('year')

        # Динамика количества вакансий по годам 
        context['demand_vacancies'] = VacancyDynamic.objects.values('year').annotate(
            vacancy_count=Sum('vacancy_count') 
        ).order_by('year')

        return context


class GeoView(TemplateView):
    template_name = 'geo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Уровень зарплат по городам
        context['geo_salary'] = CitySalary.objects.values('city').annotate(
            average_salary=Avg('average_salary')
        ).order_by('-average_salary')

        # Доля вакансий по городам
        context['geo_share'] = CityVacancyShare.objects.values('city').annotate(
            vacancy_share=Avg('vacancy_share')
        ).order_by('-vacancy_share')

        return context


class SkillsView(TemplateView):
    template_name = 'skills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_year = self.request.GET.get('year', 2024)
        
        # Топ-20 навыков для выбранного года
        context['top_skills'] = TopSkills.objects.filter(year=selected_year).order_by('-count')[:20]
        context['selected_year'] = selected_year
        
        # Годы для выпадающего списка
        context['years'] = TopSkills.objects.values_list('year', flat=True).distinct().order_by('year')

        return context



class CSVUploadView(TemplateView):
    template_name = 'csv_upload.html'

    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        if not csv_file:
            return render(request, 'csv_error.html', {'error': 'Файл не был загружен'})

        try:
            data = pd.read_csv(csv_file)
            for _, row in data.iterrows():
                # Создание записей в соответствующих моделях
                SalaryDynamic.objects.create(
                    year=row['year'],
                    average_salary=row['average_salary']
                )
                VacancyDynamic.objects.create(
                    year=row['year'],
                    vacancy_count=row['vacancy_count']
                )
                CitySalary.objects.create(
                    city=row['city'],
                    average_salary=row['average_salary']
                )
                CityVacancyShare.objects.create(
                    city=row['city'],
                    vacancy_share=row['vacancy_share']
                )
                # Добавляем данные для топ-20 навыков
                if 'skill' in row and 'count' in row:
                    TopSkills.objects.create(
                        year=row['year'],
                        skill=row['skill'],
                        count=row['count']
                    )
            return render(request, 'csv_success.html')
        except Exception as e:
            return render(request, 'csv_error.html', {'error': str(e)})
        
class StatisticsView(TemplateView):
    template_name = 'statistics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Динамика зарплат по годам
        context['salary_dynamics'] = SalaryDynamic.objects.values('year').annotate(
            average_salary=Avg('average_salary')
        ).order_by('year')

        # Динамика количества вакансий по годам
        context['vacancy_dynamics'] = VacancyDynamic.objects.values('year').annotate(
            vacancy_count=Sum('vacancy_count')
        ).order_by('year')

        # Уровень зарплат по городам
        context['city_salary'] = CitySalary.objects.values('city').annotate(
            average_salary=Avg('average_salary')
        ).order_by('-average_salary')

        # Доля вакансий по городам
        context['city_share'] = CityVacancyShare.objects.values('city').annotate(
            vacancy_share=Avg('vacancy_share')
        ).order_by('-vacancy_share')

        # Топ-20 навыков
        selected_year = self.request.GET.get('year', 2024)  # По умолчанию 2024 год
        context['top_skills'] = TopSkills.objects.filter(year=selected_year).order_by('-count')[:20]
        context['selected_year'] = selected_year
        context['years'] = TopSkills.objects.values_list('year', flat=True).distinct().order_by('year')

        # Загрузка изображений для графиков
        context['salary_chart_image'] = ChartImage.objects.filter(chart_type='salary_trend').first()
        context['vacancy_chart_image'] = ChartImage.objects.filter(chart_type='vacancy_trend').first()
        context['city_salary_chart_image'] = ChartImage.objects.filter(chart_type='city_salary_trend').first()
        context['city_share_chart_image'] = ChartImage.objects.filter(chart_type='city_vacancy_share').first()
        
        # Загрузка изображения для топ-20 навыков с учётом года
        context['skills_chart_image'] = ChartImage.objects.filter(chart_type='top_skills', year=selected_year).first()

        return context

class DemandView(TemplateView):
    template_name = 'demand.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Динамика зарплат по годам для страницы "Востребованность"
        context['demand_salary_dynamics'] = DemandSalary.objects.all().order_by('year')
        
        # Динамика количества вакансий по годам для страницы "Востребованность"
        context['demand_vacancy_dynamics'] = DemandVacancy.objects.all().order_by('year')
        
        # Изображения графиков
        context['demand_salary_chart_image'] = ChartImage.objects.filter(
            chart_type='demand_salary_trend'  # Тип графика для зарплат
        ).first()
        
        context['demand_vacancy_chart_image'] = ChartImage.objects.filter(
            chart_type='demand_vacancy_trend'  # Тип графика для вакансий
        ).first()
        
        return context
        
class GeoView(TemplateView):
    template_name = 'geo.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Данные для таблицы "Уровень зарплат по городам"
        context['geo_salary'] = GeoCitySalary.objects.all().order_by('-average_salary')

        # Данные для таблицы "Доля вакансий по городам"
        context['geo_share'] = GeoCityVacancyShare.objects.all().order_by('-vacancy_share')

        # Изображения графиков
        context['geo_salary_chart_image'] = ChartImage.objects.filter(
            chart_type='geo_salary_by_city'
        ).first()
        
        context['geo_share_chart_image'] = ChartImage.objects.filter(
            chart_type='geo_vacancy_share_by_city'
        ).first()

        return context
    

class TopUXUISkillsView(TemplateView):
    template_name = 'skills.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем выбранный год из запроса (по умолчанию 2024)
        selected_year = self.request.GET.get('year', 2024)
        
        # Топ-20 UX/UI навыков для выбранного года
        context['top_uxui_skills'] = TopUXUISkills.objects.filter(year=selected_year).order_by('-count')[:20]
        context['selected_year'] = selected_year
        
        # Годы для выпадающего списка
        context['years'] = TopUXUISkills.objects.values_list('year', flat=True).distinct().order_by('year')

        # Загрузка изображения для графика
        context['uxui_skills_chart_image'] = ChartImage.objects.filter(
            chart_type='top_uxui_skills',  # Тип графика
            year=selected_year  # Выбранный год
        ).first()

        return context

def latest_vacancies(request):
    vacancies = get_vacancies()
    detailed_vacancies = []
    
    for vacancy in vacancies:
        details = get_vacancy_details(vacancy['id'])
        if details:
            detailed_vacancies.append({
                'name': details.get('name', ''),
                'description': details.get('description', ''),
                'skills': ', '.join([skill['name'] for skill in details.get('key_skills', [])]),
                'company': details.get('employer', {}).get('name', ''),
                'salary': details.get('salary', {}),
                'region': details.get('area', {}).get('name', ''),
                'published_at': details.get('published_at', '')
            })
    
    return render(request, 'latest_vacancies.html', {'vacancies': detailed_vacancies})

def vacancy_list(request):
    """
    Отображает список вакансий.
    """
    profession = "UX/UI Designer"
    vacancies = get_vacancies(profession)
    return render(request, 'vacancy.html', {'vacancies': vacancies})

class VacanciesView(TemplateView):
    template_name = 'vacancies.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Получение вакансий через API HH
        context['vacancies'] = self.get_vacancies_from_api()
        
        return context

    def get_vacancies_from_api(self):
        url = "https://api.hh.ru/vacancies"
        params = {
            'period': 1,
            'order_by': 'publication_time',
            'text': 'UX/UI дизайнер',
            'search_field': 'name',
            'per_page': 10
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            vacancies = data.get('items', [])
            
            # Для каждой вакансии получаем полное описание
            for vacancy in vacancies:
                vacancy_id = vacancy.get('id')
                if vacancy_id:
                    vacancy_details = self.get_vacancy_details(vacancy_id)
                    if vacancy_details:
                        # Обрабатываем описание: преобразуем <ul> и <li> в тире
                        description = vacancy_details.get('description', '')
                        vacancy['description'] = self.convert_ul_to_dash(description)
                    else:
                        vacancy['description'] = 'Описание отсутствует'
                else:
                    vacancy['description'] = 'Описание отсутствует'
            
        except requests.RequestException as e:
            vacancies = []
            print(f"Ошибка при запросе к API HH: {e}")
        
        return vacancies

    def get_vacancy_details(self, vacancy_id):
        url = f"https://api.hh.ru/vacancies/{vacancy_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка при запросе деталей вакансии: {e}")
            return None

    def convert_ul_to_dash(self, html_text):
        """
        Преобразует HTML-списки (<ul>, <li>) в текст с тире.
        :param html_text: Исходный HTML-текст.
        :return: Обработанный текст.
        """
        soup = BeautifulSoup(html_text, 'html.parser')
        
        # Находим все теги <ul>
        for ul in soup.find_all('ul'):
            # Для каждого <li> внутри <ul> заменяем его на текст с тире и переносом строки
            for li in ul.find_all('li'):
                li.replace_with(f"— {li.get_text(strip=True)}\n")
            # Удаляем сам тег <ul>
            ul.unwrap()
        
        # Возвращаем обработанный HTML
        return str(soup)