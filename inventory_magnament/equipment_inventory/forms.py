from django import forms
from .models import Empleado, InventarioEquipo, AsignacionEquipo
from equipment_inventory import models

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'

class InventarioEquipoForm(forms.ModelForm):
    class Meta:
        model = InventarioEquipo
        fields = '__all__'




from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()




from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class AsignacionEquipoForm(forms.ModelForm):
    class Meta:
        model = AsignacionEquipo
        fields = ['empleado', 'fecha_asignacion', 'detalles']  # No incluir 'equipo' aquí