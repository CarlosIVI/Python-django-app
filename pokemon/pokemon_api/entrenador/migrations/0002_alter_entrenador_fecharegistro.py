# Generated by Django 4.0 on 2021-12-17 00:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('entrenador', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entrenador',
            name='fechaRegistro',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
