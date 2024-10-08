# Generated by Django 5.0.6 on 2024-06-20 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rpe', models.CharField(max_length=5, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('adscripcion', models.CharField(max_length=100)),
                ('ubicacion', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombramiento', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='InventarioEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_inventario', models.CharField(default=0, max_length=25)),
                ('num_activo', models.CharField(default=0, max_length=25)),
                ('num_serie', models.CharField(max_length=50, unique=True)),
                ('marca', models.CharField(choices=[('HP', 'HP'), ('Dell', 'Dell'), ('Lenovo', 'Lenovo')], max_length=100)),
                ('modelo', models.CharField(choices=[('Modelo1', 'Modelo1'), ('Modelo2', 'Modelo2')], max_length=100)),
                ('tipo', models.CharField(choices=[('Laptop', 'Laptop'), ('Desktop', 'Desktop')], max_length=50)),
                ('especificaciones', models.TextField(blank=True)),
                ('fecha_adquisicion', models.DateField()),
                ('estado', models.CharField(choices=[('nuevo', 'Nuevo'), ('usado', 'Usado'), ('dado de baja', 'Dado de baja')], default='nuevo', max_length=50)),
                ('ubicacion', models.CharField(choices=[('Oficina1', 'Oficina1'), ('Oficina2', 'Oficina2')], max_length=100)),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='equipment_inventory.empleado')),
            ],
        ),
        migrations.CreateModel(
            name='AsignacionEquipo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_asignacion', models.DateField()),
                ('fecha_devolucion', models.DateField(blank=True, null=True)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment_inventory.empleado')),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='equipment_inventory.inventarioequipo')),
            ],
        ),
    ]
