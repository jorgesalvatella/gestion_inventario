from django.db import models
from django.utils.timezone import now

class Restaurante(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    ubicacion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Restaurantes"

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    restaurante = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name="inventario", default=1)
    imagen = models.ImageField(upload_to='inventario/', blank=True, null=True)
    nombre = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField()
    material = models.CharField(max_length=255, blank=True, null=True)
    marca = models.CharField(max_length=255, blank=True, null=True)
    codigo = models.CharField(max_length=100, unique=True)
    fecha_ingreso = models.DateTimeField(default=now, blank=True)

    class Meta:
        verbose_name_plural = "Inventarios"
        ordering = ['-fecha_ingreso']

    def __str__(self):
        return f"{self.nombre} ({self.codigo}) - {self.restaurante.nombre}"

class Asignacion(models.Model):
    inventario = models.ForeignKey(Inventario, on_delete=models.CASCADE)
    restaurante_origen = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name="envios")
    restaurante_destino = models.ForeignKey(Restaurante, on_delete=models.CASCADE, related_name="recepciones")
    cantidad_asignada = models.PositiveIntegerField()
    fecha_asignacion = models.DateTimeField(default=now, blank=True)

    class Meta:
        verbose_name_plural = "Asignaciones"
        ordering = ['-fecha_asignacion']

    def __str__(self):
        return f"{self.cantidad_asignada} de {self.inventario.nombre} de {self.restaurante_origen.nombre} a {self.restaurante_destino.nombre}"
