from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('home/', views.home, name='home'),
    path('empleados/', views.listar_empleados, name='listar_empleados'),
    path('empleados/<str:rpe>/', views.detalle_empleado, name='detalle_empleado'),
    path('empleados/nuevo/', views.crear_empleado, name='crear_empleado'),
    path('equipos/', views.listar_equipos, name='listar_equipos'),
    path('equipos/<str:num_serie>/', views.detalle_equipo, name='detalle_equipo'),
    path('equipos/nuevo/', views.crear_equipo, name='crear_equipo'),
    path('asignaciones/', views.listar_asignaciones, name='listar_asignaciones'),
    path('asignaciones/nuevo/', views.crear_asignacion, name='crear_asignacion'),
    path('upload/empleados/', views.upload_empleados, name='upload_empleados'),
    path('upload/equipos/', views.upload_equipos, name='upload_equipos'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
  
    path('equipo/asignar/<int:equipo_id>/', views.crear_asignacion, name='crear_asignacion'),

    path('empleados/area/<str:clave_area>/', views.listar_empleados_por_area, name='listar_empleados_por_area'),
    path('equipos/<str:num_serie>/', views.detalle_equipo, name='detalle_equipo'),  # Asegúrate de que esto coincida con lo que necesitas
    path('reporte/clave-area/', views.reporte_por_clave_area, name='reporte_por_clave_area'),
]
