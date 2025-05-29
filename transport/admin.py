# transport/admin.py

from django.contrib import admin
from .models import VehicleType, Driver, Vehicle, MaintenanceRecord

# Регистрация модели Тип ТС
@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description') # Какие поля отображать в списке
    search_fields = ('name',) # По каким полям искать

# Регистрация модели Водитель
@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license_number', 'phone_number', 'hire_date')
    list_filter = ('hire_date',) # По каким полям фильтровать
    search_fields = ('first_name', 'last_name', 'license_number')
    date_hierarchy = 'hire_date' # Иерархия дат для навигации по дате приема

# Inline для записей о ТО (будет отображаться на странице ТС)
class MaintenanceRecordInline(admin.TabularInline): # TabularInline или StackedInline
    model = MaintenanceRecord
    extra = 0 # Сколько пустых форм отображать по умолчанию
    fields = ('date', 'record_type', 'description', 'cost', 'notes') # Поля для отображения/редактирования в инлайне
    # readonly_fields = () # Поля только для чтения в инлайне (пока нет таких)


# Регистрация модели Транспортное средство
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    # list_display (+использование внутри list_display собственного метода)
    list_display = ('license_plate', 'make', 'model', 'year', 'vehicle_type', 'display_driver', 'status', 'is_in_repair')

    # list_display_links - какие поля в list_display будут ссылками на объект
    list_display_links = ('license_plate', 'make', 'model') # Сделаем несколько полей ссылками

    # list_filter - фильтры справа
    list_filter = ('vehicle_type', 'status', 'year')

    # search_fields - поля для поиска
    search_fields = ('license_plate', 'vin', 'make', 'model', 'driver__first_name', 'driver__last_name') # Можно искать по полям связанных моделей (driver__first_name)

    # date_hierarchy - иерархия дат
    date_hierarchy = 'acquisition_date'

    # inlines - связанные объекты прямо на странице редактирования родительского объекта
    inlines = [MaintenanceRecordInline] # Здесь подключаем инлайн для записей о ТО

    # raw_id_fields - для ForeignKey/ManyToMany полей, где много объектов, отображает только ID вместо выпадающего списка
    # raw_id_fields = ('driver', 'vehicle_type') # Можно использовать, если много водителей/типов

    # readonly_fields - поля только для чтения на странице редактирования
    # readonly_fields = ('acquisition_date',) # Пример: сделать дату приобретения только для чтения после создания

    # filter_horizontal - для ManyToMany полей, удобный виджет выбора (у нас пока нет ManyToMany)
    # filter_horizontal = ('some_m2m_field',)

    # fieldsets - группировка полей на странице редактирования (опционально, для организации)
    # fieldsets = (
    #     (None, {
    #         'fields': (('make', 'model', 'year'), ('license_plate', 'vin'), ('vehicle_type', 'driver'), 'status')
    #     }),
    #     ('Дополнительная информация', {
    #         'fields': ('acquisition_date', 'mileage',),
    #         'classes': ('collapse',), # Скрывает блок по умолчанию
    #     }),
    # )

# Регистрация модели Запись о ТО/Ремонте (можно зарегистрировать отдельно, если не только через инлайн)
@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'record_type', 'cost', 'description')
    list_filter = ('record_type', 'date', 'vehicle__vehicle_type') # Фильтр по типу записи, дате, и типу ТС
    search_fields = ('description', 'notes', 'vehicle__license_plate', 'vehicle__make', 'vehicle__model') # Поиск по описанию, примечаниям, госномеру ТС, марке, модели
    date_hierarchy = 'date'
    # Поле vehicle будет выпадающим списком, raw_id_fields может быть полезно:
    # raw_id_fields = ('vehicle',)