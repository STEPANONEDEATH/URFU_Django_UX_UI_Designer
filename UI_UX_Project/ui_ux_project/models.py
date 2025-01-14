from django.db import models

# Динамика зарплат по годам
class SalaryDynamic(models.Model):
    year = models.IntegerField(verbose_name="Год")
    average_salary = models.FloatField(verbose_name="Средняя зарплата")

    def __str__(self):
        return f"{self.year} - {self.average_salary}"

    class Meta:
        verbose_name = "Динамика зарплат"
        verbose_name_plural = "Динамика зарплат"


# Динамика количества вакансий по годам
class VacancyDynamic(models.Model):
    year = models.IntegerField(unique=True, verbose_name="Год")
    vacancy_count = models.IntegerField(verbose_name="Количество вакансий")

    def __str__(self):
        return f"{self.year} - {self.vacancy_count}"

    class Meta:
        verbose_name = "Динамика вакансий"
        verbose_name_plural = "Динамика вакансий"


# Уровень зарплат по городам
class CitySalary(models.Model):
    city = models.CharField(max_length=100, unique=True, verbose_name="Город")
    average_salary = models.FloatField(verbose_name="Средняя зарплата")

    def __str__(self):
        return f"{self.city} - {self.average_salary}"

    class Meta:
        verbose_name = "Зарплата по городам"
        verbose_name_plural = "Зарплата по городам"


# Доля вакансий по городам
class CityVacancyShare(models.Model):
    city = models.CharField(max_length=100, unique=True, verbose_name="Город")
    vacancy_share = models.FloatField(verbose_name="Доля вакансий")

    def __str__(self):
        return f"{self.city} - {self.vacancy_share}"

    class Meta:
        verbose_name = "Доля вакансий по городам"
        verbose_name_plural = "Доля вакансий по городам"


# Топ навыков
class TopSkills(models.Model):
    year = models.IntegerField(verbose_name="Год")
    skill = models.CharField(max_length=100, verbose_name="Навык")
    count = models.IntegerField(verbose_name="Количество упоминаний")

    def __str__(self):
        return f"{self.year} - {self.skill}"

    class Meta:
        verbose_name = "Топ навыков"
        verbose_name_plural = "Топ навыков"
        unique_together = ("year", "skill")


class ChartImage(models.Model):
    # Тип графика (например, "salary_trend", "vacancy_trend", "top_skills" и т.д.)
    chart_type = models.CharField(max_length=50, verbose_name="Тип графика")

    # Год (опционально, для графиков, которые зависят от года)
    year = models.IntegerField(null=True, blank=True, verbose_name="Год")

    # Изображение
    image = models.ImageField(upload_to='charts/', verbose_name="Изображение")

    def __str__(self):
        if self.year:
            return f"{self.chart_type} ({self.year})"
        return self.chart_type

    class Meta:
        verbose_name = "График"
        verbose_name_plural = "Графики"
        unique_together = ('chart_type', 'year')


# Общая статистика
class SalaryDynamic(models.Model):
    year = models.IntegerField(verbose_name="Год")
    average_salary = models.FloatField(verbose_name="Средняя зарплата")
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name="Профессия")

    def __str__(self):
        if self.profession:
            return f"{self.year} - {self.profession} - {self.average_salary}"
        return f"{self.year} - Общие - {self.average_salary}"

    class Meta:
        verbose_name = "Динамика зарплат"
        verbose_name_plural = "Динамика зарплат"


class VacancyDynamic(models.Model):
    year = models.IntegerField(verbose_name="Год")
    vacancy_count = models.IntegerField(verbose_name="Количество вакансий")
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name="Профессия")

    def __str__(self):
        if self.profession:
            return f"{self.year} - {self.profession} - {self.vacancy_count}"
        return f"{self.year} - Общие - {self.vacancy_count}"

    class Meta:
        verbose_name = "Динамика вакансий"
        verbose_name_plural = "Динамика вакансий"


# Востребованность
class DemandSalary(models.Model):
    year = models.IntegerField(verbose_name="Год")
    average_salary = models.FloatField(verbose_name="Средняя зарплата")

    def __str__(self):
        return f"{self.year} - {self.average_salary}"

    class Meta:
        verbose_name = "Зарплата (Востребованность)"
        verbose_name_plural = "Зарплаты (Востребованность)"


class DemandVacancy(models.Model):
    year = models.IntegerField(verbose_name="Год")
    vacancy_count = models.IntegerField(verbose_name="Количество вакансий")

    def __str__(self):
        return f"{self.year} - {self.vacancy_count}"

    class Meta:
        verbose_name = "Вакансия (Востребованность)"
        verbose_name_plural = "Вакансии (Востребованность)"


# География
class GeoCitySalary(models.Model):
    city = models.CharField(max_length=100, verbose_name="Город")
    average_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Средняя зарплата")

    def __str__(self):
        return f"{self.city} - {self.average_salary}"

    class Meta:
        verbose_name = "Зарплата по городам (География)"
        verbose_name_plural = "Зарплаты по городам (География)"


class GeoCityVacancyShare(models.Model):
    city = models.CharField(max_length=100, verbose_name="Город")
    vacancy_share = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Доля вакансий")

    def __str__(self):
        return f"{self.city} - {self.vacancy_share}%"

    class Meta:
        verbose_name = "Доля вакансий по городам (География)"
        verbose_name_plural = "Доли вакансий по городам (География)"

# Топ 20 скиллов
class TopUXUISkills(models.Model):
    year = models.IntegerField(verbose_name="Год")
    skill = models.CharField(max_length=100, verbose_name="Навык")
    count = models.IntegerField(verbose_name="Количество упоминаний")

    def __str__(self):
        return f"{self.year} - {self.skill}"

    class Meta:
        verbose_name = "Топ UX/UI Навыков"
        verbose_name_plural = "Топ UX/UI Навыков"
        unique_together = ("year", "skill")

