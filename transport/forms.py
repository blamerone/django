# transport/forms.py

from django import forms
from .models import Vehicle, VehicleType, Driver

class VehicleForm(forms.ModelForm):

    class Meta:
        model = Vehicle

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



        widgets = {
             'acquisition_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
             'vehicle_type': forms.Select(attrs={'class': 'form-select'}),
             'driver': forms.Select(attrs={'class': 'form-select'}),
             'status': forms.Select(attrs={'class': 'form-select'}),
             'make': forms.TextInput(attrs={'class': 'form-control'}),
             'model': forms.TextInput(attrs={'class': 'form-control'}),
             'year': forms.NumberInput(attrs={'class': 'form-control'}),
             'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
             'vin': forms.TextInput(attrs={'class': 'form-control'}),
             'mileage': forms.NumberInput(attrs={'class': 'form-control'}),

        }
