# transport/forms.py

from django import forms
from .models import Vehicle, VehicleType, Driver

class VehicleForm(forms.ModelForm):
    # Можно добавить дополнительные настройки или поля формы здесь, если нужно
    # Например, если нужно кастомизировать виджеты:
    # acquisition_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Vehicle # Связываем форму с моделью Vehicle
        # fields = '__all__' # Включает все поля модели в форму
        # Или явно указываем, какие поля включить (лучше для контроля)
        fields = [
            'make',
            'model',
            'year',
            'license_plate',
            'vin',
            'vehicle_type',
            'driver',
            'status',
            'acquisition_date',
            'mileage',
        ]
        # exclude = ['field_name'] # Исключить определенные поля

        # Можно добавить виджеты или классы CSS для полей
        widgets = {
             'acquisition_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), # Добавляем класс Bootstrap
             'vehicle_type': forms.Select(attrs={'class': 'form-select'}), # Класс Bootstrap для select
             'driver': forms.Select(attrs={'class': 'form-select'}),
             'status': forms.Select(attrs={'class': 'form-select'}),
             'make': forms.TextInput(attrs={'class': 'form-control'}),
             'model': forms.TextInput(attrs={'class': 'form-control'}),
             'year': forms.NumberInput(attrs={'class': 'form-control'}),
             'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
             'vin': forms.TextInput(attrs={'class': 'form-control'}),
             'mileage': forms.NumberInput(attrs={'class': 'form-control'}),

        }
        # Добавляем verbose_name в help_text, чтобы они отображались рядом с полем в случае использования form.as_p или ручного вывода без label
        # help_texts = {
        #     field: model._meta.get_field(field).verbose_name for field in fields
        # }
        # Этот help_text может дублировать label при ручном выводе, используйте осторожно.