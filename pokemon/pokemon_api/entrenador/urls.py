from django.urls import path 
from . import views
from .views import *




urlpatterns = [
    path('listar', views.listar, name="listar"),
    path('login', views.login, name="login"),
    path('crear', views.crear, name="crear"),
    path('pokemones/<int:id>', views.listarPokemones, name="listar_pokemones"),
    path('post/<int:pk>', Entrenador_APIView.as_view()),
]


    
