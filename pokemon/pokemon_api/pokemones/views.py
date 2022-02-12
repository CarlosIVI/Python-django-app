from django.shortcuts import render
from .models import Pokemones
from django.shortcuts import  render, redirect

def listar(r):
    context = {
        "pokemones": Pokemones.objects.all()
    }
    return render(r, "pokemones/listar.html", context)
