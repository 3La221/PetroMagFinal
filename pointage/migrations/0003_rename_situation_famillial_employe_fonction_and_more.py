# Generated by Django 5.0.2 on 2024-02-14 14:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0002_alter_employe_id_station_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employe',
            old_name='Situation_Famillial',
            new_name='Fonction',
        ),
        migrations.RemoveField(
            model_name='employe',
            name='Date_Recruitment',
        ),
        migrations.RemoveField(
            model_name='employe',
            name='Nbr_Enfant',
        ),
        migrations.AddField(
            model_name='employe',
            name='Affect_Origin',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='employe',
            name='Date_Recrutement',
            field=models.DateField(default=datetime.datetime.now),
        ),
        migrations.AddField(
            model_name='employe',
            name='Nbr_Enfants',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='employe',
            name='Situation_Familliale',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='Adresse',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employe',
            name='Date_Detach',
            field=models.DateField(null=True),
        ),
    ]