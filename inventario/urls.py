from django.urls import path
from .views import inventario_list, agregar_producto, asignar_producto, asignaciones_list, inventario_edit

urlpatterns = [
    path('', inventario_list, name='inventario_list'),
    path('agregar/', agregar_producto, name='agregar_producto'),
    path('asignar/', asignar_producto, name='asignar_producto'),
    path('asignaciones/', asignaciones_list, name='asignaciones_list'),
    path('editar/<int:pk>/', inventario_edit, name='inventario_edit'),  # Nueva ruta agregada
]
