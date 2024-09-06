from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import IntegrityError
from django.forms import DurationField, ValidationError

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Empleado, InventarioEquipo, AsignacionEquipo
from .forms import  AsignacionEquipoForm, EmpleadoForm, InventarioEquipoForm,  CSVUploadForm
import csv
import chardet
from django.db.models import Q
from django.core.paginator import Paginator
from equipment_inventory import models
from django.db.models import Count, Sum

import logging

# Configura el logger para usar el nombre del módulo actual
logger = logging.getLogger(__name__)



def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'equipment_inventory/crear_empleado.html', {'form': form})

@login_required
def listar_equipos(request):
    query = request.GET.get('q')
    if query:
        equipos = InventarioEquipo.objects.filter(
            Q(num_serie__icontains=query) | Q(num_inventario__icontains=query) |
            Q(num_activo__icontains=query) | Q(marca__icontains=query) |
            Q(modelo__icontains=query) | Q(tipo__icontains=query)
        ).order_by('id')  # Ordena los resultados para evitar inconsistencias en la paginación
    else:
        equipos = InventarioEquipo.objects.all()
    
    paginator = Paginator(equipos, 10)  # Mostrar 10 equipos por página
    page = request.GET.get('page')
    try:
        equipos = paginator.page(page)
    except PageNotAnInteger:
        equipos = paginator.page(1)
    except EmptyPage:
        equipos = paginator.page(paginator.num_pages)
    
    return render(request, 'equipment_inventory/listar_equipos.html', {'equipos': equipos})


@login_required
def detalle_equipo(request, num_serie):
    equipo = get_object_or_404(InventarioEquipo, num_serie=num_serie)
    asignacion = AsignacionEquipo.objects.filter(equipo=equipo).last()  # Obtén la asignación actual, si existe
    #asignacion = AsignacionEquipo.objects.filter(equipo=equipo).exists()  # Verifica si el equipo está asignado
    print("Asignación encontrada:", asignacion)
    print("Empleado asignado:", asignacion.empleado.nombre if asignacion else "Ninguno")
    return render(request, 'equipment_inventory/detalle_equipo.html', {
        'equipo': equipo,
        'asignado': asignacion,
    })

@login_required
def crear_equipo(request):
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_equipos')
    else:
        form = InventarioEquipoForm()
    return render(request, 'equipment_inventory/crear_equipo.html', {'form': form})

@login_required
def listar_asignaciones(request):
    query = request.GET.get('q')
    if query:
        asignaciones = AsignacionEquipo.objects.select_related('empleado', 'equipo').filter(
            Q(empleado__nombre__icontains=query) | Q(empleado__rpe__icontains=query) | 
            Q(equipo__num_serie__icontains=query)
        ).order_by('empleado')
    else:
        asignaciones = AsignacionEquipo.objects.select_related('empleado', 'equipo').order_by('empleado')
    
    paginator = Paginator(asignaciones, 10)  # Mostrar 10 asignaciones por página
    page = request.GET.get('page')
    try:
        asignaciones = paginator.page(page)
    except PageNotAnInteger:
        asignaciones = paginator.page(1)
    except EmptyPage:
        asignaciones = paginator.page(paginator.num_pages)
    
    context = {
        'asignaciones': asignaciones
    }
    return render(request, 'equipment_inventory/listar_asignaciones.html', context)


#*********************** CREAR ASIGNACION ***********************

