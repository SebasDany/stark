# Generated by Django 3.2.3 on 2021-08-12 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_alter_detalle_importacion_actualizado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='das',
            name='fecha_embarque',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='das',
            name='fecha_llegada',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='importacion',
            name='fecha',
            field=models.DateField(),
        ),
    ]
