from django.contrib import admin
from .models import Empleado, InventarioEquipo, AsignacionEquipo


admin.site.site_header= 'Admin. Equip.Gab'



class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['rpe', 'nombre', 'fecha_antiguedad', 'tc',  'numero_plaza', 'clave_categoria', 'descripcion_categoria', 'area_adscripcion']

     # Agregar campos que se pueden buscar
    search_fields = ('rpe', 'nombre', 'tc', 'clave_categoria', 'descripcion_categoria')




class InventarioEquipoAdmin(admin.ModelAdmin):
    list_display = ['num_serie', 'num_inventario', 'num_activo', 'marca', 'modelo', 'tipo', 'especificaciones', 'fecha_adquisicion', 'estado', 'ip', 'nombre_equipo']
    search_fields = ['num_serie', 'num_inventario', 'num_activo']
    list_filter = ['marca', 'modelo', 'tipo', 'estado']

class AsignacionEquipoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'equipo', 'fecha_asignacion', 'detalles']
    search_fields = ['empleado__nombre', 'equipo__num_serie']
    list_filter = ['fecha_asignacion', 'empleado', 'equipo']

admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(InventarioEquipo, InventarioEquipoAdmin)
admin.site.register(AsignacionEquipo, AsignacionEquipoAdmin)
