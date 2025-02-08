import pandas as pd
from django.core.files import File
from inventario.models import Inventario, Restaurante
from django.conf import settings

def importar_inventarios():
    # Cargar el archivo Excel
    archivo_excel = 'ruta/a/tu/archivo.xlsx'  # Asegúrate de poner la ruta correcta
    df = pd.read_excel(archivo_excel)

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        # Obtener el restaurante
        restaurante = Restaurante.objects.get(nombre=row['Restaurante'])

        # Crear el inventario
        imagen_path = row['Imagen']  # El campo de la imagen en el Excel
        imagen = None

        # Si se proporciona la ruta de la imagen
        if imagen_path:
            imagen = File(open(imagen_path, 'rb'))

        # Crear el producto (inventario)
        inventario = Inventario.objects.create(
            nombre=row['Nombre'],
            cantidad=row['Cantidad'],
            material=row['Material'],
            marca=row['Marca'],
            codigo=row['Codigo'],
            restaurante=restaurante,
            imagen=imagen if imagen else None
        )

        print(f"Producto '{row['Nombre']}' importado correctamente.")

# Llamar a la función
importar_inventarios()
