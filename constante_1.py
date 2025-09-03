# Ventana
ANCHO_VENTANA = 1900
ALTO_VENTANA = 1080

# Tamaño de la cuadricula
TILE_SIZE = 160  # Se puede usar de ser necesario!!!
TILE_TYPES = 15
FILAS = 7
COLUMNAS = 9
LIMITE_PANTALLA_v = 440
LIMITE_PANTALLA_H = 925

# Pirmera vista
ANCHO_CELDA = 1900 // 9
ALTO_CELDA = 1080 // 7


# Personaje atacante

# ALTO_PERSONAJE = 0.5
# ANCHO_PERSONAJE = 0.5
COLOR_PERSONAJE = (0, 255, 0)
COLOR_BG = (0, 0, 20)
FPS = 144  # Frames en los que se mueve el personaje
VELOCIDAD = 5
SCALA_PERSONAJE = 2

# Personaje Torre

ALTO_TORRE = 90
ANCHO_TORRE = 35
COLOR_TORRE = (255, 0, 0)
SCALA_PERSONAJET = 9
COLOR_ARMA = (255, 0, 0)

# Diseño del enemigo

ANCHO_ENEMIGO = 25
ALTO_ENEMIGO = 15
VELOCIDAD_ENEMIGO = 3
COLOR_ENEMIGO = (5, 0, 10)

# Arma O
SCALA_BACULO = 0.20

SCALA_ATAQUE_ESPECIAL21 = 1
SCALA_ATAQUE_ESPECIAL11 = 9
SCALA_ATAQUE_EXPLOSION = 1.5
SCALA_ATAQUE_ESPECIALMAX = 10
# BLuz
VELOCIDAD_BLuz = 16
SACALA_BLUZ = 0.09
COOLDOWN_BLuz = 500

# Enemigos
SCALA_ENEMIGOS = 7

# Color de texto
ROJO = (203, 50, 55)

# Color de cuadricula
BLANCO = (255, 255, 255)


# ATAQUE BASICO
ALCANCE_MAXIMOBASICO = 3 * ANCHO_CELDA

# ATAQUE BASICO 21
ALCANCE_MAXIMO21 = 3 * ANCHO_CELDA
DURACION_ATAQUEBASICO21 = 0.5


# AtaEsp22
VELOCIDAD_ATA_ESP22 = 25  # Velocidad del proyectil
DURACION_ATA_ESP22 = 1  # Duración del ataque en segundos
DAÑO_BASE_ATA_ESP22 = 50  # Daño base del proyectil
RADIO_ATA_ESP22_CUADRICULAS = 4  # Radio de ataque en cuadriculas
# Tiempo que la imagen queda después del impacto (1 seg)
TIEMPO_DESAPARECER_ATA_ESP22 = 250
TIEMPO_ENFRIAMIENTO_ATA_ESP22 = 3  # Tiempo de enfriamiento del ataque en segundos


# AtaEspMAX

VELOCIDAD_ATA_ESPMAX = 25  # Velocidad del proyectil
DURACION_ATA_ESPMAX = 1  # Duración del ataque en segundos
DAÑO_BASE_ATA_ESPMAX = 50  # Daño base del proyectil
RADIO_ATA_ESPMAX_CUADRICULAS = 4  # Radio de ataque en cuadriculas
# Tiempo que la imagen queda después del impacto (1 seg)
TIEMPO_DESAPARECER_ATA_ESPMAX = 250
# Tiempo de enfriamiento del ataque en segundos
TIEMPO_ENFRIAMIENTO_ATA_ESPMAX = 3
