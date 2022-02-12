from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('entrenador/', include("entrenador.urls") ),
    path('pokemones/', include("pokemones.urls") )
]
