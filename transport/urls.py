# transport/urls.py

from django.urls import path
from . import views # Импортируем представления из текущей папки

urlpatterns = [
    path('', views.index, name='index'), # URL для главной страницы
    path('vehicles/', views.vehicle_list, name='vehicle_list'), # Страница со списком ТС
    # Страница детального просмотра ТС. <int:pk> - захватывает целое число из URL и передает его как аргумент pk в представление
    path('vehicles/<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('vehicles/add/', views.vehicle_create, name='vehicle_create'), # Страница добавления ТС
    path('vehicles/<int:pk>/edit/', views.vehicle_update, name='vehicle_update'), # Страница редактирования ТС
    path('vehicles/<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'), # Страница удаления ТС (подтверждение)
]