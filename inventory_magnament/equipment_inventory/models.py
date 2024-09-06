from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import UniqueConstraint

    

class Empleado(models.Model):
    TC_CHOICES = [
        ('1', 'Confianza'),
        ('6', 'Base'),
    ]
   

    rpe = models.CharField(max_length=5, unique=True)
    nombre = models.CharField(max_length=200)
    fecha_antiguedad = models.DateField(null=True, blank=True)
    tc = models.CharField(max_length=2, choices=TC_CHOICES, null=True, blank=True)
    numero_plaza = models.CharField(max_length=50, null=True, blank=True)
    clave_categoria = models.CharField(max_length=50, null=True, blank=True)
    descripcion_categoria = models.CharField(max_length=200, null=True, blank=True)
    ts = models.CharField(max_length=50, null=True, blank=True)
    fecha_ocupacion = models.DateField(null=True, blank=True)
    clave_area = models.CharField(max_length=50, null=True, blank=True)
    area_adscripcion = models.TextField(null=True, blank=True)
    clave_area_t = models.TextField(null=True, blank=True)
    descripcion_area_t = models.TextField(null=True, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15, default="")
   

    def __str__(self):
        return f"{self.nombre} {self.numero_plaza} {self.area_adscripcion}"
    

class InventarioEquipo(models.Model):
    MARCA_CHOICES = [
        ('HP', 'HP'),
        ('Dell', 'Dell'),
        ('Lenovo', 'Lenovo'),
    ]

    MODELO_CHOICES = [
        ('ThinkCentre', 'ThinkCentre'),
        ('HP Prodesk 600 G6', 'HP Prodesk 600 G6'),
        ('Probook 440 G7', 'Probook 440 G7'),
        ('ThinkPad', 'ThinkPad'),
    ]

    TIPO_CHOICES = [
        ('Laptop', 'Laptop'),
        ('Desktop', 'Desktop'),
    ]

    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('usado', 'Usado'),
        ('dado de baja', 'Dado de baja'),
    ]

    UBICACION_CHOICES = [
        ('Departamento Compras', 'Departamento Compras'),
        ('Departamento Almacenes y Trafico', 'Departamento Almacenes y Trafico'),
        ('Departamento Proveedores', 'Departamento Proveedores'),
        ('Soporte Tecnico', 'Soporte Tecnico'),
        ('Auxiliaria General', 'Auxiliaria General'),
    ]

    num_serie = models.CharField(max_length=50, unique=True)
    num_inventario = models.CharField(max_length=25, default=0)
    num_activo = models.CharField(max_length=25, default=0)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    especificaciones = models.TextField(blank=True)
    fecha_adquisicion = models.DateField()
    estado = models.CharField(max_length=50, default='nuevo')
    ip = models.GenericIPAddressField(protocol='both', unpack_ipv4=True, blank=True, null=True)
    nombre_equipo = models.CharField(max_length=100, default='Equipo Desconocido')  # Define un valor predeterminado aquí

    def __str__(self):
        return self.num_serie
    
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _





    
    
class AsignacionEquipo(models.Model):
    empleado = models.ForeignKey('Empleado', on_delete=models.CASCADE, related_name='asignaciones')
    equipo = models.ForeignKey('InventarioEquipo', on_delete=models.CASCADE, related_name='asignaciones')
    fecha_asignacion = models.DateField()
    detalles = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['equipo'], name='unique_equipo_asignado')  # Asegura que cada equipo solo pueda ser asignado una vez.
        ]

    #def clean(self):
     #   if not self.equipo_id:  # Verifica si el equipo está asignado
       #     raise ValidationError("El equipo debe estar asignado antes de validar.")
       # if AsignacionEquipo.objects.filter(equipo=self.equipo).exclude(id=self.id).exists():
        #    raise ValidationError("Este equipo ya está asignado a otro empleado.")