# Generated by Django 5.0.6 on 2024-08-21 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipment_inventory', '0006_remove_empleado_ubicacion_empleado_apellido_materno_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empleado',
            old_name='nombramiento',
            new_name='area_adscripcion',
        ),
        migrations.RenameField(
            model_name='empleado',
            old_name='categoria_descripcion',
            new_name='descripcion_categoria',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='adscripcion',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='apellido_materno',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='apellido_paterno',
        ),
        migrations.RemoveField(
            model_name='empleado',
            name='area_trabajo',
        ),
        migrations.AddField(
            model_name='empleado',
            name='clave_area',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='clave_area_t',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='clave_categoria',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='descrpcion_area_t',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='fecha_ocupacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='numero_plaza',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='empleado',
            name='ts',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='empleado',
            name='rpe',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
