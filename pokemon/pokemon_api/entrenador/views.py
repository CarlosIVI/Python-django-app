import entrenador
from entrenador.service import get_pokemon_list
from .models import Entrenador , EntrenadorPokemones
from .forms import *
from django.shortcuts import  render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EntrenadorSerializer
from rest_framework import status
from django.http import Http404

def listar(r):
    context = {
        "entrenadores": Entrenador.objects.all()
    }
    return render(r, "entrenador/listar.html", context)

def login(r):
    formulario =  LoginForm(r.POST)
    context = {
         "formulario" :formulario,
    }
    if r.POST:
        formulario = LoginForm(r.POST)
        try:
            miEntrenador=Entrenador.objects.get(nick=formulario['nick'].value()) 
            try:
                if miEntrenador.password == formulario['password'].value():
                    return redirect("listar")
            except:
                return render(r, "entrenador/login.html", context)
        except:
            print('NO FUNCIONA')
            return render(r, "entrenador/login.html", context)
    return render(r, "entrenador/login.html", context)
    
            
    

def listarPokemones(r, id):
    entrenador = Entrenador.objects.get(pk=id)
    pokemones = EntrenadorPokemones.objects.filter(entrenador=entrenador) ##regresa el join con la tabla asignatura
    
    context = {  
        "pokemones" : pokemones
      }
    return render(r, "entrenador/listar_pokemones.html", context)

def crear(r):

    formulario =  EntrenadorForm()
    context = {
        "formulario" :formulario,
    }

    if r.POST:
        formulario = EntrenadorForm(r.POST)
        formulario.save()

        return redirect("listar")

    return render(r, "entrenador/register.html", context)

class Entrenador_APIView(APIView):
    def get_object(self, pk):
        try:
            return Entrenador.objects.get(pk=pk)
        except Entrenador.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        entrenador = self.get_object(pk)
        serializer = EntrenadorSerializer(entrenador)  
        return Response(serializer.data) 

  

