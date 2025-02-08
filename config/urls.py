from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar 'path' y 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventario/', include('inventario.urls')),  # Asegúrate de tener esta línea para incluir las rutas de la app 'inventario'
]

# Si tienes archivos estáticos o medios (como imágenes), añade estas líneas al final
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
