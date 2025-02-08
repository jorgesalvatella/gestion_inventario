from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, Asignacion, Restaurante, Grupo  # Importamos los modelos necesarios
from .forms import AsignacionForm, InventarioForm  # Importamos los formularios necesarios
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
from .models import Inventario
from datetime import datetime

def agregar_producto(request):
    ultimo_producto = Inventario.objects.order_by('-fecha_ingreso').first()

    if request.method == "POST":
        form = InventarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('agregar_producto')  # Redirige para ver el último agregado
    else:
        form = InventarioForm()

    return render(request, 'inventario/agregar_producto.html', {
        'form': form,
        'ultimo_producto': ultimo_producto,
    })



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


from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, Restaurante, Grupo
from .forms import InventarioForm

def inventario_list(request):
    productos = Inventario.objects.all()
    restaurantes = Restaurante.objects.all()
    grupos = Grupo.objects.all()

    # Filtros
    nombre = request.GET.get('nombre')
    restaurante = request.GET.get('restaurante')
    grupo = request.GET.get('grupo')
    material = request.GET.get('material')
    marca = request.GET.get('marca')

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

    orden = request.GET.get('orden')
    if orden:
        productos = productos.order_by(orden)

    # Paginación
    paginator = Paginator(productos, 10)  # 10 productos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'inventario/inventario_list.html', {
        'page_obj': page_obj,
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

def generar_pdf_inventario(request):
    """Genera un PDF con el inventario paginado, ordenado y con imágenes."""

    # Obtener la URL base del sitio para cargar imágenes
    base_url = request.build_absolute_uri('/').rstrip('/')

    # Obtener datos ordenados por restaurante y nombre de producto
    productos = Inventario.objects.all().order_by("restaurante__nombre", "nombre")

    # Contexto para la plantilla HTML
    context = {
        'productos': productos,
        'base_url': base_url,
        'fecha_impresion': datetime.now().strftime("%d/%m/%Y"),
    }

    # Renderizar HTML con contexto
    html_string = render_to_string("inventario/inventario_pdf.html", context)

    # Generar el PDF con estilos CSS
    pdf = HTML(string=html_string, base_url=base_url).write_pdf(
        stylesheets=[CSS(string="""
            @page {
                size: A4 landscape;
                margin: 20mm;
            }
            body {
                font-family: Arial, sans-serif;
                font-size: 12px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
                word-wrap: break-word;
                overflow-wrap: break-word;
                max-width: 200px;
            }
            th {
                background-color: #f2f2f2;
                font-weight: bold;
            }
            img {
                width: 80px;
                height: 80px;
                object-fit: cover;
            }
        """)]
    )

    # Configurar respuesta HTTP
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventario.pdf"'
    return response