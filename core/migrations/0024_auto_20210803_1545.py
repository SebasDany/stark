# Generated by Django 3.2.3 on 2021-08-03 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_alter_producto_sku'),
    ]

    operations = [
        migrations.AddField(
            model_name='detalle_importacion',
            name='nuevo_costo',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='detalle_importacion',
            name='total_inventario',
            field=models.IntegerField(default=0),
        ),
    ]