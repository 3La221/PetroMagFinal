# Generated by Django 5.0.2 on 2024-02-14 00:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employe',
            name='ID_Station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pointage.chef_station'),
        ),
        migrations.RemoveField(
            model_name='chef_station',
            name='ID_Station',
        ),
        migrations.DeleteModel(
            name='Station',
        ),
    ]
