# Generated by Django 4.0 on 2021-12-18 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Preguntas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pregunta', models.CharField(max_length=100)),
                ('respuestaCorrecta', models.CharField(max_length=100)),
                ('respuestaIncorrecta1', models.CharField(max_length=100)),
                ('respuestaIncorrecta2', models.CharField(max_length=100)),
            ],
        ),
    ]
