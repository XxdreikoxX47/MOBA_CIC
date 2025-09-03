import pygame
import gif_pygame

# Inicializa Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Carga el GIF
gif = gif_pygame.load("assets//images//characters//Mario.gif")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibuja el GIF en la pantalla
    screen.fill((255, 255, 255))
    gif.render(screen, (100, 100))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

#######################################################################


# Carga el GIF usando gif_pygame
gif = gif_pygame.load("assets/images/characters/Mario.gif")

# Escala los frames del GIF
scaled_frames = [pygame.transform.scale(frame, (frame.get_width() * constante_1.SCALA_PERSONAJE,
                                                frame.get_height() * constante_1.SCALA_PERSONAJE))
                 for frame in gif.frames]

screen = pygame.display.set_mode(
    (constante_1.ANCHO_VENTANA, constante_1.ALTO_VENTANA))
clock = pygame.time.Clock()

jugador = Personaje(50, 50, scaled_frames[0])  # Usa el primer frame del GIF


reloj = pygame.time.Clock()  # CONTROLA EL FRAME RATE

run = True
frame_index = 0

while run:
    reloj.tick(constante_1.FPS)  # FPS

    screen.fill(constante_1.COLOR_BG)

 # Mostrar en ventana
    jugador.dibujar(screen)
    Torre_1.dibujar(screen)


# Dibuja el frame actual del GIF en la pantalla
    screen.blit(scaled_frames[frame_index], (100, 100))
    # Avanza al siguiente frame
    frame_index = (frame_index + 1) % len(scaled_frames)
