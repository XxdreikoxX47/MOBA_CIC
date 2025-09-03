import pygame
import constante_1


class Torre(object):

    def __init__(self, image_t, x=0, y=0, equipo=1, ID=0):
        self.image = image_t

        self.forma = pygame.Rect(
            0, 0, constante_1.ANCHO_TORRE, constante_1.ALTO_TORRE)
        self.forma.center = (x, y)

        self.ID = ID
        self.type = "Torre"
        self.x = x
        self.y = y
        self.equipo = equipo
        self.salud = 25000
        self.salud_max = +25000
        self.multilabel = True
        self.labels = ["t1", "t2"]
        if equipo == 1:
            self.codificacion = self.labels[0]
        else:
            self.codificacion = self.labels[1]
        self.target = None
        self.limite = 0
        self.boton1 = False
        self.attack_time = 0
        self.esperaCuracion = 0
        self.mapa = None

    def dibujar(self, ventana):
        ventana.blit(self.image, self.forma)
        # pygame.draw.rect(ventana, constante_1.COLOR_TORRE, self.forma)
