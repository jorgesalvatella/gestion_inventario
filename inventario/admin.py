from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurante, Inventario

@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ubicacion')
    search_fields = ('nombre',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = ('imagen_preview', 'nombre', 'codigo', 'cantidad', 'marca', 'material', 'fecha_ingreso', 'restaurante')
    search_fields = ('nombre', 'codigo', 'marca', 'restaurante__nombre')
    list_filter = ('material', 'marca', 'restaurante')
    readonly_fields = ('imagen_preview',)

    def imagen_preview(self, obj):
        if obj.imagen and hasattr(obj.imagen, 'url'):
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;" />', obj.imagen.url)
        return "Sin imagen"
    
    imagen_preview.short_description = "Vista previa"
