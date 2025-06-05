# transport/views.py

from django.shortcuts import render, get_object_or_404, redirect  # Добавляем get_object_or_404 и redirect
from django.urls import reverse  # Для получения URL по имени (необязательно для этого примера, но полезно)
from .models import Vehicle, MaintenanceRecord, Driver, VehicleType
from .forms import VehicleForm  # Импортируем форму


def index(request):
    total_vehicles = Vehicle.objects.count()
    vehicles_in_repair = Vehicle.objects.filter(status='in_repair').count()
    vehicles_active = Vehicle.objects.filter(status='active').count()

    # Задача 2: Последние записи о ТО/Ремонте
    latest_maintenance = MaintenanceRecord.objects.order_by('-date')[:5].select_related(
        'vehicle')  # Получаем 5 последних записей, оптимизируем запрос
    # Добавил select_related('vehicle'), чтобы избежать N+1 запросов при доступе к record.vehicle в шаблоне

    # Задача 3: Список водителей с назначенными ТС
    # Можно получить список всех ТС и отобразить их водителей
    vehicles_list = Vehicle.objects.select_related('driver',
                                                   'vehicle_type').all()  # Получаем все ТС, связанные типы и водителей

    context = {
        'total_vehicles': total_vehicles,
        'vehicles_in_repair': vehicles_in_repair,
        'vehicles_active': vehicles_active,
        'latest_maintenance': latest_maintenance,
        'vehicles_list': vehicles_list,  # Передаем список ТС для отображения водителей
    }
    return render(request, 'transport/index.html', context)  # Рендерим шаблон index.html, передавая контекст


def vehicle_list(request):
    """Представление для списка всех транспортных средств"""
    vehicles = Vehicle.objects.select_related('vehicle_type',
                                              'driver').all()  # Получаем все ТС с связанными типами и водителями
    context = {
        'vehicles': vehicles
    }
    return render(request, 'transport/vehicle_list.html', context)


def vehicle_detail(request, pk):
    """Представление для детальной страницы транспортного средства"""
    # Получаем объект Vehicle по его первичному ключу (pk) или возвращаем 404 ошибку
    # Используем select_related для оптимизации доступа к vehicle_type и driver
    vehicle = get_object_or_404(Vehicle.objects.select_related('vehicle_type', 'driver'), pk=pk)
    # Получаем все связанные записи о ТО для этого ТС (используем related_name='maintenance_records')
    maintenance_records = vehicle.maintenance_records.all()  # Этот запрос будет выполнен отдельно, но обычно записей о ТО меньше, чем ТС

    context = {
        'vehicle': vehicle,
        'maintenance_records': maintenance_records,
    }
    return render(request, 'transport/vehicle_detail.html', context)


def vehicle_create(request):
    """Представление для добавления нового ТС"""
    if request.method == 'POST':
        form = VehicleForm(request.POST)  # Создаем форму, заполняя ее данными из POST-запроса
        if form.is_valid():  # Проверяем, валидны ли данные в форме
            vehicle = form.save()  # Сохраняем новый объект в БД
            return redirect('vehicle_detail', pk=vehicle.pk)  # Перенаправляем на страницу созданного ТС
    else:
        form = VehicleForm()  # Создаем пустую форму для GET-запроса

    context = {
        'form': form,
        'title': 'Добавить транспортное средство'
    }
    return render(request, 'transport/vehicle_form.html', context)


def vehicle_update(request, pk):
    """Представление для редактирования ТС"""
    vehicle = get_object_or_404(Vehicle, pk=pk)  # Получаем существующий объект

    if request.method == 'POST':
        form = VehicleForm(request.POST,
                           instance=vehicle)  # Создаем форму, заполняя ее POST-данными и привязывая к существующему объекту
        if form.is_valid():
            form.save()  # Сохраняем изменения в БД
            return redirect('vehicle_detail', pk=vehicle.pk)  # Перенаправляем на страницу обновленного ТС
    else:
        form = VehicleForm(instance=vehicle)  # Создаем форму, предзаполняя ее данными из объекта

    context = {
        'form': form,
        'vehicle': vehicle,
        # Передаем объект для отображения какой-то инфо на странице редактирования (например, госномер в заголовке)
        'title': f'Редактировать ТС: {vehicle.license_plate}'
    }
    return render(request, 'transport/vehicle_form.html', context)  # Используем тот же шаблон формы


def vehicle_delete(request, pk):

    vehicle = get_object_or_404(Vehicle, pk=pk)

    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_list')


    context = {
        'vehicle': vehicle
    }
    return render(request, 'transport/vehicle_confirm_delete.html', context)


from django.shortcuts import render


