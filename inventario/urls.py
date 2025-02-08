from django.urls import path
from .views import agregar_producto, asignar_producto

urlpatterns = [
    path('agregar-producto/', agregar_producto, name='agregar_producto'),
    path('asignar-producto/', asignar_producto, name='asignar_producto'),
]
