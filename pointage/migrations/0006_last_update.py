# Generated by Django 5.0.2 on 2024-02-16 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pointage', '0005_alter_employe_id_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='Last_Update',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
            ],
        ),
    ]
