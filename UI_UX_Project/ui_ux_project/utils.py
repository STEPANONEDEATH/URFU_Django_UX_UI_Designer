import requests
from datetime import datetime
from bs4 import BeautifulSoup

def get_vacancy_details(vacancy_id):
    """
    Получает полное описание вакансии по её ID.
    :param vacancy_id: ID вакансии.
    :return: Описание вакансии или "Описание отсутствует".
    """
    url = f"https://api.hh.ru/vacancies/{vacancy_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def get_vacancies(profession_keywords):
    """
    Получает список вакансий по ключевым словам профессии.
    :param profession_keywords: Список ключевых слов для поиска (например, ["design", "ux", "ui", "дизайн", "иллюстратор"]).
    :return: Список вакансий.
    """
    params = {
        'text': profession_keywords, 
        'order_by': 'publication_time',
        'per_page': 10,
        'search_field': 'name'
    }

    response = requests.get("https://api.hh.ru/vacancies", params=params)
    if response.status_code != 200:
        print(f"Ошибка: {response.status_code}. {response.text}")
        return []

    return response.json().get('items', [])

def format_salary(salary):
    """
    Форматирует информацию о зарплате в предпочтительном формате.
    :param salary: Данные о зарплате из API.
    :return: Отформатированная строка с зарплатой.
    """
    if not salary:
        return 'Не указан'

    salary_from = salary.get('from')
    salary_to = salary.get('to')
    currency = salary.get('currency', 'RUR')
    gross = '(gross)' if salary.get('gross') else ''

    if salary_from and salary_to:
        return f"{salary_from} - {salary_to} {currency} {gross}"
    elif salary_from:
        return f"{salary_from} {currency} {gross}"
    elif salary_to:
        return f"до {salary_to} {currency} {gross}"
    return 'Не указан'

def format_date(date_str):
    """
    Форматирует дату публикации.
    :param date_str: Дата в строковом формате.
    :return: Отформатированная строка с датой.
    """
    if not date_str:
        return 'Не указана'

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S')
    except ValueError:
        return 'Не указана'

def truncate_text(text, max_length=500):
    """
    Обрезает текст до указанной длины.
    :param text: Исходный текст.
    :param max_length: Максимальная длина текста.
    :return: Обрезанный текст с многоточием, если он превышает длину.
    """
    return text if len(text) <= max_length else text[:max_length - 3] + '...'

def clean_html(self, html_text):
    """
    Удаляет HTML-разметку из текста и форматирует списки.
    :param html_text: Исходный HTML-текст.
    :return: Очищенный и отформатированный текст с HTML-тегами.
    """
    if not html_text:
        return '<p>Описание отсутствует</p>'

    soup = BeautifulSoup(html_text, 'html.parser')

    # Обрабатываем списки (<ul>, <ol>)
    for list_tag in soup.find_all(['ul', 'ol']):
        for li in list_tag.find_all('li', recursive=False):
            li.string = f"• {li.get_text(strip=True)}"
            li.append(soup.new_tag('br'))
        list_tag.unwrap()

    # Добавляем переносы строк между блоками текста
    for tag in soup.find_all(['p', 'br', 'strong', 'em']):
        if tag.name == 'p' and tag.get_text(strip=True):
            tag.append(soup.new_tag('br')) 

    # Удаляем все остальные HTML-теги, кроме <p>, <br>, <strong>, <em>
    allowed_tags = ['p', 'br', 'strong', 'em']
    for tag in soup.find_all(True):
        if tag.name not in allowed_tags:
            tag.unwrap()

    # Возвращаем очищенный HTML
    return str(soup)


def format_vacancy(vacancy):
    """
    Форматирует информацию о вакансии в единый формат.
    :param vacancy: Данные о вакансии.
    :return: Отформатированная информация о вакансии.
    """
    vacancy_details = get_vacancy_details(vacancy['id'])
    if not vacancy_details:
        return None

    description = clean_html(vacancy_details.get('description', 'Описание отсутствует'))
    salary = format_salary(vacancy.get('salary'))
    published_at = format_date(vacancy.get('published_at'))

    formatted_vacancy = {
        'name': vacancy.get('name', 'Название не указано'),
        'salary': salary,
        'description': truncate_text(description),
        'published_at': published_at,
        'employer': vacancy.get('employer', {}).get('name', 'Работодатель не указан'),
        'experience': vacancy.get('experience', {}).get('name', 'Опыт не указан'),
        'employment': vacancy.get('employment', {}).get('name', 'Тип занятости не указан')
    }

    return formatted_vacancy

def main():
    profession_keywords = ["design", "ux", "ui", "дизайн", "иллюстратор"]
    vacancies = get_vacancies(profession_keywords)

    formatted_vacancies = []
    for vacancy in vacancies:
        formatted_vacancy = format_vacancy(vacancy)
        if formatted_vacancy:
            formatted_vacancies.append(formatted_vacancy)

    for vacancy in formatted_vacancies:
        print(vacancy)

if __name__ == "__main__":
    main()