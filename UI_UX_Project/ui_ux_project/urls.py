from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    # Основные маршруты
    path('', MainPageView.as_view(), name='main'),                      # Главная страница
    path('statistics/', StatisticsView.as_view(), name='statistics'),   # Общая статистика
    path('skills/', TopUXUISkillsView.as_view(), name='skills'),        # Навыки
    path('demand/', DemandView.as_view(), name='demand'),               # Востребованность
    path('geo/', GeoView.as_view(), name='geo'),                        # География
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),      # Последние вакансии

    # Админ-панель и аутентификация
    path('admin/', admin.site.urls),                                    # Панель администрирования
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),     # Страница входа
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),                            # Страница выхода
]

# Добавление маршрутов для работы с загружаемыми файлами
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    # Обработчик медиа-файлов
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Обработчик статических файлов
