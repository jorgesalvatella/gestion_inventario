from django.shortcuts import render
from .models import Inventario

def agregar_producto(request):
    if request.method == "POST":
        # Lógica para agregar un producto
        pass
    return render(request, 'inventario/agregar_producto.html')

def asignar_producto(request):
    if request.method == "POST":
        # Lógica para asignar un producto
        pass
    return render(request, 'inventario/asignar_producto.html')
