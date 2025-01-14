import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Настройки графиков
sns.set(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


# Проверка на ключевые слова профессии
def is_ux_ui_designer(name):
    keywords = ['design', 'ux', 'ui', 'дизайн', 'иллюстратор']
    if not isinstance(name, str):
        return False
    return any(keyword.lower() in name.lower() for keyword in keywords)


# Преобразование даты к году
def convert_to_year(date_str):
    try:
        dt = pd.to_datetime(date_str, errors='coerce').tz_localize(None)
        if pd.isna(dt):
            return None
        return dt.year
    except Exception as e:
        print(f"Ошибка преобразования даты: {e}")
        return None


# Загрузка курсов валют
def load_exchange_rates(file_path):
    try:
        rates = pd.read_csv(file_path)
        rates = rates.set_index('date')
        return rates
    except Exception as e:
        print(f"Ошибка загрузки курсов валют: {e}")
        return None


# Получение курса валют
def get_exchange_rate(date, currency, rates):
    try:
        if date not in rates.index:
            return None
        if currency not in rates.columns:
            return None
        rate = rates.loc[date, currency]
        return rate if pd.notna(rate) and rate > 0 else None
    except Exception as e:
        print(f"Ошибка получения курса валют: {e}")
        return None


# Расчет средней зарплаты в рублях
def calculate_salary(row, rates):
    if pd.isna(row['salary_from']) or pd.isna(row['salary_to']) or pd.isna(row['salary_currency']):
        return None

    # Если валюта RUR, возвращаем среднюю зарплату без конвертации
    if row['salary_currency'] == 'RUR':
        return (row['salary_from'] + row['salary_to']) / 2

    # Для других валют выполняем конвертацию
    avg_salary = (row['salary_from'] + row['salary_to']) / 2
    date = convert_to_year(row['published_at'])
    if date is None:
        return None
    rate = get_exchange_rate(date, row['salary_currency'], rates)
    return avg_salary * rate if rate else None


# Построение графиков
def plot_salary_trend(data, title, filename):
    trend = data.groupby('published_at')['converted_salary'].mean()
    print(f"Данные для графика '{title}':")
    print(trend)
    trend.plot(kind='bar', color='orange', edgecolor='black')
    plt.title(title, fontsize=14)
    plt.ylabel('Средняя зарплата (руб.)', fontsize=12)
    plt.xlabel('Год', fontsize=12)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_vacancy_count_trend(data, title, filename):
    trend = data['published_at'].value_counts().sort_index()
    print(f"Данные для графика '{title}':")
    print(trend)
    trend.plot(kind='bar', color='green', edgecolor='black')
    plt.title(title, fontsize=14)
    plt.ylabel('Количество вакансий', fontsize=12)
    plt.xlabel('Год', fontsize=12)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def plot_city_vacancies_share(data, title, filename):
    city_shares = data['area_name'].value_counts(normalize=True)
    city_shares = city_shares[city_shares > 0.01]  # Фильтруем города с долей больше 1%

    if not city_shares.empty:
        other_cities_share = 1 - city_shares.sum()
        city_shares['Другие'] = other_cities_share

        print(f"Данные для графика '{title}':")
        print(city_shares)

        city_shares.plot(kind='pie', autopct='%1.1f%%', startangle=140, colormap='tab20', legend=False)
        plt.title(title, fontsize=14)
        plt.ylabel('')
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()
    else:
        print(f"Нет городов с долей вакансий больше 1% для графика '{title}'.")


def plot_city_salary_trend(data, title, filename):
    city_shares = data['area_name'].value_counts(normalize=True)
    city_shares = city_shares[city_shares > 0.01]  # Фильтруем города с долей больше 1%

    if not city_shares.empty:
        city_trends = data.groupby('area_name')['converted_salary'].mean().sort_values(ascending=False)
        city_trends = city_trends[city_trends.index.isin(city_shares.index)].head(10)

        print(f"Данные для графика '{title}':")
        print(city_trends)

        city_trends.plot(kind='bar', color='blue', edgecolor='black')
        plt.title(title, fontsize=14)
        plt.ylabel('Средняя зарплата (руб.)', fontsize=12)
        plt.xlabel('Город', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(filename)
        plt.show()
    else:
        print(f"Нет городов с долей вакансий больше 1% для графика '{title}'.")


# Топ навыков по годам для всех профессий
def plot_top_skills_by_year(data, start_year=2015, end_year=2024):
    for year in range(start_year, end_year + 1):
        skills_data = data[data['published_at'] == year]
        skills_data = skills_data.dropna(subset=['key_skills'])
        skills = skills_data['key_skills'].str.split('\n').explode().value_counts().head(20)
        print(f"Топ-20 навыков за {year} год:")
        print(skills)

        # Построение графика
        skills.plot(kind='bar', color='purple', edgecolor='black')
        plt.title(f'Топ-20 навыков за {year} год', fontsize=14)
        plt.ylabel('Частота', fontsize=12)
        plt.xlabel('Навыки', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'top_skills_{year}.png')
        plt.show()


# Топ навыков по годам для UX/UI дизайнеров
def plot_top_skills_by_year_for_ux_ui(data, start_year=2015, end_year=2024):
    for year in range(start_year, end_year + 1):
        skills_data = data[(data['published_at'] == year) & (data['name'].apply(is_ux_ui_designer))]
        skills_data = skills_data.dropna(subset=['key_skills'])
        skills = skills_data['key_skills'].str.split('\n').explode().value_counts().head(20)
        print(f"Топ-20 навыков для UX/UI дизайнеров за {year} год:")
        print(skills)

        # Построение графика
        skills.plot(kind='bar', color='purple', edgecolor='black')
        plt.title(f'Топ-20 навыков для UX/UI дизайнеров за {year} год', fontsize=14)
        plt.ylabel('Частота', fontsize=12)
        plt.xlabel('Навыки', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(f'top_skills_ux_ui_{year}.png')
        plt.show()


# Основная функция
def main():
    vacancies_file = '../Vacancies 2024.csv'
    rates_file = 'exchange_rates.csv'
    rates = load_exchange_rates(rates_file)

    if rates is None:
        print("Не удалось загрузить курсы валют.")
        return

    # Загрузка данных о вакансиях
    data = pd.read_csv(
        vacancies_file,
        dtype={
            'name': str,
            'key_skills': str,
            'salary_from': float,
            'salary_to': float,
            'salary_currency': str,
            'area_name': str,
            'published_at': str,
        },
        low_memory=False
    )

    # Преобразование даты к году
    data['published_at'] = data['published_at'].apply(convert_to_year)

    # Расчет зарплаты в рублях
    data['converted_salary'] = data.apply(lambda row: calculate_salary(row, rates), axis=1)

    # Удаление аномальных значений
    data = data[(data['converted_salary'] <= 10_000_000) | (data['converted_salary'].isna())]

    # Удаление строк с NaN в зарплатах
    data = data.dropna(subset=['converted_salary'])

    # Построение графиков
    plot_salary_trend(data, 'Динамика уровня зарплат по годам', 'salary_trend.png')
    plot_vacancy_count_trend(data, 'Динамика количества вакансий по годам', 'vacancy_count_trend.png')
    plot_city_vacancies_share(data, 'Доля вакансий по городам', 'city_vacancy_share.png')
    plot_city_salary_trend(data, 'Уровень зарплат по городам', 'city_salary_trend.png')

    # Топ навыков по годам для всех профессий
    plot_top_skills_by_year(data)

    # Графики для профессии UX/UI дизайнер
    ux_ui_data = data[data['name'].apply(is_ux_ui_designer)]
    plot_salary_trend(ux_ui_data, 'Динамика уровня зарплат для UX/UI дизайнеров', 'ux_ui_salary_trend.png')
    plot_vacancy_count_trend(ux_ui_data, 'Динамика количества вакансий для UX/UI дизайнеров',
                             'ux_ui_vacancy_count_trend.png')
    plot_city_salary_trend(ux_ui_data, 'Уровень зарплат по городам для UX/UI дизайнеров', 'ux_ui_city_salary_trend.png')
    plot_city_vacancies_share(ux_ui_data, 'Доля вакансий по городам для UX/UI дизайнеров',
                              'ux_ui_city_vacancy_share.png')

    # Топ навыков по годам для UX/UI дизайнеров
    plot_top_skills_by_year_for_ux_ui(data)


if __name__ == "__main__":
    main()
