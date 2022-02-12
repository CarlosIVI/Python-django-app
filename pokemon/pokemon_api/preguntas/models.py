from django.db import models
from django.db.models.fields import BooleanField, CharField, DateField, IntegerField, PositiveSmallIntegerField

# Create your models here.
class Preguntas(models.Model):  
    pregunta = CharField(max_length=100)
    respuestaCorrecta = CharField (max_length=100)
    respuestaIncorrecta1 = CharField (max_length=100)
    respuestaIncorrecta2 = CharField (max_length=100)