# transport/models.py

from django.db import models

# Модель: Тип транспортного средства (связанная таблица 1)
class VehicleType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название типа")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тип транспортного средства"
        verbose_name_plural = "Типы транспортных средств"

    def __str__(self):
        return self.name

# Модель: Водитель (связанная таблица 2)
class Driver(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Номер ВУ")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Номер телефона")
    hire_date = models.DateField(verbose_name="Дата приема на работу")

    class Meta:
        verbose_name = "Водитель"
        verbose_name_plural = "Водители"
        ordering = ['last_name', 'first_name'] # Сортировка по умолчанию

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель: Транспортное средство (ключевая таблица)
class Vehicle(models.Model):
    make = models.CharField(max_length=100, verbose_name="Марка")
    model = models.CharField(max_length=100, verbose_name="Модель")
    year = models.PositiveSmallIntegerField(verbose_name="Год выпуска")
    license_plate = models.CharField(max_length=20, unique=True, verbose_name="Госномер")
    vin = models.CharField(max_length=17, unique=True, blank=True, null=True, verbose_name="VIN")
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Тип ТС") # Связь Many-to-One с VehicleType
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Назначенный водитель") # Связь Many-to-One с Driver (может быть None)
    status = models.CharField(
        max_length=50,
        choices=[
            ('active', 'Активен'),
            ('in_repair', 'В ремонте'),
            ('retired', 'Списан'),
            ('idle', 'Простаивает'),
        ],
        default='active',
        verbose_name="Статус"
    )
    acquisition_date = models.DateField(verbose_name="Дата приобретения")
    mileage = models.PositiveIntegerField(default=0, verbose_name="Пробег (км)")

    class Meta:
        verbose_name = "Транспортное средство"
        verbose_name_plural = "Транспортные средства"
        ordering = ['license_plate'] # Сортировка по умолчанию

    def __str__(self):
        return f"{self.make} {self.model} ({self.license_plate})"

    # Добавим метод для отображения в админке или шаблонах
    # @admin.display(description="Водитель") # Можно использовать декоратор вместо short_description
    def display_driver(self):
        return self.driver if self.driver else "Не назначен"
    display_driver.short_description = "Водитель" # Название колонки в админке

    # @admin.display(boolean=True, description="В ремонте?") # Можно использовать декоратор
    def is_in_repair(self):
        return self.status == 'in_repair'
    is_in_repair.boolean = True # Отображать как галочку в админке
    is_in_repair.short_description = "В ремонте?"


# Модель: Запись о техническом обслуживании/ремонте (связанная таблица 3)
class MaintenanceRecord(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name="Транспортное средство") # Связь Many-to-One с Vehicle. related_name позволяет получать записи из Vehicle: vehicle.maintenance_records.all()
    date = models.DateField(verbose_name="Дата")
    description = models.TextField(verbose_name="Описание работ")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Стоимость")
    record_type = models.CharField(
        max_length=50,
        choices=[
            ('maintenance', 'Техническое обслуживание'),
            ('repair', 'Ремонт'),
            ('inspection', 'Осмотр'),
        ],
        verbose_name="Тип записи"
    )
    notes = models.TextField(blank=True, verbose_name="Примечания")

    class Meta:
        verbose_name = "Запись о ТО/Ремонте"
        verbose_name_plural = "Записи о ТО/Ремонте"
        ordering = ['-date'] # Сортировка по дате (новые сверху)

    def __str__(self):
        # Убедимся, что vehicle существует, прежде чем обращаться к license_plate
        vehicle_info = self.vehicle.license_plate if self.vehicle else "Неизвестное ТС"
        return f"ТО/Ремонт для {vehicle_info} от {self.date}"