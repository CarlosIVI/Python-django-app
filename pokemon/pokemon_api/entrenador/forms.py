from django.db import models
from django.db.models import fields
from django.forms import ModelForm, widgets
from django import forms
from .models import Entrenador 


class EntrenadorForm(ModelForm):

    class Meta:
        model = Entrenador
        fields = '__all__'
        labels = {
    'nick' : 'Entrenador',
    'password' : 'Password',
    'region' : 'Region' ,
    'medallas' : 'Medallas' ,
    'batallas' : 'Batallas' ,
    'fechaRegistro' : 'Fecha de Inicio',
    'numeroPokemones': 'Pokemones'
        }

class LoginForm(ModelForm):

    class Meta:
        model = Entrenador
        exclude = ['medallas','batallas','fechaRegistro', 'nombre', 'region', 'numeroPokemones']
        labels = {
    'nick' : 'Entrenador',
    'password' : 'Contraseña'
        }
      