from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, Asignacion  # Importamos los modelos necesarios
from .forms import AsignacionForm, InventarioForm  # Importamos los formularios necesarios


def agregar_producto(request):
    if request.method == "POST":
        form = InventarioForm(request.POST, request.FILES)  # ✅ Agregamos request.FILES para imágenes
        if form.is_valid():
            form.save()
            return redirect('inventario_list')  # ✅ Redirige después de guardar
    else:
        form = InventarioForm()
    return render(request, 'inventario/agregar_producto.html', {'form': form})

def asignar_producto(request):
    """ Vista para asignar productos """
    if request.method == "POST":
        form = AsignacionForm(request.POST)  # Usamos el formulario correcto
        if form.is_valid():
            form.save()
            return redirect('inventario_list')  # Redirigir después de asignar
    else:
        form = AsignacionForm()
    return render(request, 'inventario/asignar_producto.html', {'form': form})
    
    return render(request, 'inventario/asignar_producto.html', {'form': form})

def inventario_list(request):
    """ Vista que muestra la lista de productos en el inventario """
    inventarios = Inventario.objects.all()
    return render(request, 'inventario/inventario_list.html', {'inventarios': inventarios})

def inventario_edit(request, pk):
    """ Vista para editar un producto existente """
    inventario = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')  # Redirige al listado de inventarios
    else:
        form = InventarioForm(instance=inventario)

    return render(request, 'inventario/inventario_edit.html', {'form': form, 'inventario': inventario})

def asignaciones_list(request):
    asignaciones = Asignacion.objects.all()  # Obtiene todas las asignaciones
    return render(request, 'inventario/asignaciones_list.html', {'asignaciones': asignaciones})