@login_required
@login_required
def crear_asignacion(request, equipo_id):
    equipo = get_object_or_404(InventarioEquipo, pk=equipo_id)
    form = AsignacionEquipoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            asignacion = form.save(commit=False)
            asignacion.equipo = equipo
            
            try:
                asignacion.save()
                # Mensaje de éxito después de una asignación correcta
                messages.success(request, f"El equipo {equipo.num_serie} ha sido asignado correctamente a {asignacion.empleado.nombre}.")
                return redirect('detalle_equipo', num_serie=equipo.num_serie)  # Redirige a la vista de detalle del equipo
            except IntegrityError:
                form.add_error(None, "Este equipo ya ha sido asignado a otro empleado.")
                messages.error(request, "Este equipo ya ha sido asignado a otro empleado.")
            except ValidationError as e:
                form.add_error(None, e)
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f"Error técnico al crear la asignación: {e}")
        else:
            messages.error(request, "Por favor, corrija los errores en el formulario.")

    return render(request, 'equipment_inventory/crear_asignacion.html', {'form': form, 'equipo': equipo})



#************** FIN CREAR ASIGNACION ******************************************



def homepage(request):
    return render(request, 'equipment_inventory/home.html')


@login_required
def home(request):
    return render(request, 'equipment_inventory/home.html')

