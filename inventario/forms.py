from django import forms
from .models import Asignacion, Inventario

class AsignacionForm(forms.ModelForm):
    class Meta:
        model = Asignacion
        fields = ['inventario', 'restaurante_origen', 'restaurante_destino', 'cantidad_asignada']

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['restaurante', 'imagen', 'nombre', 'cantidad', 'material', 'marca', 'codigo', 'fecha_ingreso', 'grupo']
        widgets = {
            'fecha_ingreso': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
