# transport/admin.py

from django.contrib import admin
from .models import VehicleType, Driver, Vehicle, MaintenanceRecord


@admin.register(VehicleType)
class VehicleTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'license_number', 'phone_number', 'hire_date')
    list_filter = ('hire_date',)
    search_fields = ('first_name', 'last_name', 'license_number')
    date_hierarchy = 'hire_date'


class MaintenanceRecordInline(admin.TabularInline):
    model = MaintenanceRecord
    extra = 0
    fields = ('date', 'record_type', 'description', 'cost', 'notes')



@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = ('license_plate', 'make', 'model', 'year', 'vehicle_type', 'display_driver', 'status', 'is_in_repair')


    list_display_links = ('license_plate', 'make', 'model')


    list_filter = ('vehicle_type', 'status', 'year')


    search_fields = ('license_plate', 'vin', 'make', 'model', 'driver__first_name', 'driver__last_name')


    date_hierarchy = 'acquisition_date'


    inlines = [MaintenanceRecordInline]

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'date', 'record_type', 'cost', 'description')
    list_filter = ('record_type', 'date', 'vehicle__vehicle_type')
    search_fields = ('description', 'notes', 'vehicle__license_plate', 'vehicle__make', 'vehicle__model')
    date_hierarchy = 'date'
