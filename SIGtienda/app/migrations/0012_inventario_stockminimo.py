# Generated by Django 5.1.6 on 2025-06-03 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_proveedor_calificacion_proveedor_comentarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventario',
            name='stockMinimo',
            field=models.IntegerField(default=0),
        ),
    ]
