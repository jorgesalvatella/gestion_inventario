from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventario, Asignacion, Restaurante, Grupo  # Importamos los modelos necesarios
from .forms import AsignacionForm, InventarioForm  # Importamos los formularios necesarios
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from .models import Inventario

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
    """Genera un PDF con el inventario paginado y columnas ajustadas automáticamente."""
    
    # Configurar respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventario.pdf"'

    # Configurar lienzo PDF en tamaño carta horizontal
    pdf_canvas = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)  # Obtener dimensiones
    
    # Cargar logo (Asegúrate de que el archivo esté en "static/images/logo.png")
    logo_path = "static/images/logo.png"
    try:
        logo = ImageReader(logo_path)
        pdf_canvas.drawImage(logo, 40, height - 80, width=120, height=50, preserveAspectRatio=True)
    except:
        pass  # Si no hay logo, no detiene la generación del PDF

    # Encabezado
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawString(200, height - 60, "📦 Reporte de Inventario")

    # Definir encabezados y calcular anchos dinámicos de columnas
    headers = ["ID", "Nombre", "Restaurante", "Grupo", "Material", "Marca", "Cantidad", "Fecha"]
    productos = Inventario.objects.all()

    # Determinar ancho dinámico de columnas basado en el contenido más largo
    max_widths = [max(len(str(getattr(p, field.lower(), ""))) for p in productos) for field in headers]
    base_width = 50
    col_widths = [max(base_width, w * 7) for w in max_widths]  # Escalar por caracteres
    
    start_x, start_y = 40, height - 100  # Posición inicial
    line_height = 20  # Espaciado entre líneas
    
    def draw_table(pdf_canvas, start_y, productos):
        """Dibuja la tabla paginada en el PDF."""
        y = start_y
        pdf_canvas.setFont("Helvetica-Bold", 10)
        
        # Dibujar encabezados de la tabla
        for i, header in enumerate(headers):
            pdf_canvas.drawString(start_x + sum(col_widths[:i]), y, header)

        pdf_canvas.line(start_x, y - 5, start_x + sum(col_widths), y - 5)  # Línea debajo de encabezado
        y -= line_height

        # Dibujar filas del inventario
        pdf_canvas.setFont("Helvetica", 9)
        for producto in productos:
            datos = [
                str(producto.id),
                producto.nombre,
                producto.restaurante.nombre if producto.restaurante else "N/A",
                producto.grupo.nombre if producto.grupo else "N/A",
                producto.material or "N/A",
                producto.marca or "N/A",
                str(producto.cantidad),
                producto.fecha_ingreso.strftime("%d/%m/%Y"),
            ]
            for i, dato in enumerate(datos):
                pdf_canvas.drawString(start_x + sum(col_widths[:i]), y, dato)

            y -= line_height

            if y < 40:  # Si llega al final de la página, agregar nueva página
                pdf_canvas.showPage()
                y = height - 100  # Reset posición
                
                # Redibujar encabezado en nueva página
                pdf_canvas.setFont("Helvetica-Bold", 16)
                pdf_canvas.drawString(200, height - 60, "📦 Reporte de Inventario")
                pdf_canvas.setFont("Helvetica-Bold", 10)
                for i, header in enumerate(headers):
                    pdf_canvas.drawString(start_x + sum(col_widths[:i]), y, header)
                pdf_canvas.line(start_x, y - 5, start_x + sum(col_widths), y - 5)
                y -= line_height
                pdf_canvas.setFont("Helvetica", 9)
        
    draw_table(pdf_canvas, start_y, productos)
    
    pdf_canvas.showPage()
    pdf_canvas.save()
    return response