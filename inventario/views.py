from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, Asignacion, Restaurante, Grupo  # Importamos los modelos necesarios
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


def inventario_list(request):
    productos = Inventario.objects.all()
    restaurantes = Restaurante.objects.all()
    grupos = Grupo.objects.all()

    # Obtener los parámetros de filtrado
    nombre = request.GET.get('nombre')
    restaurante = request.GET.get('restaurante')
    grupo = request.GET.get('grupo')
    material = request.GET.get('material')
    marca = request.GET.get('marca')
    orden = request.GET.get('orden')

    # Aplicar filtros si existen
    if nombre:
        productos = productos.filter(nombre__icontains=nombre)
    if restaurante:
        productos = productos.filter(restaurante_id=restaurante)
    if grupo:
        productos = productos.filter(grupo_id=grupo)
    if material:
        productos = productos.filter(material__icontains=material)
    if marca:
        productos = productos.filter(marca__icontains=marca)
    
    # Aplicar ordenamiento si se especifica
    if orden:
        productos = productos.order_by(orden)

    return render(request, 'inventario/inventario_list.html', {
        'productos': productos,
        'restaurantes': restaurantes,
        'grupos': grupos,
    })


def inventario_edit(request, pk):
    """ Vista para editar un producto existente """
    inventario = get_object_or_404(Inventario, pk=pk)
    
    if request.method == 'POST':
        form = InventarioForm(request.POST, request.FILES, instance=inventario)
        if form.is_valid():
            form.save()
            return redirect('inventario_list')  # Redirige al listado de inventarios
    else:
        form = InventarioForm(instance=inventario)

    return render(request, 'inventario/inventario_edit.html', {'form': form, 'inventario': inventario})


def asignaciones_list(request):
    asignaciones = Asignacion.objects.all()  # Obtiene todas las asignaciones
    return render(request, 'inventario/asignaciones_list.html', {'asignaciones': asignaciones})