def upload_empleados(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Detectar la codificación del archivo
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            csv_file.seek(0)  # Volver al inicio del archivo después de leerlo
            
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                for row in reader:
                    Empleado.objects.create(
                        rpe=row['rpe'],
                        nombre=row['nombre'],
                        fecha_antiguedad=row['fecha_antiguedad'],
                        tc=row['tc'],
                        numero_plaza=row['numero_plaza'],
                        clave_categoria=row['clave_categoria'],
                        descripcion_categoria=row['descripcion_categoria'],
                        ts=row['ts'],
                        fecha_ocupacion=row['fecha_ocupacion'],
                        clave_area=row['clave_area'],
                        area_adscripcion=row['area_adscripcion'],
                        clave_area_t=row['clave_area_t'],
                        descripcion_area_t=row['descripcion_area_t'],
                        email=row['email'],
                        telefono=row['email'],
                    )
                messages.success(request, 'Empleados cargados exitosamente.')
                return redirect('listar_empleados')
            except KeyError as e:
                messages.error(request, f'Error en el archivo CSV: no se encontró la columna {str(e)}.')
                return redirect('upload_empleados')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo CSV: {str(e)}.')
                return redirect('upload_empleados')
    else:
        form = CSVUploadForm()
    return render(request, 'equipment_inventory/upload_csv.html', {'form': form, 'titulo': 'Empleados'})

def upload_equipos(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            # Detectar la codificación del archivo
            raw_data = csv_file.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            csv_file.seek(0)  # Volver al inicio del archivo después de leerlo
            
            decoded_file = raw_data.decode(encoding).splitlines()
            reader = csv.DictReader(decoded_file)
            try:
                for row in reader:
                    InventarioEquipo.objects.create(
                        num_serie=row['num_serie'],
                        num_inventario=row['num_inventario'],
                        num_activo=row['num_activo'],
                        marca=row['marca'],
                        modelo=row['modelo'],
                        tipo=row['tipo'],
                        especificaciones=row['especificaciones'],
                        fecha_adquisicion=row['fecha_adquisicion'],
                        estado=row['estado'],
                        ip=row['ip'],
                        nombre_equipo=row['nombre_equipo'],
                    )
                messages.success(request, 'Equipos cargados exitosamente.')
                return redirect('listar_equipos')
            except KeyError as e:
                messages.error(request, f'Error en el archivo CSV: no se encontró la columna {str(e)}.')
                return redirect('upload_equipos')
            except Exception as e:
                messages.error(request, f'Ocurrió un error al procesar el archivo CSV: {str(e)}.')
                return redirect('upload_equipos')
    else:
        form = CSVUploadForm()
    return render(request, 'equipment_inventory/upload_csv.html', {'form': form, 'titulo': 'Equipos'})

#Listar Empleados ------------------------*****************************

@login_required
def listar_empleados(request):
    query = request.GET.get('q')
    
    if query:
        # Primero, buscamos si el usuario ingresó "Confianza" o "Base"
        if query.lower() == 'confianza':
            empleados = Empleado.objects.filter(tc='1')
        elif query.lower() == 'base':
            empleados = Empleado.objects.filter(tc='6')
        else:
            # Filtro general para otros campos
            empleados = Empleado.objects.filter(
                Q(rpe__icontains=query) |
                Q(nombre__icontains=query) |
                Q(clave_area__icontains=query) |
                Q(numero_plaza__icontains=query) |
                Q(clave_categoria__icontains=query)
            )
    else:
        empleados = Empleado.objects.all()
    
    paginator = Paginator(empleados, 10)  # Pagina los resultados a 10 empleados por página
    page = request.GET.get('page')
    try:
        empleados = paginator.page(page)
    except PageNotAnInteger:
        empleados = paginator.page(1)
    except EmptyPage:
        empleados = paginator.page(paginator.num_pages)
    
    return render(request, 'equipment_inventory/listar_empleados.html', {'empleados': empleados})




def detalle_empleado(request, rpe):
    empleado = get_object_or_404(Empleado, rpe=rpe)
    asignaciones = empleado.asignaciones.all()  # Accede a todas las asignaciones del empleado
    return render(request, 'equipment_inventory/detalle_empleado.html', {
        'empleado': empleado,
        'asignaciones': asignaciones
    })






@login_required
def listar_empleados_por_area(request, clave_area):
    # Reemplaza guiones bajos por espacios
    clave_area = clave_area.replace('_', ' ')  
    # Obtiene el término de búsqueda desde el formulario
    query = request.GET.get('q')
    
    if query:
        empleados = Empleado.objects.filter(
            Q(clave_area__icontains=query) |
            Q(numero_plaza__icontains=query) |
            Q(clave_categoria__icontains=query) |
            Q(nombre__icontains=query) |
            Q(rpe__icontains=query)
        )
    else:
        # Si no hay término de búsqueda, filtra solo por clave_area
        empleados = Empleado.objects.filter(clave_area=clave_area)
    
    return render(request, 'equipment_inventory/listar_empleados_por_area.html', {'empleados': empleados, 'clave_area': clave_area})


# ************************  Reporte por Clave de Area *******************************
from django.db.models import Count, Q, F, ExpressionWrapper, DurationField
from datetime import date
from dateutil.relativedelta import relativedelta

#************************************************************************************

@login_required
def reporte_por_clave_area(request):
    query = request.GET.get('q', '')
    antiguedad_filtro = request.GET.get('antiguedad', '')

    empleados = Empleado.objects.all()
    if query:
        empleados = empleados.filter(
            Q(clave_area__icontains=(query)) |
            Q(rpe__icontains=(query)) |
            Q(nombre__icontains=(query))
        ).order_by('clave_area')

    empleados_filtrados = []
    for empleado in empleados:
        if empleado.fecha_antiguedad:
            hoy = date.today()
            diferencia = relativedelta(hoy, empleado.fecha_antiguedad)
            empleado.anios_antiguedad = diferencia.years
            empleado.meses_antiguedad = diferencia.months
            empleado.dias_antiguedad = diferencia.days

            # Filtrar empleados que tienen exactamente el número de años de antigüedad
            if antiguedad_filtro:
                if empleado.anios_antiguedad == int(antiguedad_filtro):
                    empleados_filtrados.append(empleado)
            else:
                empleados_filtrados.append(empleado)
        else:
            empleado.anios_antiguedad = empleado.meses_antiguedad = empleado.dias_antiguedad = None
            empleados_filtrados.append(empleado)

    # Calcular el número total de empleados por clave_area
    empleados_por_area = Empleado.objects.filter(id__in=[e.id for e in empleados_filtrados]).values('clave_area').annotate(total=Count('id')).order_by('clave_area')

    total_general = len(empleados_filtrados)

    return render(request, 'equipment_inventory/reporte_por_clave_area.html', {
        'empleados': empleados_filtrados,
        'empleados_por_area': empleados_por_area,
        'query': query,
        'antiguedad_filtro': antiguedad_filtro,
        'total_general': total_general
    })
