# Generated by Django 5.0.2 on 2024-02-21 08:36

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0011_profile_delete_chef_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('ID', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('Description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='employe',
            name='Date_Recrutement',
            field=models.DateField(default=datetime.date(2024, 2, 21)),
        ),
        migrations.CreateModel(
            name='Code_Employe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.datetime(2024, 2, 21, 9, 36, 40, 762005))),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pointage.code')),
                ('employe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_emp', to='pointage.profile')),
            ],
        ),
    ]
