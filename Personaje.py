import pygame
import constante_1

clock = pygame.time.Clock()

class Personaje():
    def __init__(self, x, y, animaciones, energia, tipo):
        self.vivo = True
        self.vida = energia  # Atributo vida
        self.energia = energia
        self.flip = False
        self.animaciones = animaciones
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x, y)
        self.tipo = tipo

    def dibujar(self, ventana):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        ventana.blit(imagen_flip, self.forma)

    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.forma.x += delta_x
        self.forma.y += delta_y

        posicion_pantalla = [0, 0]

        if self.tipo == 1:
            if self.forma.right > (constante_1.ANCHO_VENTANA - constante_1.LIMITE_PANTALLA_H):
                posicion_pantalla[0] = (constante_1.ANCHO_VENTANA - constante_1.LIMITE_PANTALLA_H) - self.forma.right
                self.forma.right = constante_1.ANCHO_VENTANA - constante_1.LIMITE_PANTALLA_H
            if self.forma.left < constante_1.LIMITE_PANTALLA_H:
                posicion_pantalla[0] = constante_1.LIMITE_PANTALLA_H - self.forma.left
                self.forma.left = constante_1.LIMITE_PANTALLA_H
            if self.forma.bottom > (constante_1.ALTO_VENTANA - constante_1.LIMITE_PANTALLA_v):
                posicion_pantalla[1] = (constante_1.ALTO_VENTANA - constante_1.LIMITE_PANTALLA_v) - self.forma.bottom
                self.forma.bottom = constante_1.ALTO_VENTANA - constante_1.LIMITE_PANTALLA_v
            if self.forma.top < constante_1.LIMITE_PANTALLA_v:
                posicion_pantalla[1] = constante_1.LIMITE_PANTALLA_v - self.forma.top
                self.forma.top = constante_1.LIMITE_PANTALLA_v

        return posicion_pantalla

    def update(self):
        cooldown_animacion = 75
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0

    def recibir_dano(self, dano):
        self.vida -= dano
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            print(f"{self.tipo} ha sido derrotado.")
