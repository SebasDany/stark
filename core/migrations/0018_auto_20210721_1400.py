# Generated by Django 3.2.3 on 2021-07-21 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_das_pais_procedncia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='das',
            name='fecha_embarque',
            field=models.DateField(help_text='Ejemplo: 2021-07-07'),
        ),
        migrations.AlterField(
            model_name='das',
            name='fecha_llegada',
            field=models.DateField(help_text='Ejemplo: 2021-07-07'),
        ),
    ]
