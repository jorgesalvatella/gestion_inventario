# Generated by Django 5.1.6 on 2025-02-08 07:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0007_grupo_alter_inventario_grupo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignacion',
            name='inventario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='inventario.inventario'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='restaurante_destino',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='recepciones', to='inventario.restaurante'),
        ),
        migrations.AlterField(
            model_name='asignacion',
            name='restaurante_origen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='envios', to='inventario.restaurante'),
        ),
    ]
