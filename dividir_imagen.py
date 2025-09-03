from PIL import Image
import os

def dividir_guardar_image(ruta_imagen, carpeta_destino, divisiones_por_columna):
    # Cargar la imagen dentro del bloque `with`
    with Image.open(ruta_imagen) as img:
        ancho, alto = img.size

        # Calcular el tamaño de los cuadrados y el número de divisiones por fila
        tamaño_cuadrado = ancho // divisiones_por_columna
        divisiones_por_filas = alto // tamaño_cuadrado

        # Crear carpeta de destino si no existe
        os.makedirs(carpeta_destino, exist_ok=True)

        # Dividir la imagen en cuadrados y guardarlos
        contador = 0
        for i in range(divisiones_por_filas):
            for j in range(divisiones_por_columna):
                # Coordenadas del cuadrado
                izquierda = j * tamaño_cuadrado
                superior = i * tamaño_cuadrado
                derecha = izquierda + tamaño_cuadrado
                inferior = superior + tamaño_cuadrado

                # Cortar y guardar el cuadrado
                cuadrado = img.crop((izquierda, superior, derecha, inferior))
                nombre_archivo = f"tile_{contador + 1}.png"
                cuadrado.save(os.path.join(carpeta_destino, nombre_archivo))
                contador += 1

# Llamar a la función con los parámetros deseados
dividir_guardar_image("assets/images/Tiles/TX_Tileset_Grass.png", "assets/images/Tiles/", 8)
