from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurante, Inventario, Asignacion, Grupo  # Aseguramos que Grupo también esté importado

class AsignacionInline(admin.TabularInline):
    model = Asignacion
    extra = 1  # Esto permite agregar asignaciones adicionales en el mismo formulario
    fields = ('restaurante_destino', 'cantidad_asignada', 'fecha_asignacion')  # Los campos que se van a mostrar
    readonly_fields = ('fecha_asignacion',)  # Hace que la fecha sea de solo lectura

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion')
    search_fields = ('nombre',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('imagen_preview', 'nombre', 'codigo', 'cantidad', 'marca', 'material', 'fecha_ingreso', 'restaurante', 'grupo_display')
    search_fields = ('nombre', 'codigo', 'marca', 'restaurante__nombre', 'grupo__nombre')  # Permitimos búsqueda por grupo
    list_filter = ('material', 'marca', 'restaurante', 'grupo')  # Agregamos filtro por grupo
    readonly_fields = ('imagen_preview',)
    inlines = [AsignacionInline]  # Esto va a permitir agregar asignaciones directamente desde Inventario

    def imagen_preview(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.imagen.url)
        return "Sin imagen"
    
    imagen_preview.short_description = "Vista previa"

    def grupo_display(self, obj):
        return obj.grupo.nombre if obj.grupo else "Sin grupo"
    
    grupo_display.short_description = "Grupo"

@admin.register(Asignacion)
class AsignacionAdmin(admin.ModelAdmin):
    list_display = ('inventario', 'restaurante_origen', 'restaurante_destino', 'cantidad_asignada', 'fecha_asignacion')
    search_fields = ('inventario__nombre', 'restaurante_origen__nombre', 'restaurante_destino__nombre')
    list_filter = ('restaurante_origen', 'restaurante_destino')

@admin.register(Grupo)  # Registro del modelo Grupo en el admin para gestión de grupos
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)  # Mostrar solo el nombre del grupo
    search_fields = ('nombre',)  # Permite buscar por nombre de grupo
