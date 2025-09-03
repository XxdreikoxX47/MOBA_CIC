import pygame
import time


def pantalla_de_carga(pantalla):
    pantalla.fill((0, 0, 0))  # Fondo negro
    fuente = pygame.font.Font(None, 50)
    texto = fuente.render("Cargando recursos...", True, (255, 255, 255))

    # ✅ Calcular posición para centrar texto
    texto_rect = texto.get_rect(
        center=(pantalla.get_width() // 2, pantalla.get_height() // 3))
    pantalla.blit(texto, texto_rect)

    pygame.display.flip()

    recursos = [
        "assets/images/Escenarios/Fondo_pasto.png",
        "assets/images/characters/Player/player_0.png",
        "assets/images/characters/Player/player_1.png",
        "assets/images/Weaponds/Magico_0.png",
        "assets/images/Weaponds/BLuz.png",
        "assets/images/Weaponds/FireBool_2_1.png",
        "assets/images/Weaponds/BolaMorada.png",
        "assets/images/Weaponds/FireboolRed.png"
    ]

    cargados = []  # Lista de objetos cargados
    ancho_barra_total = 400  # Tamaño total de la barra de carga
    # ✅ Centrar barra de carga
    barra_x = (pantalla.get_width() - ancho_barra_total) // 2
    # ✅ Colocar barra en el centro verticalmente
    barra_y = pantalla.get_height() // 2

    for i, recurso in enumerate(recursos):
        imagen = pygame.image.load(recurso).convert_alpha()  # Cargar imagen
        cargados.append(imagen)  # Guardar imagen en la lista

        # ✅ Evitar que la barra de progreso se reinicie
        pantalla.fill((0, 0, 0))  # Fondo negro
        pantalla.blit(texto, texto_rect)  # Mantener el texto centrado

        # ✅ Barra de progreso con posición central
        ancho_barra = ((i + 1) / len(recursos)) * ancho_barra_total
        pygame.draw.rect(pantalla, (255, 255, 255),
                         (barra_x, barra_y, ancho_barra, 30))

        pygame.display.flip()
        pygame.time.delay(500)  # Ajusta tiempo de carga por recurso

    pygame.time.delay(1000)  # Pausa antes de comenzar el juego
    return cargados
