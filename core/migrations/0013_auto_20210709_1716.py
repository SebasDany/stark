# Generated by Django 3.2.3 on 2021-07-09 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210707_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='importacion',
            name='estado',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='importacion',
            name='tipo',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
